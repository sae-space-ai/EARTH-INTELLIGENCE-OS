"""Transactional outbox — guarantees event persistence with domain operations."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class OutboxEvent(BaseModel):
    """Outbox event record for transactional outbox pattern."""

    id: UUID = Field(default_factory=uuid4)
    event_type: str = Field(min_length=1, max_length=255)
    schema_version: str = Field(default="v1", max_length=20)
    payload: dict[str, Any]
    trace_id: UUID
    correlation_id: UUID
    status: str = Field(default="PENDING", max_length=50)
    retry_count: int = Field(default=0, ge=0)
    error_message: Optional[str] = None
    next_retry_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    delivered_at: Optional[datetime] = None


class OutboxRepository:
    """Repository interface for outbox events.

    Implementation depends on database adapter (SQLAlchemy in apps).
    """

    async def save(self, event: OutboxEvent) -> OutboxEvent:
        """Save outbox event. Must be called within same transaction as domain operation."""
        raise NotImplementedError("Use concrete implementation from apps layer")

    async def get_pending(self, limit: int = 10) -> list[OutboxEvent]:
        """Get pending events for delivery."""
        raise NotImplementedError("Use concrete implementation from apps layer")

    async def mark_delivered(self, event_id: UUID) -> None:
        """Mark event as successfully delivered."""
        raise NotImplementedError("Use concrete implementation from apps layer")

    async def mark_failed(self, event_id: UUID, error: str, retry_count: int) -> None:
        """Mark event as failed with retry information."""
        raise NotImplementedError("Use concrete implementation from apps layer")
