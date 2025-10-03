'use client';

import { FormEvent, useMemo, useState } from 'react';
import clsx from 'clsx';

import { uploadDocuments, exportComparisonReport } from '@/lib/api';
import { UploadResponse } from '@/types/comparison';
import { classNameForMatch, formatConfidence, formatMatchLabel, formatRisk } from '@/utils/format';

const MAX_FILE_SIZE = Number(process.env.NEXT_PUBLIC_MAX_FILE_SIZE ?? '26214400');

const formatFileSize = (bytes: number) => `${(bytes / (1024 * 1024)).toFixed(1)} MB`;

type ExportFormat = 'pdf' | 'csv' | 'json';

export default function HomePage() {
  const [invoiceFile, setInvoiceFile] = useState<File | null>(null);
  const [bolFile, setBolFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [result, setResult] = useState<UploadResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [exportingFormat, setExportingFormat] = useState<ExportFormat | null>(null);

  const summary = result?.comparison_result.summary;
  const comparisonRows = result?.comparison_result.field_comparisons ?? [];

  const canSubmit = useMemo(() => !!invoiceFile && !!bolFile && !isUploading, [invoiceFile, bolFile, isUploading]);

  const resetState = () => {
    setInvoiceFile(null);
    setBolFile(null);
    setResult(null);
    setError(null);
    setStatusMessage(null);
  };

  const handleFileChange = (file: File | undefined | null, setter: (value: File | null) => void) => {
    if (!file) {
      setter(null);
      return;
    }

    if (file.size > MAX_FILE_SIZE) {
      setError(`File ${file.name} exceeds the limit of ${formatFileSize(MAX_FILE_SIZE)}.`);
      setter(null);
      return;
    }

    setter(file);
    setError(null);
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!invoiceFile || !bolFile) {
      setError('Please select both documents before uploading.');
      return;
    }

    try {
      setIsUploading(true);
      setError(null);
      setStatusMessage(null);

      const response = await uploadDocuments(invoiceFile, bolFile);
      setResult(response);
      setStatusMessage('Documents processed successfully. Review the comparison below.');
    } catch (submissionError) {
      const message = submissionError instanceof Error ? submissionError.message : 'Unexpected error while uploading.';
      setError(message);
    } finally {
      setIsUploading(false);
    }
  };

  const handleExport = async (format: ExportFormat) => {
    if (!result || exportingFormat) {
      return;
    }

    try {
      setExportingFormat(format);
      const exportData = await exportComparisonReport(result.session_id, format, summary);
      const objectUrl = URL.createObjectURL(exportData.blob);
      const link = document.createElement('a');
      link.href = objectUrl;
      link.download = exportData.filename;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(objectUrl);
      setStatusMessage(`Report exported as ${format.toUpperCase()}.`);
    } catch (exportError) {
      const message = exportError instanceof Error ? exportError.message : 'Unable to export report.';
      setError(message);
    } finally {
      setExportingFormat(null);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 pb-16">
      <div className="mx-auto max-w-6xl px-6 pt-12">
        <header className="mb-12 flex flex-col gap-4">
          <span className="inline-flex w-fit items-center rounded-full border border-primary-500/40 bg-primary-500/10 px-4 py-1 text-sm font-medium text-primary-200">
            VendeYa Ops Toolkit
          </span>
          <h1 className="text-4xl font-semibold text-white md:text-5xl">Document comparison workspace</h1>
          <p className="max-w-3xl text-lg text-slate-300">
            Upload a commercial invoice and bill of lading to detect discrepancies instantly. Keep all stakeholders aligned
            with exportable PDF, CSV, or JSON reports.
          </p>
        </header>

        <section className="grid gap-8 lg:grid-cols-[1.3fr,1fr]">
          <form onSubmit={handleSubmit} className="space-y-6 rounded-3xl border border-slate-700/60 bg-slate-900/60 p-8 shadow-soft">
            <div>
              <h2 className="text-2xl font-semibold text-white">1. Upload shipment documents</h2>
              <p className="mt-2 text-sm text-slate-300">
                Supported formats: PDF, JPG, JPEG, PNG — up to {formatFileSize(MAX_FILE_SIZE)} each.
              </p>
            </div>

            <div className="grid gap-5 md:grid-cols-2">
              <label className="flex cursor-pointer flex-col rounded-2xl border border-dashed border-slate-600 bg-slate-800/40 p-5 text-center transition hover:border-primary-400 hover:bg-slate-800/70">
                <span className="text-sm uppercase tracking-wide text-slate-400">Commercial invoice</span>
                <span className="mt-3 text-base font-medium text-white">
                  {invoiceFile ? invoiceFile.name : 'Select file'}
                </span>
                <input
                  type="file"
                  accept=".pdf,.jpg,.jpeg,.png"
                  className="hidden"
                  onChange={(event) => handleFileChange(event.target.files?.[0], setInvoiceFile)}
                />
              </label>

              <label className="flex cursor-pointer flex-col rounded-2xl border border-dashed border-slate-600 bg-slate-800/40 p-5 text-center transition hover:border-primary-400 hover:bg-slate-800/70">
                <span className="text-sm uppercase tracking-wide text-slate-400">Bill of lading</span>
                <span className="mt-3 text-base font-medium text-white">{bolFile ? bolFile.name : 'Select file'}</span>
                <input
                  type="file"
                  accept=".pdf,.jpg,.jpeg,.png"
                  className="hidden"
                  onChange={(event) => handleFileChange(event.target.files?.[0], setBolFile)}
                />
              </label>
            </div>

            {error && (
              <div className="rounded-2xl border border-danger-500/40 bg-danger-500/10 px-4 py-3 text-sm text-danger-200">
                {error}
              </div>
            )}

            {statusMessage && !error && (
              <div className="rounded-2xl border border-success-500/40 bg-success-500/10 px-4 py-3 text-sm text-success-200">
                {statusMessage}
              </div>
            )}

            <div className="flex flex-wrap gap-4">
              <button
                type="submit"
                disabled={!canSubmit}
                className={clsx(
                  'inline-flex items-center justify-center rounded-full px-6 py-3 text-sm font-semibold transition focus:outline-none focus:ring-2 focus:ring-primary-400 focus:ring-offset-2 focus:ring-offset-slate-900',
                  canSubmit
                    ? 'bg-primary-500 text-white hover:bg-primary-400'
                    : 'cursor-not-allowed bg-slate-700 text-slate-300'
                )}
              >
                {isUploading ? 'Processing…' : 'Run comparison'}
              </button>

              <button
                type="button"
                onClick={resetState}
                className="inline-flex items-center justify-center rounded-full border border-slate-700 px-6 py-3 text-sm font-semibold text-slate-200 transition hover:border-slate-500 hover:text-white"
              >
                Reset
              </button>
            </div>
          </form>

          <aside className="space-y-4 rounded-3xl border border-slate-700/60 bg-slate-900/60 p-8 shadow-soft">
            <h2 className="text-2xl font-semibold text-white">2. Monitor job status</h2>
            <p className="text-sm text-slate-300">
              After processing, we store a session ID so you can retrieve the results, export reports, or revisit the
              comparison later.
            </p>

            <dl className="grid gap-3 text-sm text-slate-200">
              <div className="rounded-2xl border border-slate-700/60 bg-slate-800/60 px-4 py-3">
                <dt className="text-xs uppercase tracking-wide text-slate-400">Session ID</dt>
                <dd className="mt-1 font-mono text-sm">{result?.session_id ?? '—'}</dd>
              </div>
              <div className="rounded-2xl border border-slate-700/60 bg-slate-800/60 px-4 py-3">
                <dt className="text-xs uppercase tracking-wide text-slate-400">Job ID</dt>
                <dd className="mt-1 font-mono text-sm">{result?.job_id ?? '—'}</dd>
              </div>
              <div className="rounded-2xl border border-slate-700/60 bg-slate-800/60 px-4 py-3">
                <dt className="text-xs uppercase tracking-wide text-slate-400">Status</dt>
                <dd className="mt-1 text-sm font-semibold text-success-200">{result ? 'Completed' : 'Pending upload'}</dd>
              </div>
            </dl>

            <div className="pt-2">
              <p className="text-xs uppercase tracking-wide text-slate-400">Export comparison report</p>
              <div className="mt-3 flex flex-wrap gap-3">
                {(['pdf', 'csv', 'json'] as ExportFormat[]).map((format) => (
                  <button
                    key={format}
                    type="button"
                    disabled={!result || exportingFormat === format}
                    onClick={() => handleExport(format)}
                    className={clsx(
                      'inline-flex items-center justify-center rounded-full border px-4 py-2 text-xs font-semibold uppercase tracking-wide transition',
                      !result
                        ? 'cursor-not-allowed border-slate-700 text-slate-500'
                        : 'border-primary-500/50 bg-primary-500/10 text-primary-200 hover:border-primary-400 hover:text-primary-100',
                      exportingFormat === format && 'opacity-60'
                    )}
                  >
                    {exportingFormat === format ? 'Preparing…' : `Download ${format.toUpperCase()}`}
                  </button>
                ))}
              </div>
            </div>
          </aside>
        </section>

        {result && (
          <section className="mt-12 space-y-8">
            <div className="rounded-3xl border border-slate-700/60 bg-slate-900/60 p-8 shadow-soft">
              <h2 className="text-2xl font-semibold text-white">3. Review key metrics</h2>
              <div className="mt-6 grid gap-4 md:grid-cols-3 lg:grid-cols-6">
                {[
                  { label: 'Total fields', value: summary?.total_fields ?? 0 },
                  { label: 'Exact matches', value: summary?.matching_fields ?? 0 },
                  { label: 'Partial matches', value: summary?.partial_matches ?? 0 },
                  { label: 'Discrepancies', value: summary?.discrepant_fields ?? 0 },
                  { label: 'Missing fields', value: summary?.missing_fields ?? 0 },
                  { label: 'Confidence', value: summary ? `${Math.round(summary.confidence_score * 100)}%` : '0%' },
                ].map((metric) => (
                  <div
                    key={metric.label}
                    className="rounded-2xl border border-slate-700/60 bg-slate-800/50 px-5 py-4 text-center"
                  >
                    <dt className="text-xs uppercase tracking-wide text-slate-400">{metric.label}</dt>
                    <dd className="mt-2 text-2xl font-semibold text-white">{metric.value}</dd>
                  </div>
                ))}
              </div>

              <div className="mt-6 flex flex-wrap gap-3 text-sm text-slate-200">
                <span className="inline-flex items-center gap-2 rounded-full border border-slate-600 bg-slate-800/60 px-4 py-2">
                  Overall match:
                  <span className="font-semibold text-white">{formatMatchLabel(summary?.overall_match ?? 'mismatch')}</span>
                </span>
                <span className="inline-flex items-center gap-2 rounded-full border border-slate-600 bg-slate-800/60 px-4 py-2">
                  Overall risk: <span className="font-semibold text-white">{formatRisk(summary?.overall_risk ?? 'LOW')}</span>
                </span>
              </div>

              {summary?.risk_by_category && (
                <div className="mt-6 space-y-2 text-sm text-slate-200">
                  <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-400">Risk by category</h3>
                  <div className="flex flex-wrap gap-3">
                    {Object.entries(summary.risk_by_category).map(([category, risk]) => (
                      <span
                        key={category}
                        className="inline-flex items-center gap-2 rounded-full border border-slate-600 bg-slate-800/60 px-4 py-2"
                      >
                        <span className="text-xs uppercase tracking-wide text-slate-400">{category}</span>
                        <span className="font-semibold text-white">{formatRisk(risk)}</span>
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div className="rounded-3xl border border-slate-700/60 bg-slate-900/60 p-8 shadow-soft">
              <h2 className="text-2xl font-semibold text-white">4. Field-by-field comparison</h2>
              <div className="mt-6 overflow-hidden rounded-2xl border border-slate-700/60">
                <table className="min-w-full divide-y divide-slate-700 text-sm">
                  <thead className="bg-slate-800/70 text-xs uppercase tracking-wide text-slate-400">
                    <tr>
                      <th scope="col" className="px-4 py-3 text-left">Field</th>
                      <th scope="col" className="px-4 py-3 text-left">Invoice value</th>
                      <th scope="col" className="px-4 py-3 text-left">Bill of lading value</th>
                      <th scope="col" className="px-4 py-3 text-left">Confidence</th>
                      <th scope="col" className="px-4 py-3 text-left">Status</th>
                      <th scope="col" className="px-4 py-3 text-left">Notes</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800 text-slate-100">
                    {comparisonRows.map((row) => (
                      <tr key={row.field_name} className="hover:bg-slate-800/40">
                        <td className="px-4 py-3 font-medium text-white">{row.field_name.replace(/_/g, ' ')}</td>
                        <td className="px-4 py-3 text-slate-200">{row.invoice_value ?? '—'}</td>
                        <td className="px-4 py-3 text-slate-200">{row.bol_value ?? '—'}</td>
                        <td className="px-4 py-3 text-slate-200">{formatConfidence(row.confidence)}</td>
                        <td className="px-4 py-3">
                          <span
                            className={clsx(
                              'inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-wide',
                              classNameForMatch(row.match)
                            )}
                          >
                            {formatMatchLabel(row.match)}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-slate-300">{row.notes ?? '—'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </section>
        )}
      </div>
    </main>
  );
}
