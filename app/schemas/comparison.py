"""Pydantic schemas that define the contract for document comparison."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    INVOICE = "commercial_invoice"
    BILL_OF_LADING = "bill_of_lading"


class MatchLevel(str, Enum):
    EXACT = "exact"
    PARTIAL = "partial"
    MISMATCH = "mismatch"
    MISSING = "missing"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ExportFormat(str, Enum):
    PDF = "pdf"
    CSV = "csv"
    JSON = "json"


class ExtractedField(BaseModel):
    name: str
    value: Optional[str] = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class DocumentData(BaseModel):
    document_type: DocumentType
    raw_text: str = ""
    fields: Dict[str, ExtractedField] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True


class DocumentFieldComparison(BaseModel):
    field_name: str
    invoice_value: Optional[str]
    bol_value: Optional[str]
    match: MatchLevel
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    notes: Optional[str] = None


class ComparisonSummary(BaseModel):
    total_fields: int
    matching_fields: int
    partial_matches: int
    discrepant_fields: int
    missing_fields: int
    overall_match: MatchLevel
    overall_risk: RiskLevel
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    risk_by_category: Dict[str, RiskLevel] = Field(default_factory=dict)


class ComparisonResult(BaseModel):
    field_comparisons: List[DocumentFieldComparison] = Field(default_factory=list)
    summary: ComparisonSummary


class ComparisonRequest(BaseModel):
    session_id: str
    commercial_invoice: DocumentData
    bill_of_lading: DocumentData


class ComparisonResponse(BaseModel):
    session_id: str
    comparison_result: ComparisonResult
    timestamp: datetime


class ComparisonSummaryPayload(BaseModel):
    session_id: str
    created_at: datetime
    summary: ComparisonSummary


__all__ = [
    "ComparisonRequest",
    "ComparisonResponse",
    "ComparisonResult",
    "ComparisonSummary",
    "ComparisonSummaryPayload",
    "DocumentData",
    "DocumentFieldComparison",
    "DocumentType",
    "ExtractedField",
    "ExportFormat",
    "MatchLevel",
    "RiskLevel",
]
