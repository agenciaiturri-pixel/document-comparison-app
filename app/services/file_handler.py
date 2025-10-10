"""Helper utilities for persisting uploaded files."""
from __future__ import annotations

import asyncio
from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings
from app.schemas.comparison import DocumentType
from app.utils.logger import setup_logger


logger = setup_logger("file_handler")


class FileHandler:
    """Persist uploaded files and manage storage directories."""

    def __init__(self) -> None:
        self._base_dir = Path(settings.UPLOAD_DIR)
        self._base_dir.mkdir(parents=True, exist_ok=True)

    async def save_uploaded_file(self, upload: UploadFile, document_type: DocumentType, job_id: str) -> Path:
        """Store an UploadFile asynchronously and return its path."""

        job_dir = self._base_dir / job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        extension = Path(upload.filename or "").suffix or ".bin"
        filename = f"{document_type.value}{extension}"
        destination = job_dir / filename

        logger.info("Saving %s to %s", upload.filename, destination)
        contents = await upload.read()
        await asyncio.to_thread(destination.write_bytes, contents)
        await upload.close()
        return destination

    async def cleanup_job(self, job_id: str) -> None:
        """Remove all files associated with a job."""

        job_dir = self._base_dir / job_id
        if not job_dir.exists():
            return

        for path in job_dir.glob("*"):
            try:
                path.unlink(missing_ok=True)
            except OSError as exc:  # pragma: no cover - best effort cleanup
                logger.warning("Failed to delete %s: %s", path, exc)
        try:
            job_dir.rmdir()
        except OSError:
            logger.debug("Directory %s not removed (may not be empty)", job_dir)
