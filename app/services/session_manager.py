"""In-memory storage for comparison sessions and job metadata."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional

from app.schemas.comparison import ComparisonResult, DocumentData
from app.utils.logger import setup_logger


logger = setup_logger("session_manager")


@dataclass
class StoredSession:
    """Representation of a processed comparison session."""

    job_id: str
    session_id: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    status: str = "pending"
    progress: int = 0
    invoice: Optional[DocumentData] = None
    bill_of_lading: Optional[DocumentData] = None
    comparison: Optional[ComparisonResult] = None

    def mark_processing(self) -> None:
        self.status = "processing"
        self.progress = 10
        self.updated_at = datetime.utcnow()

    def mark_completed(
        self,
        invoice: DocumentData,
        bill_of_lading: DocumentData,
        comparison: ComparisonResult,
    ) -> None:
        self.invoice = invoice
        self.bill_of_lading = bill_of_lading
        self.comparison = comparison
        self.status = "completed"
        self.progress = 100
        self.updated_at = datetime.utcnow()

    def to_status_payload(self) -> Dict[str, object]:
        return {
            "job_id": self.job_id,
            "session_id": self.session_id,
            "stage": self.status,
            "progress": self.progress,
            "status": self.status,
            "message": "Processing completed successfully"
            if self.status == "completed"
            else "Processing",
            "updated_at": self.updated_at.isoformat() + "Z",
        }

    def to_session_payload(self) -> Dict[str, object]:
        return {
            "session_id": self.session_id,
            "job_id": self.job_id,
            "status": self.status,
            "created_at": self.created_at.isoformat() + "Z",
            "updated_at": self.updated_at.isoformat() + "Z",
            "comparison_result": self.comparison.model_dump()
            if self.comparison
            else None,
        }

    def to_result_payload(self) -> Dict[str, object]:
        return {
            "job_id": self.job_id,
            "session_id": self.session_id,
            "timestamp": self.updated_at.isoformat() + "Z",
            "invoiceData": self.invoice.model_dump() if self.invoice else None,
            "blData": self.bill_of_lading.model_dump() if self.bill_of_lading else None,
            "comparisons": [comp.model_dump() for comp in self.comparison.field_comparisons]
            if self.comparison
            else [],
            "summary": self.comparison.summary.model_dump()
            if self.comparison
            else None,
        }


class ComparisonSessionManager:
    """Coordinate access to session metadata in a threadsafe manner."""

    def __init__(self) -> None:
        self._sessions: Dict[str, StoredSession] = {}
        self._job_index: Dict[str, str] = {}
        self._lock = asyncio.Lock()

    async def create_session(self, job_id: str, session_id: str) -> None:
        async with self._lock:
            session = StoredSession(job_id=job_id, session_id=session_id)
            session.mark_processing()
            self._sessions[session_id] = session
            self._job_index[job_id] = session_id
            logger.info("Session %s created for job %s", session_id, job_id)

    async def store_results(
        self,
        job_id: str,
        invoice: DocumentData,
        bill_of_lading: DocumentData,
        comparison: ComparisonResult,
    ) -> None:
        async with self._lock:
            session_id = self._job_index.get(job_id)
            if not session_id:
                raise KeyError(f"Job {job_id} not found")
            session = self._sessions[session_id]
            session.mark_completed(invoice, bill_of_lading, comparison)
            logger.info("Stored results for job %s (session %s)", job_id, session_id)

    async def get_job_status(self, job_id: str) -> Dict[str, object]:
        async with self._lock:
            session_id = self._job_index.get(job_id)
            if not session_id:
                raise KeyError(f"Job {job_id} not found")
            return self._sessions[session_id].to_status_payload()

    async def get_job_result(self, job_id: str) -> Dict[str, object]:
        async with self._lock:
            session_id = self._job_index.get(job_id)
            if not session_id:
                raise KeyError(f"Job {job_id} not found")
            payload = self._sessions[session_id].to_result_payload()
            if not payload["summary"]:
                raise ValueError("Comparison has not completed yet")
            return payload

    async def get_session(self, session_id: str) -> Dict[str, object]:
        async with self._lock:
            session = self._sessions.get(session_id)
            if not session:
                raise KeyError(f"Session {session_id} not found")
            return session.to_session_payload()

    async def get_job_id_for_session(self, session_id: str) -> Optional[str]:
        async with self._lock:
            session = self._sessions.get(session_id)
            return session.job_id if session else None

    async def get_session_summary(self, session_id: str) -> ComparisonResult:
        async with self._lock:
            session = self._sessions.get(session_id)
            if not session or not session.comparison:
                raise KeyError(f"Session {session_id} not found")
            return session.comparison

    async def delete_session(self, session_id: str) -> Optional[str]:
        async with self._lock:
            session = self._sessions.pop(session_id, None)
            if not session:
                return None
            self._job_index.pop(session.job_id, None)
            logger.info("Session %s deleted", session_id)
            return session.job_id


session_manager = ComparisonSessionManager()


__all__ = ["ComparisonSessionManager", "session_manager"]

