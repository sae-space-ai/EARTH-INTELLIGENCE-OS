"""Event catalog — all supported event types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EventTopic:
    """Event topic definition."""

    name: str
    version: str
    domain: str
    description: str

    @property
    def full_name(self) -> str:
        """Return fully qualified topic name."""
        return f"{self.name}.{self.version}"


# Satellite / Constellation
SATELLITE_TELEMETRY_RECEIVED = EventTopic(
    "satellite.telemetry.received", "v1", "CONSTELLATION", "Raw telemetry received"
)
SATELLITE_STATE_UPDATED = EventTopic(
    "satellite.state.updated", "v1", "CONSTELLATION", "Satellite state changed"
)

# Observation pipeline
OBSERVATION_RECEIVED = EventTopic(
    "observation.received", "v1", "OBSERVATION", "New observation ingested"
)
OBSERVATION_VALIDATED = EventTopic(
    "observation.validated", "v1", "OBSERVATION", "Observation validated"
)
OBSERVATION_CALIBRATED = EventTopic(
    "observation.calibrated", "v1", "OBSERVATION", "Radiometric calibration applied"
)
OBSERVATION_GEOREFERENCED = EventTopic(
    "observation.georeferenced", "v1", "OBSERVATION", "Georeferencing complete"
)
OBSERVATION_COREGISTERED = EventTopic(
    "observation.coregistered", "v1", "OBSERVATION", "Coregistration complete"
)
OBSERVATION_QUALITY_SCORED = EventTopic(
    "observation.quality-scored", "v1", "OBSERVATION", "Quality score computed"
)

# Intelligence
EMBEDDING_CREATED = EventTopic(
    "embedding.created", "v1", "INTELLIGENCE", "Embedding generated"
)
CHANGE_DETECTED = EventTopic(
    "change.detected", "v1", "EARTH_EVENTS", "Temporal change detected"
)
ANOMALY_DETECTED = EventTopic(
    "anomaly.detected", "v1", "EARTH_EVENTS", "Anomaly detected"
)

# Earth Events
EARTH_EVENT_CREATED = EventTopic(
    "earth-event.created", "v1", "EARTH_EVENTS", "New Earth Event"
)
EARTH_EVENT_UPDATED = EventTopic(
    "earth-event.updated", "v1", "EARTH_EVENTS", "Earth Event updated"
)
EARTH_EVENT_CONFIRMED = EventTopic(
    "earth-event.confirmed", "v1", "EARTH_EVENTS", "Earth Event confirmed"
)

# Predictions
PREDICTION_CREATED = EventTopic(
    "prediction.created", "v1", "INTELLIGENCE", "Forecast generated"
)

# Mission
MISSION_REQUESTED = EventTopic(
    "mission.requested", "v1", "MISSION", "Mission requested"
)
MISSION_PLAN_CREATED = EventTopic(
    "mission.plan-created", "v1", "MISSION", "Mission plan created"
)
MISSION_SIMULATION_PASSED = EventTopic(
    "mission.simulation-passed", "v1", "MISSION", "Simulation passed"
)
MISSION_SIMULATION_FAILED = EventTopic(
    "mission.simulation-failed", "v1", "MISSION", "Simulation failed"
)
MISSION_AUTHORIZATION_REQUIRED = EventTopic(
    "mission.authorization-required", "v1", "MISSION", "Authorization required"
)
MISSION_APPROVED = EventTopic(
    "mission.approved", "v1", "MISSION", "Mission approved"
)
MISSION_REJECTED = EventTopic(
    "mission.rejected", "v1", "MISSION", "Mission rejected"
)

# Model registry
MODEL_REGISTERED = EventTopic(
    "model.registered", "v1", "INTELLIGENCE", "Model version registered"
)
MODEL_VALIDATION_PASSED = EventTopic(
    "model.validation-passed", "v1", "INTELLIGENCE", "Model validation passed"
)
MODEL_PROMOTED = EventTopic(
    "model.promoted", "v1", "INTELLIGENCE", "Model promoted to production"
)

# Security
AUDIT_RECORDED = EventTopic(
    "audit.recorded", "v1", "SECURITY", "Audit event recorded"
)

# Central catalog
EVENT_CATALOG: list[EventTopic] = [
    SATELLITE_TELEMETRY_RECEIVED,
    SATELLITE_STATE_UPDATED,
    OBSERVATION_RECEIVED,
    OBSERVATION_VALIDATED,
    OBSERVATION_CALIBRATED,
    OBSERVATION_GEOREFERENCED,
    OBSERVATION_COREGISTERED,
    OBSERVATION_QUALITY_SCORED,
    EMBEDDING_CREATED,
    CHANGE_DETECTED,
    ANOMALY_DETECTED,
    EARTH_EVENT_CREATED,
    EARTH_EVENT_UPDATED,
    EARTH_EVENT_CONFIRMED,
    PREDICTION_CREATED,
    MISSION_REQUESTED,
    MISSION_PLAN_CREATED,
    MISSION_SIMULATION_PASSED,
    MISSION_SIMULATION_FAILED,
    MISSION_AUTHORIZATION_REQUIRED,
    MISSION_APPROVED,
    MISSION_REJECTED,
    MODEL_REGISTERED,
    MODEL_VALIDATION_PASSED,
    MODEL_PROMOTED,
    AUDIT_RECORDED,
]
