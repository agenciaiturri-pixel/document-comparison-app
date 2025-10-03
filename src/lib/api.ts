import { ComparisonSummary, JobStatus, UploadResponse } from '@/types/comparison';

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export async function uploadDocuments(invoice: File, billOfLading: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append('commercial_invoice', invoice);
  formData.append('bill_of_lading', billOfLading);

  const response = await fetch(`${API_URL}/api/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || 'Failed to upload documents');
  }

  return response.json();
}

export async function fetchJobStatus(jobId: string): Promise<JobStatus> {
  const response = await fetch(`${API_URL}/api/status/${jobId}`);
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || 'Unable to retrieve job status');
  }
  return response.json();
}

export async function exportComparisonReport(
  sessionId: string,
  format: 'pdf' | 'csv' | 'json',
  summary?: ComparisonSummary
): Promise<{ blob: Blob; filename: string }> {
  const url = new URL(`${API_URL}/api/export/${sessionId}`);
  url.searchParams.set('format', format);

  const response = await fetch(url.toString(), {
    method: 'POST',
    headers: summary ? { 'Content-Type': 'application/json' } : undefined,
    body: summary ? JSON.stringify(summary) : undefined,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || 'Failed to export report');
  }

  const blob = await response.blob();
  const disposition = response.headers.get('content-disposition');
  let filename = `${sessionId}.${format}`;

  if (disposition) {
    const match = disposition.match(/filename="?([^";]+)"?/i);
    if (match?.[1]) {
      filename = match[1];
    }
  }

  return { blob, filename };
}
