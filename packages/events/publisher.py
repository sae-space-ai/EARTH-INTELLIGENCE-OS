"""Event publisher — Kafka/Redpanda adapter."""

from __future__ import annotations

import json
from typing import Any, Optional

from packages.contracts.event import EventEnvelope
from packages.core.config import get_settings
from packages.core.logging import get_logger

logger = get_logger(__name__)


class EventPublisher:
    """Publishes events to Kafka-compatible message bus.

    Uses confluent-kafka for production-grade delivery guarantees.
    """

    def __init__(self, brokers: Optional[str] = None) -> None:
        """Initialize publisher with broker configuration."""
        settings = get_settings()
        self._brokers = brokers or settings.event_bus_brokers
        self._producer: Any = None

    def _get_producer(self) -> Any:
        """Lazy-initialize Kafka producer."""
        if self._producer is None:
            try:
                from confluent_kafka import Producer

                config = {
                    "bootstrap.servers": self._brokers,
                    "client.id": "earth-intelligence-os",
                }
                self._producer = Producer(config)
            except ImportError:
                logger.warning("confluent-kafka not installed, events will not be published")
                return None
        return self._producer

    def publish(self, event: EventEnvelope, topic: str) -> None:
        """Publish event to topic.

        Args:
            event: Event envelope to publish.
            topic: Target topic name.

        Raises:
            RuntimeError: If producer unavailable.
        """
        producer = self._get_producer()
        if producer is None:
            logger.warning("Event not published (no producer)", extra={"topic": topic, "event_id": str(event.event_id)})
            return

        data = json.dumps(event.to_dict()).encode("utf-8")

        def delivery_callback(err: Any, msg: Any) -> None:
            if err:
                logger.error("Event delivery failed", extra={"topic": topic, "error": str(err)})
            else:
                logger.info("Event delivered", extra={"topic": topic, "partition": msg.partition()})

        producer.produce(topic, value=data, callback=delivery_callback)
        producer.poll(0)

    def flush(self, timeout: float = 10.0) -> int:
        """Flush pending messages.

        Args:
            timeout: Maximum time to wait.

        Returns:
            Number of messages still in queue.
        """
        producer = self._get_producer()
        if producer is None:
            return 0
        return producer.flush(timeout)
