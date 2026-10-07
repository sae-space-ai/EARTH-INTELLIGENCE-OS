"""European Space Federation domain models."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class AccessPolicy(str, Enum):
    """Data access policy classification."""
    OPEN_ANONYMOUS = "OPEN_ANONYMOUS"
    OPEN_REGISTRATION_REQUIRED = "OPEN_REGISTRATION_REQUIRED"
    FREE_REGISTRATION_REQUIRED = "FREE_REGISTRATION_REQUIRED"
    FREE_ELIGIBLE_USERS = "FREE_ELIGIBLE_USERS"
    RESTRICTED = "RESTRICTED"
    COMMERCIAL = "COMMERCIAL"
    UNKNOWN = "UNKNOWN"


class ProviderCapability(str, Enum):
    """Provider capability flags."""
    CATALOG_SEARCH = "CATALOG_SEARCH"
    STAC = "STAC"
    ODATA = "ODATA"
    REST = "REST"
    S3 = "S3"
    DOWNLOAD = "DOWNLOAD"
    SUBSETTING = "SUBSETTING"
    PROCESSING = "PROCESSING"
    TIMESERIES = "TIMESERIES"
    WMS = "WMS"
    WCS = "WCS"
    WMTS = "WMTS"
    HAPI = "HAPI"
    OPENEO = "OPENEO"
    GNSS = "GNSS"
    GNSS_CORRECTIONS = "GNSS_CORRECTIONS"
    NAVIGATION_AUTHENTICATION = "NAVIGATION_AUTHENTICATION"
    SPACE_WEATHER = "SPACE_WEATHER"
    DIGITAL_TWIN = "DIGITAL_TWIN"
    FORECAST = "FORECAST"
    SPACE_SITUATIONAL_AWARENESS = "SPACE_SITUATIONAL_AWARENESS"
    EMERGENCY_PRODUCTS = "EMERGENCY_PRODUCTS"


class ProviderHealthStatus(str, Enum):
    """Provider health status."""
    AVAILABLE = "AVAILABLE"
    DEGRADED = "DEGRADED"
    AUTH_REQUIRED = "AUTH_REQUIRED"
    RATE_LIMITED = "RATE_LIMITED"
    UNAVAILABLE = "UNAVAILABLE"
    NOT_CONFIGURED = "NOT_CONFIGURED"


class MissionLifecycleStatus(str, Enum):
    """Mission lifecycle status."""
    PLANNED = "PLANNED"
    LAUNCHED = "LAUNCHED"
    COMMISSIONING = "COMMISSIONING"
    OPERATIONAL = "OPERATIONAL"
    DEGRADED = "DEGRADED"
    ENDED = "ENDED"
    UNKNOWN = "UNKNOWN"


class SpaceEnvironmentCategory(str, Enum):
    """Space environment observation categories."""
    SOLAR_ACTIVITY = "SOLAR_ACTIVITY"
    SOLAR_FLARE = "SOLAR_FLARE"
    CME = "CME"
    SOLAR_WIND = "SOLAR_WIND"
    GEOMAGNETIC_ACTIVITY = "GEOMAGNETIC_ACTIVITY"
    RADIATION = "RADIATION"
    IONOSPHERIC_CONDITION = "IONOSPHERIC_CONDITION"
    SPACE_WEATHER_ALERT = "SPACE_WEATHER_ALERT"
    OTHER = "OTHER"


class AuthenticationStatus(str, Enum):
    """Navigation authentication status."""
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


class SpaceDataProvider(BaseModel):
    """External space data provider (ESA, EUMETSAT, Copernicus, etc.)."""
    id: UUID = Field(default_factory=uuid4)
    code: str = Field(..., description="Unique provider code (e.g., COPERNICUS_CDSE)")
    name: str
    organization_type: Optional[str] = None
    country_or_region: Optional[str] = None
    base_url: Optional[str] = None
    documentation_url: Optional[str] = None
    status: str = "ACTIVE"
    capabilities: list[ProviderCapability] = Field(default_factory=list)
    access_policy: Optional[dict[str, Any]] = None
    last_catalog_sync: Optional[datetime] = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ExternalMission(BaseModel):
    """External satellite mission (Sentinel, Meteosat, etc.)."""
    id: UUID = Field(default_factory=uuid4)
    provider_id: UUID
    mission_code: str
    name: str
    description: Optional[str] = None
    programme: Optional[str] = None
    operator: Optional[str] = None
    lifecycle_status: MissionLifecycleStatus
    launch_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    documentation_url: Optional[str] = None
    capabilities: list[str] = Field(default_factory=list)
    access_policy: Optional[dict[str, Any]] = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ExternalSpacecraft(BaseModel):
    """External spacecraft/satellite platform."""
    id: UUID = Field(default_factory=uuid4)
    provider_id: UUID
    mission_id: Optional[UUID] = None
    external_id: Optional[str] = None
    name: str
    norad_id: Optional[int] = None
    cospar_id: Optional[str] = None
    lifecycle_status: str
    launch_date: Optional[datetime] = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ExternalInstrument(BaseModel):
    """External instrument/sensor."""
    id: UUID = Field(default_factory=uuid4)
    provider_id: UUID
    mission_id: Optional[UUID] = None
    spacecraft_id: Optional[UUID] = None
    external_id: Optional[str] = None
    name: str
    sensor_type: str
    capabilities: list[str] = Field(default_factory=list)
    spatial_resolution: Optional[str] = None
    swath: Optional[str] = None
    frequency: Optional[str] = None
    wavelength_metadata: Optional[dict[str, Any]] = None
    polarizations: Optional[list[str]] = None
    spectral_bands: Optional[dict[str, Any]] = None
    product_levels: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ExternalCollection(BaseModel):
    """External data collection (STAC collection, dataset, etc.)."""
    id: UUID = Field(default_factory=uuid4)
    provider_id: UUID
    external_collection_id: str
    mission_id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    sensor_types: list[str] = Field(default_factory=list)
    temporal_extent: Optional[dict[str, Any]] = None
    spatial_extent: Optional[dict[str, Any]] = None
    processing_level: Optional[str] = None
    license_metadata: Optional[dict[str, Any]] = None
    access_policy: Optional[dict[str, Any]] = None
    capabilities: list[str] = Field(default_factory=list)
    canonical_url: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    last_synced_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ExternalSpaceService(BaseModel):
    """External space service (Copernicus services, etc.)."""
    id: UUID = Field(default_factory=uuid4)
    provider_id: UUID
    external_service_id: Optional[str] = None
    name: str
    service_type: str
    description: Optional[str] = None
    capabilities: list[str] = Field(default_factory=list)
    base_url: Optional[str] = None
    documentation_url: Optional[str] = None
    access_policy: Optional[dict[str, Any]] = None
    status: str = "ACTIVE"
    metadata: dict[str, Any] = Field(default_factory=dict)
    last_verified_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ExternalObservationCandidate(BaseModel):
    """Normalized external observation candidate from federated search."""
    provider: str
    mission: Optional[str] = None
    spacecraft: Optional[str] = None
    instrument: Optional[str] = None
    collection: Optional[str] = None
    external_item_id: str
    datetime: datetime
    geometry: dict[str, Any]
    bbox: Optional[list[float]] = None
    sensor_type: Optional[str] = None
    processing_level: Optional[str] = None
    resolution: Optional[str] = None
    cloud_cover: Optional[float] = None
    assets: dict[str, Any] = Field(default_factory=dict)
    access_policy: Optional[dict[str, Any]] = None
    license_metadata: Optional[dict[str, Any]] = None
    download_capability: bool = False
    processing_capabilities: list[str] = Field(default_factory=list)
    provider_metadata: dict[str, Any] = Field(default_factory=dict)


class SpaceEnvironmentObservation(BaseModel):
    """Space environment observation (solar activity, radiation, etc.)."""
    id: UUID = Field(default_factory=uuid4)
    provider_id: UUID
    observed_at: datetime
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    knowledge_state: str  # OBSERVED, INFERRED, FORECAST, SIMULATED
    category: SpaceEnvironmentCategory
    variable: str
    value: Optional[float] = None
    unit: Optional[str] = None
    confidence: Optional[float] = Field(None, ge=0, le=1)
    source_asset: Optional[str] = None
    provenance_metadata: Optional[dict[str, Any]] = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CatalogSyncRun(BaseModel):
    """Catalog synchronization run record."""
    id: UUID = Field(default_factory=uuid4)
    provider_id: UUID
    started_at: datetime
    finished_at: Optional[datetime] = None
    status: str  # RUNNING, COMPLETED, FAILED
    collections_discovered: int = 0
    collections_updated: int = 0
    missions_discovered: int = 0
    spacecraft_discovered: int = 0
    services_discovered: int = 0
    errors: list[dict[str, Any]] = Field(default_factory=list)
    provider_cursor: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)
