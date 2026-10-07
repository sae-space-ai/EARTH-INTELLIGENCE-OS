"""Live entity models and enums."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class EntityType(str, Enum):
    """Types of live entities."""
    AIRCRAFT = "AIRCRAFT"
    MILITARY_AIRCRAFT = "MILITARY_AIRCRAFT"
    VESSEL = "VESSEL"
    SATELLITE = "SATELLITE"
    EARTHQUAKE = "EARTHQUAKE"
    FIRE_DETECTION = "FIRE_DETECTION"


class FreshnessState(str, Enum):
    """Freshness states for live data."""
    LIVE = "LIVE"
    DELAYED = "DELAYED"
    STALE = "STALE"
    UNAVAILABLE = "UNAVAILABLE"
    PARTIAL = "PARTIAL"


class KnowledgeState(str, Enum):
    """Knowledge state for entity data."""
    OBSERVED = "OBSERVED"
    INFERRED = "INFERRED"
    FORECAST = "FORECAST"
    SIMULATED = "SIMULATED"


class LiveEntity(BaseModel):
    """Canonical live entity model."""
    
    id: UUID = Field(default_factory=uuid4)
    entity_type: EntityType
    provider: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    altitude: Optional[float] = None  # meters
    heading: Optional[float] = None  # degrees
    speed: Optional[float] = None  # m/s
    observed_at: datetime
    retrieved_at: datetime = Field(default_factory=datetime.utcnow)
    freshness: FreshnessState = FreshnessState.LIVE
    knowledge_state: KnowledgeState = KnowledgeState.OBSERVED
    metadata: dict[str, Any] = Field(default_factory=dict)
    
    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, v: float) -> float:
        """Validate longitude is within valid range."""
        if not -180 <= v <= 180:
            raise ValueError(f"Longitude must be between -180 and 180, got {v}")
        return v
    
    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, v: float) -> float:
        """Validate latitude is within valid range."""
        if not -90 <= v <= 90:
            raise ValueError(f"Latitude must be between -90 and 90, got {v}")
        return v
    
    def calculate_freshness(self, thresholds: Optional[dict[str, float]] = None) -> FreshnessState:
        """Calculate freshness based on observed_at timestamp.
        
        Args:
            thresholds: Optional dict mapping FreshnessState to max age in seconds.
                       Defaults to entity-type-specific thresholds.
        
        Returns:
            Calculated FreshnessState.
        """
        if thresholds is None:
            # Default thresholds by entity type
            thresholds = {
                EntityType.AIRCRAFT: {"LIVE": 30, "DELAYED": 300},
                EntityType.MILITARY_AIRCRAFT: {"LIVE": 60, "DELAYED": 600},
                EntityType.VESSEL: {"LIVE": 300, "DELAYED": 1800},
                EntityType.SATELLITE: {"LIVE": 3600, "DELAYED": 86400},
                EntityType.EARTHQUAKE: {"LIVE": 300, "DELAYED": 3600},
                EntityType.FIRE_DETECTION: {"LIVE": 600, "DELAYED": 3600},
            }.get(self.entity_type, {"LIVE": 300, "DELAYED": 3600})
        
        age_seconds = (datetime.utcnow() - self.observed_at).total_seconds()
        
        if age_seconds <= thresholds.get("LIVE", 300):
            return FreshnessState.LIVE
        elif age_seconds <= thresholds.get("DELAYED", 3600):
            return FreshnessState.DELAYED
        else:
            return FreshnessState.STALE


class AircraftEntity(LiveEntity):
    """Aircraft-specific entity with aviation metadata."""
    
    entity_type: EntityType = EntityType.AIRCRAFT
    icao24: Optional[str] = None
    callsign: Optional[str] = None
    registration: Optional[str] = None
    aircraft_type: Optional[str] = None
    ground_speed: Optional[float] = None  # m/s
    vertical_rate: Optional[float] = None  # m/s
    squawk: Optional[str] = None
    
    @field_validator("icao24")
    @classmethod
    def validate_icao24(cls, v: Optional[str]) -> Optional[str]:
        """Validate ICAO24 address format (6 hex chars)."""
        if v is not None and len(v) != 6:
            raise ValueError(f"ICAO24 must be 6 hex characters, got {v}")
        return v


class MilitaryAircraftEntity(LiveEntity):
    """Military aircraft entity with public ADS-B data."""
    
    entity_type: EntityType = EntityType.MILITARY_AIRCRAFT
    icao24: Optional[str] = None
    callsign: Optional[str] = None
    aircraft_type: Optional[str] = None
    ground_speed: Optional[float] = None
    vertical_rate: Optional[float] = None
    classification_source: str = "PUBLIC_ADS_B"


class VesselEntity(LiveEntity):
    """Vessel entity with maritime metadata."""
    
    entity_type: EntityType = EntityType.VESSEL
    mmsi: Optional[int] = None
    name: Optional[str] = None
    ship_type: Optional[str] = None
    course: Optional[float] = None  # degrees
    destination: Optional[str] = None
    navigation_status: Optional[str] = None
    
    @field_validator("mmsi")
    @classmethod
    def validate_mmsi(cls, v: Optional[int]) -> Optional[int]:
        """Validate MMSI is 9 digits."""
        if v is not None and not (100000000 <= v <= 999999999):
            raise ValueError(f"MMSI must be 9 digits, got {v}")
        return v


class SatelliteEntity(LiveEntity):
    """Satellite entity with orbital metadata."""
    
    entity_type: EntityType = EntityType.SATELLITE
    norad_id: Optional[int] = None
    name: Optional[str] = None
    mission: Optional[str] = None
    orbit_class: Optional[str] = None  # LEO, MEO, GEO
    element_epoch: Optional[datetime] = None
    orbital_elements_source: Optional[str] = None
    is_propagated: bool = False  # True if position is propagated, not observed
    
    @field_validator("knowledge_state")
    @classmethod
    def validate_knowledge_state(cls, v: KnowledgeState, info: Any) -> KnowledgeState:
        """Validate knowledge state for satellites."""
        # Propagated positions should be INFERRED, not OBSERVED
        if info.data.get("is_propagated", False) and v == KnowledgeState.OBSERVED:
            return KnowledgeState.INFERRED
        return v


class EarthquakeEntity(LiveEntity):
    """Earthquake entity with seismic metadata."""
    
    entity_type: EntityType = EntityType.EARTHQUAKE
    event_id: str
    magnitude: float
    depth_km: float
    place: Optional[str] = None
    source_url: Optional[str] = None
    updated_at: Optional[datetime] = None


class FireDetectionEntity(LiveEntity):
    """Fire detection entity with remote sensing metadata."""
    
    entity_type: EntityType = EntityType.FIRE_DETECTION
    satellite: Optional[str] = None
    instrument: Optional[str] = None
    confidence: Optional[str] = None  # low, nominal, high
    frp: Optional[float] = None  # Fire Radiative Power (MW)
    acquisition_time: Optional[datetime] = None
