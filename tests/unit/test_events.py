"""Unit tests for event envelope and catalog."""

import pytest
from datetime import datetime
from uuid import uuid4

from packages.contracts.event import EventEnvelope
from packages.contracts.catalog import EVENT_CATALOG, OBSERVATION_RECEIVED


def test_event_envelope_creation():
    """Test EventEnvelope creation."""
    envelope = EventEnvelope(
        event_type="observation.received",
        producer="test-service",
        trace_id=uuid4(),
        correlation_id=uuid4(),
        payload={"observation_id": str(uuid4())},
    )
    assert envelope.schema_version == "v1"
    assert envelope.event_type == "observation.received"


def test_event_envelope_serialization():
    """Test EventEnvelope serialization/deserialization."""
    original = EventEnvelope(
        event_type="test.event",
        producer="test",
        trace_id=uuid4(),
        correlation_id=uuid4(),
        payload={"key": "value"},
    )

    data = original.to_dict()
    restored = EventEnvelope.from_dict(data)

    assert restored.event_id == original.event_id
    assert restored.event_type == original.event_type
    assert restored.payload == original.payload


def test_event_catalog_uniqueness():
    """Test all event topics have unique names."""
    names = [t.full_name for t in EVENT_CATALOG]
    assert len(names) == len(set(names)), "Duplicate event topic names found"


def test_event_catalog_has_required_topics():
    """Test catalog contains all required topics."""
    topic_names = {t.full_name for t in EVENT_CATALOG}
    required = [
        "observation.received.v1",
        "earth-event.created.v1",
        "mission.requested.v1",
        "audit.recorded.v1",
    ]
    for req in required:
        assert req in topic_names, f"Missing required topic: {req}"


def test_observation_received_topic():
    """Test observation.received topic definition."""
    assert OBSERVATION_RECEIVED.name == "observation.received"
    assert OBSERVATION_RECEIVED.version == "v1"
    assert OBSERVATION_RECEIVED.domain == "OBSERVATION"
    assert OBSERVATION_RECEIVED.full_name == "observation.received.v1"
