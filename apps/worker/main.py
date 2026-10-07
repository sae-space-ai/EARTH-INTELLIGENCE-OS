"""Background worker — processes transactional outbox events."""

from __future__ import annotations

import asyncio
import json
import signal
import sys
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from packages.core.config import get_settings
from packages.core.logging import get_logger, setup_logging
from packages.events.publisher import EventPublisher
from packages.events.outbox import OutboxEvent

logger = get_logger(__name__)


class OutboxWorker:
    """Processes transactional outbox events and publishes to event bus.

    Polls for pending outbox events, publishes them via EventPublisher,
    and marks them as delivered. Implements retry with exponential backoff.
    """

    def __init__(self, poll_interval: float = 1.0) -> None:
        """Initialize worker."""
        self._poll_interval = poll_interval
        self._running = False
        self._publisher: Optional[EventPublisher] = None
        self._pending: list[OutboxEvent] = []

    async def start(self) -> None:
        """Start the worker loop."""
        setup_logging()
        logger.info("Outbox worker starting")

        self._running = True
        self._publisher = EventPublisher()

        # Handle graceful shutdown
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(self.stop()))

        while self._running:
            try:
                await self._process_pending()
                await asyncio.sleep(self._poll_interval)
            except Exception:
                logger.exception("Worker loop error")
                await asyncio.sleep(self._poll_interval * 2)

        logger.info("Outbox worker stopped")

    async def stop(self) -> None:
        """Stop the worker gracefully."""
        logger.info("Outbox worker shutdown requested")
        self._running = False
        if self._publisher:
            self._publisher.flush(timeout=5.0)

    async def _process_pending(self) -> None:
        """Process pending outbox events."""
        # In production, this would query the database
        # For Phase 0, we demonstrate the pattern
        for event in list(self._pending):
            if event.next_retry_at and event.next_retry_at > datetime.utcnow():
                continue

            try:
                self._publish_event(event)
                event.status = "DELIVERED"
                event.delivered_at = datetime.utcnow()
                logger.info(
                    "Outbox event delivered",
                    extra={"event_id": str(event.id), "event_type": event.event_type},
                )
            except Exception as e:
                event.retry_count += 1
                event.error_message = str(e)
                # Exponential backoff: 1s, 2s, 4s, 8s, ...
                backoff = timedelta(seconds=2 ** event.retry_count)
                event.next_retry_at = datetime.utcnow() + backoff
                event.status = "RETRY"
                logger.warning(
                    "Outbox event failed, will retry",
                    extra={
                        "event_id": str(event.id),
                        "retry_count": event.retry_count,
                        "error": str(e),
                    },
                )

        # Remove delivered events
        self._pending = [e for e in self._pending if e.status != "DELIVERED"]

    def _publish_event(self, event: OutboxEvent) -> None:
        """Publish single outbox event to event bus."""
        if not self._publisher:
            raise RuntimeError("Publisher not initialized")

        from packages.contracts.event import EventEnvelope

        envelope = EventEnvelope(
            event_id=event.id,
            event_type=event.event_type,
            schema_version=event.schema_version,
            occurred_at=event.created_at,
            produced_at=datetime.utcnow(),
            producer="earth-intelligence-worker",
            trace_id=event.trace_id,
            correlation_id=event.correlation_id,
            payload=event.payload,
        )

        # Extract topic from event_type (e.g., "observation.received.v1" → "observation.received")
        topic_parts = event.event_type.rsplit(".", 1)
        topic = topic_parts[0] if len(topic_parts) > 1 else event.event_type

        self._publisher.publish(envelope, topic)

    def enqueue(self, event: OutboxEvent) -> None:
        """Add event to pending queue (for testing/demo)."""
        self._pending.append(event)


async def main() -> None:
    """Worker entry point."""
    worker = OutboxWorker()
    await worker.start()


if __name__ == "__main__":
    asyncio.run(main())
