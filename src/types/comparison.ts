export type DocumentType = 'commercial_invoice' | 'bill_of_lading';

export interface ExtractedField {
  name: string;
  value?: string | null;
  confidence: number;
}

export interface DocumentData {
  document_type: DocumentType;
  raw_text: string;
  fields: Record<string, ExtractedField>;
}

export type MatchLevel = 'exact' | 'partial' | 'mismatch' | 'missing';
export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH';

export interface DocumentFieldComparison {
  field_name: string;
  invoice_value?: string | null;
  bol_value?: string | null;
  match: MatchLevel;
  confidence: number;
  notes?: string | null;
}

export interface ComparisonSummary {
  total_fields: number;
  matching_fields: number;
  partial_matches: number;
  discrepant_fields: number;
  missing_fields: number;
  overall_match: MatchLevel;
  overall_risk: RiskLevel;
  confidence_score: number;
  risk_by_category: Record<string, RiskLevel>;
}

export interface ComparisonResult {
  field_comparisons: DocumentFieldComparison[];
  summary: ComparisonSummary;
}

export interface UploadResponse {
  job_id: string;
  session_id: string;
  message: string;
  commercial_invoice: DocumentData;
  bill_of_lading: DocumentData;
  comparison_result: ComparisonResult;
}

export interface JobStatus {
  job_id: string;
  session_id: string;
  stage: string;
  progress: number;
  status: string;
  message: string;
  updated_at: string;
}
