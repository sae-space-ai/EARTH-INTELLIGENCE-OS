"""Unit tests for tracing utilities."""

import pytest
from packages.core.tracing import (
    generate_trace_id,
    generate_correlation_id,
    set_trace_id,
    get_trace_id,
    is_valid_uuid,
)


def test_generate_trace_id():
    """Test trace ID generation."""
    trace_id = generate_trace_id()
    assert is_valid_uuid(trace_id)


def test_generate_correlation_id():
    """Test correlation ID generation."""
    corr_id = generate_correlation_id()
    assert is_valid_uuid(corr_id)


def test_set_and_get_trace_id():
    """Test trace ID context."""
    trace_id = generate_trace_id()
    set_trace_id(trace_id)
    assert get_trace_id() == trace_id


def test_is_valid_uuid():
    """Test UUID validation."""
    import uuid
    valid = str(uuid.uuid4())
    assert is_valid_uuid(valid) is True
    assert is_valid_uuid("not-a-uuid") is False
    assert is_valid_uuid("") is False
