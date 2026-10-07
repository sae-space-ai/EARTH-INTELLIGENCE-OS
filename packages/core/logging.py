"""Structured logging with trace/correlation ID support."""

from __future__ import annotations

import logging
import sys
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any, Optional

from pythonjsonlogger import jsonlogger

from packages.core.config import get_settings

# Context variables for distributed tracing
_trace_id_var: ContextVar[Optional[str]] = ContextVar("trace_id", default=None)
_correlation_id_var: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)


class EarthIntelligenceFormatter(jsonlogger.JsonFormatter):
    """JSON log formatter with trace context injection."""

    def add_fields(self, log_record: dict[str, Any], record: logging.LogRecord, message: str) -> None:
        """Add structured fields to log record."""
        super().add_fields(log_record, record, message)
        log_record["timestamp"] = datetime.now(timezone.utc).isoformat()
        log_record["service"] = "earth-intelligence-os"

        settings = get_settings()
        log_record["environment"] = settings.environment

        trace_id = _trace_id_var.get()
        if trace_id:
            log_record["trace_id"] = trace_id

        correlation_id = _correlation_id_var.get()
        if correlation_id:
            log_record["correlation_id"] = correlation_id


def setup_logging() -> None:
    """Configure structured JSON logging for the application."""
    settings = get_settings()

    handler = logging.StreamHandler(sys.stdout)
    formatter = EarthIntelligenceFormatter()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, settings.log_level))

    # Reduce noise from third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger instance."""
    return logging.getLogger(name)


def set_trace_context(trace_id: Optional[str] = None, correlation_id: Optional[str] = None) -> None:
    """Set trace context for current execution scope."""
    if trace_id is not None:
        _trace_id_var.set(trace_id)
    if correlation_id is not None:
        _correlation_id_var.set(correlation_id)


def get_trace_id() -> Optional[str]:
    """Get current trace ID from context."""
    return _trace_id_var.get()


def get_correlation_id() -> Optional[str]:
    """Get current correlation ID from context."""
    return _correlation_id_var.get()
