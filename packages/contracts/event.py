"""Event envelope and serialization."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class EventEnvelope(BaseModel):
    """Versioned event envelope for the event bus."""

    event_id: UUID = Field(default_factory=uuid4)
    event_type: str = Field(min_length=1, max_length=255)
    schema_version: str = Field(default="v1", max_length=20)
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
    produced_at: datetime = Field(default_factory=datetime.utcnow)
    producer: str = Field(min_length=1, max_length=100)
    trace_id: UUID
    correlation_id: UUID
    payload: dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary for event bus."""
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "schema_version": self.schema_version,
            "occurred_at": self.occurred_at.isoformat(),
            "produced_at": self.produced_at.isoformat(),
            "producer": self.producer,
            "trace_id": str(self.trace_id),
            "correlation_id": str(self.correlation_id),
            "payload": self.payload,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EventEnvelope:
        """Deserialize from dictionary."""
        return cls(
            event_id=UUID(data["event_id"]),
            event_type=data["event_type"],
            schema_version=data["schema_version"],
            occurred_at=datetime.fromisoformat(data["occurred_at"]),
            produced_at=datetime.fromisoformat(data["produced_at"]),
            producer=data["producer"],
            trace_id=UUID(data["trace_id"]),
            correlation_id=UUID(data["correlation_id"]),
            payload=data["payload"],
        )
