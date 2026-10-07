"""Distributed tracing utilities."""

from __future__ import annotations

import uuid
from contextvars import ContextVar
from typing import Optional

_trace_id_var: ContextVar[Optional[str]] = ContextVar("trace_id", default=None)
_correlation_id_var: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)


def generate_trace_id() -> str:
    """Generate a new UUID v4 trace ID."""
    return str(uuid.uuid4())


def generate_correlation_id() -> str:
    """Generate a new UUID v4 correlation ID."""
    return str(uuid.uuid4())


def set_trace_id(trace_id: str) -> None:
    """Set trace ID in current context."""
    _trace_id_var.set(trace_id)


def get_trace_id() -> Optional[str]:
    """Get trace ID from current context."""
    return _trace_id_var.get()


def set_correlation_id(correlation_id: str) -> None:
    """Set correlation ID in current context."""
    _correlation_id_var.set(correlation_id)


def get_correlation_id() -> Optional[str]:
    """Get correlation ID from current context."""
    return _correlation_id_var.get()


def is_valid_uuid(value: str) -> bool:
    """Check if string is a valid UUID v4."""
    try:
        uuid.UUID(value, version=4)
        return True
    except (ValueError, AttributeError):
        return False
