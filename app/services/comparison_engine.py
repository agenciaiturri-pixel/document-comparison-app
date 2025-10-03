"""Logic responsible for comparing extracted document fields."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Dict, Iterable, List, Tuple

from app.core.config import settings
from app.schemas.comparison import (
    ComparisonResult,
    ComparisonSummary,
    DocumentData,
    DocumentFieldComparison,
    MatchLevel,
    RiskLevel,
)
from app.utils.logger import setup_logger


logger = setup_logger("comparison_engine")


@dataclass
class FieldComparisonConfig:
    name: str
    weight: float = 1.0
    risk_category: str = "general"


CORE_FIELDS: Iterable[FieldComparisonConfig] = [
    FieldComparisonConfig("invoice_number", 1.2, "commercial"),
    FieldComparisonConfig("bill_of_lading_number", 1.2, "logistics"),
    FieldComparisonConfig("total_amount", 1.0, "commercial"),
    FieldComparisonConfig("shipper", 0.8, "parties"),
    FieldComparisonConfig("consignee", 0.8, "parties"),
    FieldComparisonConfig("origin", 0.5, "logistics"),
    FieldComparisonConfig("destination", 0.5, "logistics"),
]


class ComparisonEngine:
    """Compare extracted data from the invoice and bill of lading."""

    async def compare_documents(
        self, invoice: DocumentData, bill_of_lading: DocumentData
    ) -> ComparisonResult:
        logger.info("Comparing %s with %s", invoice.document_type, bill_of_lading.document_type)
        field_configs = {cfg.name: cfg for cfg in CORE_FIELDS}
        tasks = [
            asyncio.create_task(
                self._compare_field(name, invoice.fields.get(name), bill_of_lading.fields.get(name), field_configs.get(name))
            )
            for name in self._collect_field_names(invoice, bill_of_lading)
        ]
        comparisons = await asyncio.gather(*tasks)

        summary = self._build_summary(comparisons)
        return ComparisonResult(field_comparisons=comparisons, summary=summary)

    def _collect_field_names(self, invoice: DocumentData, bol: DocumentData) -> Iterable[str]:
        names = set(invoice.fields.keys()) | set(bol.fields.keys())
        return sorted(names)

    async def _compare_field(
        self,
        name: str,
        invoice_field,
        bol_field,
        config: FieldComparisonConfig | None,
    ) -> DocumentFieldComparison:
        match_level, confidence = await asyncio.to_thread(
            self._calculate_similarity,
            invoice_field.value if invoice_field else None,
            bol_field.value if bol_field else None,
        )

        notes = None
        if not invoice_field and not bol_field:
            notes = "Field missing in both documents"
        elif not invoice_field:
            notes = "Missing from invoice"
        elif not bol_field:
            notes = "Missing from bill of lading"

        return DocumentFieldComparison(
            field_name=name,
            invoice_value=invoice_field.value if invoice_field else None,
            bol_value=bol_field.value if bol_field else None,
            match=match_level,
            confidence=confidence,
            notes=notes,
        )

    def _calculate_similarity(self, invoice_value: str | None, bol_value: str | None) -> Tuple[MatchLevel, float]:
        if invoice_value is None and bol_value is None:
            return MatchLevel.MISSING, 0.0
        if invoice_value is None or bol_value is None:
            return MatchLevel.MISMATCH, 0.0

        invoice_norm = invoice_value.strip().lower()
        bol_norm = bol_value.strip().lower()

        if not invoice_norm and not bol_norm:
            return MatchLevel.MISSING, 0.0
        if not invoice_norm or not bol_norm:
            return MatchLevel.MISMATCH, 0.0

        ratio = SequenceMatcher(None, invoice_norm, bol_norm).ratio()
        if ratio >= settings.FUZZY_MATCH_THRESHOLD:
            return MatchLevel.EXACT, ratio
        if ratio >= settings.PARTIAL_MATCH_THRESHOLD:
            return MatchLevel.PARTIAL, ratio
        return MatchLevel.MISMATCH, ratio

    def _build_summary(self, comparisons: List[DocumentFieldComparison]) -> ComparisonSummary:
        total = len(comparisons)
        matching = sum(1 for c in comparisons if c.match == MatchLevel.EXACT)
        partial = sum(1 for c in comparisons if c.match == MatchLevel.PARTIAL)
        mismatched = sum(1 for c in comparisons if c.match == MatchLevel.MISMATCH)
        missing = sum(1 for c in comparisons if c.match == MatchLevel.MISSING)

        overall_match = MatchLevel.EXACT
        if mismatched > 0 or partial > 0:
            overall_match = MatchLevel.PARTIAL if mismatched == 0 else MatchLevel.MISMATCH

        # Compute risk heuristic
        if mismatched > 0:
            overall_risk = RiskLevel.HIGH
        elif partial > 0:
            overall_risk = RiskLevel.MEDIUM
        else:
            overall_risk = RiskLevel.LOW

        confidence = 0.0
        if total:
            confidence = sum(c.confidence for c in comparisons) / total

        risk_by_category: Dict[str, RiskLevel] = {}
        for cfg in CORE_FIELDS:
            comp = next((c for c in comparisons if c.field_name == cfg.name), None)
            if not comp:
                continue
            if comp.match == MatchLevel.EXACT:
                risk = RiskLevel.LOW
            elif comp.match == MatchLevel.PARTIAL:
                risk = RiskLevel.MEDIUM
            else:
                risk = RiskLevel.HIGH
            existing = risk_by_category.get(cfg.risk_category)
            if existing is None or risk.value > existing.value:
                risk_by_category[cfg.risk_category] = risk

        return ComparisonSummary(
            total_fields=total,
            matching_fields=matching,
            partial_matches=partial,
            discrepant_fields=mismatched,
            missing_fields=missing,
            overall_match=overall_match,
            overall_risk=overall_risk,
            confidence_score=round(confidence, 2),
            risk_by_category=risk_by_category or {"general": overall_risk},
        )
