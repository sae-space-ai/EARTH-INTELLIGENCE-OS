"""Event consumer — Kafka/Redpanda adapter."""

from __future__ import annotations

import json
from typing import Any, Callable, Optional

from packages.contracts.event import EventEnvelope
from packages.core.config import get_settings
from packages.core.logging import get_logger

logger = get_logger(__name__)


class EventConsumer:
    """Consumes events from Kafka-compatible message bus."""

    def __init__(
        self,
        group_id: str,
        topics: list[str],
        brokers: Optional[str] = None,
    ) -> None:
        """Initialize consumer.

        Args:
            group_id: Consumer group ID.
            topics: Topics to subscribe to.
            brokers: Broker addresses (defaults to settings).
        """
        settings = get_settings()
        self._brokers = brokers or settings.event_bus_brokers
        self._group_id = group_id
        self._topics = topics
        self._consumer: Any = None

    def _get_consumer(self) -> Any:
        """Lazy-initialize Kafka consumer."""
        if self._consumer is None:
            try:
                from confluent_kafka import Consumer

                config = {
                    "bootstrap.servers": self._brokers,
                    "group.id": self._group_id,
                    "auto.offset.reset": "earliest",
                    "enable.auto.commit": False,
                }
                self._consumer = Consumer(config)
                self._consumer.subscribe(self._topics)
            except ImportError:
                logger.warning("confluent-kafka not installed, consumer disabled")
                return None
        return self._consumer

    def consume(self, handler: Callable[[EventEnvelope], None], max_messages: int = 1) -> int:
        """Consume and process messages.

        Args:
            handler: Callback for each event.
            max_messages: Maximum messages to process.

        Returns:
            Number of messages processed.
        """
        consumer = self._get_consumer()
        if consumer is None:
            return 0

        processed = 0
        for _ in range(max_messages):
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                logger.error("Consumer error", extra={"error": msg.error().str()})
                continue

            try:
                data = json.loads(msg.value().decode("utf-8"))
                event = EventEnvelope.from_dict(data)
                handler(event)
                consumer.commit(msg)
                processed += 1
            except Exception:
                logger.exception("Failed to process message")

        return processed

    def close(self) -> None:
        """Close consumer connection."""
        if self._consumer:
            self._consumer.close()
