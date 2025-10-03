"""Utilities for exporting comparison results into multiple formats."""
from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from app.core.config import settings
from app.schemas.comparison import ComparisonSummary
from app.utils.logger import setup_logger


logger = setup_logger("report_generator")


class ReportGenerator:
    """Generate PDF, CSV or JSON reports for comparison outcomes."""

    def __init__(self) -> None:
        self._reports_dir = Path(settings.REPORTS_DIR)
        self._reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_pdf_report(self, comparison: ComparisonSummary, session_id: str) -> Path:
        """Create a PDF summarising the comparison result."""

        path = self._reports_dir / f"{session_id}.pdf"
        logger.info("Generating PDF report at %s", path)
        doc = SimpleDocTemplate(str(path), pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        story.append(Paragraph("<b>Document Comparison Report</b>", styles["Title"]))
        story.append(Spacer(1, 16))
        story.append(Paragraph(f"Session ID: {session_id}", styles["Normal"]))
        story.append(Paragraph(f"Generated: {datetime.utcnow().isoformat()}Z", styles["Normal"]))
        story.append(Spacer(1, 12))

        for label, value in [
            ("Total fields", comparison.total_fields),
            ("Matching", comparison.matching_fields),
            ("Partial matches", comparison.partial_matches),
            ("Discrepant", comparison.discrepant_fields),
            ("Missing", comparison.missing_fields),
            ("Overall match", comparison.overall_match.value),
            ("Overall risk", comparison.overall_risk.value),
            ("Confidence", comparison.confidence_score),
        ]:
            story.append(Paragraph(f"<b>{label}:</b> {value}", styles["Normal"]))

        if comparison.risk_by_category:
            story.append(Spacer(1, 12))
            story.append(Paragraph("<b>Risk by category</b>", styles["Heading2"]))
            for category, risk in comparison.risk_by_category.items():
                story.append(Paragraph(f"{category.title()}: {risk.value}", styles["Normal"]))

        doc.build(story)
        return path

    def generate_csv_report(self, comparison: ComparisonSummary, session_id: str) -> Path:
        """Generate a CSV report with summary metrics."""

        path = self._reports_dir / f"{session_id}.csv"
        logger.info("Generating CSV report at %s", path)
        with path.open("w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["metric", "value"])
            writer.writerow(["total_fields", comparison.total_fields])
            writer.writerow(["matching_fields", comparison.matching_fields])
            writer.writerow(["partial_matches", comparison.partial_matches])
            writer.writerow(["discrepant_fields", comparison.discrepant_fields])
            writer.writerow(["missing_fields", comparison.missing_fields])
            writer.writerow(["overall_match", comparison.overall_match.value])
            writer.writerow(["overall_risk", comparison.overall_risk.value])
            writer.writerow(["confidence_score", comparison.confidence_score])
            for category, risk in comparison.risk_by_category.items():
                writer.writerow([f"risk_{category}", risk.value])
        return path

    def generate_json_report(self, comparison: ComparisonSummary, session_id: str) -> Path:
        """Persist comparison summary as JSON."""

        path = self._reports_dir / f"{session_id}.json"
        logger.info("Generating JSON report at %s", path)
        payload = {
            "session_id": session_id,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "summary": comparison.model_dump(),
        }
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path
