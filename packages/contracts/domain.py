"""Domain models — core business entities."""

from __future__ import annotations

import enum
from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class KnowledgeState(str, enum.Enum):
    """Epistemic classification of scientific knowledge."""

    OBSERVED = "OBSERVED"
    INFERRED = "INFERRED"
    FORECAST = "FORECAST"
    SIMULATED = "SIMULATED"


class SensorType(str, enum.Enum):
    """Supported sensor types."""

    SAR = "SAR"
    LIDAR = "LIDAR"
    HYPERSPECTRAL = "HYPERSPECTRAL"
    SUBSURFACE_RADAR = "SUBSURFACE_RADAR"
    OTHER = "OTHER"


class ModelVersionStatus(str, enum.Enum):
    """Model lifecycle states."""

    REGISTERED = "REGISTERED"
    VALIDATING = "VALIDATING"
    VALIDATED = "VALIDATED"
    REJECTED = "REJECTED"
    PROMOTED = "PROMOTED"
    DEPLOYED = "DEPLOYED"
    RETIRED = "RETIRED"


class Satellite(BaseModel):
    """Satellite platform entity."""

    id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=1, max_length=255)
    platform_type: str = Field(min_length=1, max_length=100)
    status: str = Field(default="ACTIVE", max_length=50)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Sensor(BaseModel):
    """Sensor attached to a satellite."""

    id: UUID = Field(default_factory=uuid4)
    satellite_id: UUID
    sensor_type: SensorType
    name: str = Field(min_length=1, max_length=255)
    status: str = Field(default="ACTIVE", max_length=50)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Observation(BaseModel):
    """Sensor observation with geospatial footprint."""

    id: UUID = Field(default_factory=uuid4)
    satellite_id: UUID
    sensor_id: UUID
    acquired_at: datetime
    footprint: dict[str, Any]  # GeoJSON geometry
    bbox: list[float] = Field(min_length=4, max_length=4)  # [west, south, east, north]
    processing_level: str = Field(max_length=50)
    quality_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    raw_asset_id: UUID
    processed_asset_id: Optional[UUID] = None
    model_version_id: Optional[UUID] = None
    knowledge_state: KnowledgeState = KnowledgeState.OBSERVED
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("bbox")
    @classmethod
    def validate_bbox(cls, v: list[float]) -> list[float]:
        """Validate bounding box coordinates."""
        west, south, east, north = v
        if not (-180 <= west <= 180):
            raise ValueError(f"West longitude out of range: {west}")
        if not (-90 <= south <= 90):
            raise ValueError(f"South latitude out of range: {south}")
        if not (-180 <= east <= 180):
            raise ValueError(f"East longitude out of range: {east}")
        if not (-90 <= north <= 90):
            raise ValueError(f"North latitude out of range: {north}")
        if south > north:
            raise ValueError(f"South ({south}) must be <= North ({north})")
        return v

    @field_validator("footprint")
    @classmethod
    def validate_footprint(cls, v: dict[str, Any]) -> dict[str, Any]:
        """Validate GeoJSON geometry structure."""
        if "type" not in v:
            raise ValueError("Footprint must have 'type' field")
        if "coordinates" not in v:
            raise ValueError("Footprint must have 'coordinates' field")
        return v


class ObservationAsset(BaseModel):
    """Binary asset associated with an observation."""

    id: UUID = Field(default_factory=uuid4)
    observation_id: UUID
    bucket: str
    key: str
    size: int = Field(ge=0)
    content_type: str
    sha256: str = Field(min_length=64, max_length=64)
    processing_level: str = Field(max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AreaOfInterest(BaseModel):
    """Geographic area for observation requests."""

    id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=1, max_length=255)
    geometry: dict[str, Any]  # GeoJSON
    created_at: datetime = Field(default_factory=datetime.utcnow)


class EarthEvent(BaseModel):
    """Detected planetary change or anomaly."""

    id: UUID = Field(default_factory=uuid4)
    event_type: str = Field(min_length=1, max_length=100)
    geometry: dict[str, Any]  # GeoJSON
    first_seen: datetime
    last_seen: datetime
    confidence: float = Field(ge=0.0, le=1.0)
    priority: int = Field(ge=1, le=5, description="Priority 1=highest, 5=lowest")
    knowledge_state: KnowledgeState
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("last_seen")
    @classmethod
    def validate_last_seen(cls, v: datetime, info: Any) -> datetime:
        """Ensure last_seen >= first_seen."""
        if "first_seen" in info.data and v < info.data["first_seen"]:
            raise ValueError("last_seen must be >= first_seen")
        return v


class MissionRequest(BaseModel):
    """Request for satellite observation mission."""

    id: UUID = Field(default_factory=uuid4)
    aoi: dict[str, Any]  # GeoJSON geometry
    priority: int = Field(ge=1, le=10)
    requested_by: str = Field(min_length=1, max_length=255)
    status: str = Field(default="REQUESTED", max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ModelVersion(BaseModel):
    """ML model version with full provenance."""

    id: UUID = Field(default_factory=uuid4)
    model_name: str = Field(min_length=1, max_length=255)
    semantic_version: str = Field(min_length=1, max_length=50)
    git_commit: str = Field(min_length=7, max_length=40)
    framework: str = Field(min_length=1, max_length=100)
    checkpoint_uri: str
    checkpoint_sha256: str = Field(min_length=64, max_length=64)
    training_dataset_version_id: Optional[UUID] = None
    metrics: dict[str, float] = Field(default_factory=dict)
    status: ModelVersionStatus = ModelVersionStatus.REGISTERED
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DatasetVersion(BaseModel):
    """Training/evaluation dataset version."""

    id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=1, max_length=255)
    version: str = Field(min_length=1, max_length=50)
    uri: str
    sha256: str = Field(min_length=64, max_length=64)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ProvenanceRecord(BaseModel):
    """Lineage record for data transformations."""

    id: UUID = Field(default_factory=uuid4)
    input_asset_ids: list[UUID]
    output_asset_ids: list[UUID]
    operation: str = Field(min_length=1, max_length=255)
    software_version: str = Field(min_length=1, max_length=100)
    model_version_id: Optional[UUID] = None
    parameters_hash: str = Field(min_length=1, max_length=128)
    started_at: datetime
    finished_at: datetime
    trace_id: UUID
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("finished_at")
    @classmethod
    def validate_finished_at(cls, v: datetime, info: Any) -> datetime:
        """Ensure finished_at >= started_at."""
        if "started_at" in info.data and v < info.data["started_at"]:
            raise ValueError("finished_at must be >= started_at")
        return v


class AuditRecord(BaseModel):
    """Security audit trail entry."""

    id: UUID = Field(default_factory=uuid4)
    actor_type: str = Field(min_length=1, max_length=50)  # user|system|ai|service
    actor_id: str = Field(min_length=1, max_length=255)
    action: str = Field(min_length=1, max_length=255)
    resource_type: str = Field(min_length=1, max_length=100)
    resource_id: UUID
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    trace_id: Optional[UUID] = None
    metadata: dict[str, Any] = Field(default_factory=dict)
