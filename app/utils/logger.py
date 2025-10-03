"""Logging utilities for the Document Comparison application."""
from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict

from app.core.config import settings


LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_LOG_LEVEL = logging.INFO


def _get_log_directory() -> Path:
    log_dir = settings.BASE_DIR / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def setup_logger(name: str) -> logging.Logger:
    """Configure and return a logger with stream and file handlers."""

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(DEFAULT_LOG_LEVEL)
    formatter = logging.Formatter(LOG_FORMAT)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (rotating)
    log_file = _get_log_directory() / "app.log"
    file_handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.debug("Logger initialised for %s", name)
    return logger


def log_api_request(endpoint: str, payload: Dict[str, Any] | None = None) -> None:
    """Log API request details for observability."""

    logger = logging.getLogger("api")
    if not logger.handlers:
        setup_logger("api")

    payload_str = payload if payload is not None else {}
    logger.info("Endpoint %s called with payload: %s", endpoint, payload_str)


def log_error_with_context(error: Exception, context: Dict[str, Any] | None = None) -> None:
    """Log an error including contextual metadata for troubleshooting."""

    logger = logging.getLogger("errors")
    if not logger.handlers:
        setup_logger("errors")

    context = context or {}
    logger.error("%s | Context: %s", error, context)
