"""Audit logging — security trail for all significant operations."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

from packages.contracts.domain import AuditRecord
from packages.core.logging import get_logger

logger = get_logger(__name__)


class AuditLogger:
    """Records security audit events.

    Distinguishes operational logs from security audit trail.
    All audit records are persisted for compliance and investigation.
    """

    def __init__(self) -> None:
        """Initialize audit logger."""
        self._records: list[AuditRecord] = []

    def record(
        self,
        actor_type: str,
        actor_id: str,
        action: str,
        resource_type: str,
        resource_id: UUID,
        trace_id: Optional[UUID] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> AuditRecord:
        """Record an audit event.

        Args:
            actor_type: Type of actor (user|system|ai|service).
            actor_id: Identifier of the actor.
            action: Action performed.
            resource_type: Type of resource affected.
            resource_id: ID of the resource.
            trace_id: Optional trace ID for correlation.
            metadata: Additional context.

        Returns:
            Created audit record.
        """
        record = AuditRecord(
            actor_type=actor_type,
            actor_id=actor_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            trace_id=trace_id,
            metadata=metadata or {},
        )
        self._records.append(record)

        logger.info(
            "Audit event recorded",
            extra={
                "actor_type": actor_type,
                "actor_id": actor_id,
                "action": action,
                "resource_type": resource_type,
                "resource_id": str(resource_id),
            },
        )

        return record

    def get_records(self, limit: int = 100) -> list[AuditRecord]:
        """Get recent audit records.

        Args:
            limit: Maximum records to return.

        Returns:
            List of audit records.
        """
        return self._records[-limit:]
