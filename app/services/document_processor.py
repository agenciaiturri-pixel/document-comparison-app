"""Document processing utilities for extracting structured information."""
from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable

from PyPDF2 import PdfReader
from PIL import Image

try:
    import pytesseract
except Exception:  # pragma: no cover - optional dependency at runtime
    pytesseract = None

from app.schemas.comparison import DocumentData, DocumentType, ExtractedField
from app.utils.logger import setup_logger


logger = setup_logger("document_processor")


@dataclass
class ExtractionRule:
    name: str
    patterns: Iterable[re.Pattern[str]]


INVOICE_RULES = [
    ExtractionRule(
        name="invoice_number",
        patterns=[
            re.compile(r"invoice\s*(?:no\.?|number)[:\-\s]*([A-Za-z0-9\-/]+)", re.IGNORECASE),
            re.compile(r"\bINV[-\s]?([0-9]{3,})\b", re.IGNORECASE),
        ],
    ),
    ExtractionRule(
        name="invoice_date",
        patterns=[
            re.compile(r"invoice\s*date[:\-\s]*([0-9]{2,4}[\-/][0-9]{1,2}[\-/][0-9]{2,4})", re.IGNORECASE),
            re.compile(r"date[:\-\s]*([0-9]{2,4}[\-/][0-9]{1,2}[\-/][0-9]{2,4})", re.IGNORECASE),
        ],
    ),
]


BILL_OF_LADING_RULES = [
    ExtractionRule(
        name="bill_of_lading_number",
        patterns=[
            re.compile(r"bill\s*of\s*lading\s*(?:no\.?|number)[:\-\s]*([A-Za-z0-9\-/]+)", re.IGNORECASE),
            re.compile(r"\bBOL[-\s]?([0-9]{3,})\b", re.IGNORECASE),
        ],
    ),
    ExtractionRule(
        name="bl_date",
        patterns=[
            re.compile(r"bl\s*date[:\-\s]*([0-9]{2,4}[\-/][0-9]{1,2}[\-/][0-9]{2,4})", re.IGNORECASE),
            re.compile(r"date[:\-\s]*([0-9]{2,4}[\-/][0-9]{1,2}[\-/][0-9]{2,4})", re.IGNORECASE),
        ],
    ),
]


COMMON_RULES = [
    ExtractionRule(
        name="shipper",
        patterns=[re.compile(r"shipper[:\-\s]*([A-Za-z0-9 ,.&]+)", re.IGNORECASE)],
    ),
    ExtractionRule(
        name="consignee",
        patterns=[re.compile(r"consignee[:\-\s]*([A-Za-z0-9 ,.&]+)", re.IGNORECASE)],
    ),
    ExtractionRule(
        name="notify_party",
        patterns=[re.compile(r"notify\s*party[:\-\s]*([A-Za-z0-9 ,.&]+)", re.IGNORECASE)],
    ),
    ExtractionRule(
        name="origin",
        patterns=[re.compile(r"port\s*of\s*loading[:\-\s]*([A-Za-z0-9 ,.&]+)", re.IGNORECASE)],
    ),
    ExtractionRule(
        name="destination",
        patterns=[re.compile(r"port\s*of\s*discharge[:\-\s]*([A-Za-z0-9 ,.&]+)", re.IGNORECASE)],
    ),
    ExtractionRule(
        name="total_amount",
        patterns=[
            re.compile(r"total\s*(?:amount|value)[:\-\s]*([A-Za-z$€£S/\.0-9, ]+)", re.IGNORECASE),
            re.compile(r"grand\s*total[:\-\s]*([A-Za-z$€£S/\.0-9, ]+)", re.IGNORECASE),
        ],
    ),
]


class DocumentProcessor:
    """Extract structured data from PDF or image documents."""

    async def extract_data(self, path: Path, document_type: DocumentType) -> DocumentData:
        """Read a document and extract structured fields."""

        logger.info("Extracting data from %s", path)
        text = await self._read_document_text(path)
        fields = self._apply_rules(text, document_type)
        return DocumentData(document_type=document_type, raw_text=text, fields=fields)

    async def _read_document_text(self, path: Path) -> str:
        """Extract text from PDF or image using the appropriate backend."""

        suffix = path.suffix.lower()
        if suffix == ".pdf":
            return await asyncio.to_thread(self._read_pdf, path)
        if suffix in {".png", ".jpg", ".jpeg"}:
            if pytesseract is None:
                logger.warning("pytesseract not available; returning empty text for %s", path)
                return ""
            return await asyncio.to_thread(self._read_image, path)

        logger.warning("Unsupported file extension %s. Returning empty text.", suffix)
        return ""

    @staticmethod
    def _read_pdf(path: Path) -> str:
        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    @staticmethod
    def _read_image(path: Path) -> str:
        if pytesseract is None:
            return ""
        image = Image.open(path)
        return pytesseract.image_to_string(image)

    def _apply_rules(self, text: str, document_type: DocumentType) -> Dict[str, ExtractedField]:
        """Apply extraction rules to free text."""

        normalized = text.replace("\r", " ").replace("\n", " \n ")
        rules: list[ExtractionRule] = list(COMMON_RULES)
        if document_type == DocumentType.INVOICE:
            rules = INVOICE_RULES + rules
        else:
            rules = BILL_OF_LADING_RULES + rules

        fields: Dict[str, ExtractedField] = {}
        for rule in rules:
            value = None
            confidence = 0.0
            for pattern in rule.patterns:
                match = pattern.search(normalized)
                if match:
                    value = match.group(1).strip()
                    confidence = 0.95
                    break
            fields[rule.name] = ExtractedField(name=rule.name, value=value, confidence=confidence)

        logger.debug("Extracted fields for %s: %s", document_type, fields)
        return fields
