"""Live data API routes."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from packages.live.models import LiveEntity, EntityType, FreshnessState
from packages.live.providers import (
    AircraftProvider, MilitaryAircraftProvider, VesselProvider,
    SatelliteProvider, EarthquakeProvider, FireProvider
)
from packages.live.tracking import EntityTracker, SelectionState

router = APIRouter(prefix="/api/v1/live", tags=["Live Data"])

# Initialize providers
aircraft_provider = AircraftProvider()
military_provider = MilitaryAircraftProvider()
vessel_provider = VesselProvider()
satellite_provider = SatelliteProvider()
earthquake_provider = EarthquakeProvider()
fire_provider = FireProvider()

# Initialize tracking
tracker = EntityTracker()
selection = SelectionState()


class EntityResponse(BaseModel):
    """API response model for live entities."""
    id: str
    entity_type: str
    provider: str
    latitude: float
    longitude: float
    altitude: Optional[float]
    heading: Optional[float]
    speed: Optional[float]
    observed_at: str
    retrieved_at: str
    freshness: str
    knowledge_state: str
    metadata: dict


class ProviderHealthResponse(BaseModel):
    """API response for provider health."""
    provider: str
    state: str
    last_success: Optional[str]
    last_error: Optional[str]


class PassPredictionResponse(BaseModel):
    """API response for satellite pass prediction."""
    satellite: str
    norad_id: int
    rise_time: str
    culmination_time: str
    set_time: str
    max_elevation: float
    source_epoch: str


def entity_to_response(entity: LiveEntity) -> EntityResponse:
    """Convert LiveEntity to API response."""
    return EntityResponse(
        id=str(entity.id),
        entity_type=entity.entity_type.value,
        provider=entity.provider,
        latitude=entity.latitude,
        longitude=entity.longitude,
        altitude=entity.altitude,
        heading=entity.heading,
        speed=entity.speed,
        observed_at=entity.observed_at.isoformat(),
        retrieved_at=entity.retrieved_at.isoformat(),
        freshness=entity.freshness.value,
        knowledge_state=entity.knowledge_state.value,
        metadata=entity.metadata
    )


@router.get("/aircraft", response_model=list[EntityResponse])
async def get_aircraft(
    bbox: Optional[str] = Query(None, description="Bounding box: min_lon,min_lat,max_lon,max_lat"),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get live aircraft data."""
    bbox_tuple = None
    if bbox:
        try:
            parts = [float(x.strip()) for x in bbox.split(",")]
            if len(parts) == 4:
                bbox_tuple = tuple(parts)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid bbox format")
    
    entities = await aircraft_provider.fetch(bbox=bbox_tuple, limit=limit)
    return [entity_to_response(e) for e in entities]


@router.get("/military-aircraft", response_model=list[EntityResponse])
async def get_military_aircraft(
    bbox: Optional[str] = Query(None, description="Bounding box: min_lon,min_lat,max_lon,max_lat"),
    limit: int = Query(100, ge=1, le=500)
):
    """Get public military ADS-B aircraft data."""
    bbox_tuple = None
    if bbox:
        try:
            parts = [float(x.strip()) for x in bbox.split(",")]
            if len(parts) == 4:
                bbox_tuple = tuple(parts)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid bbox format")
    
    entities = await military_provider.fetch(bbox=bbox_tuple, limit=limit)
    return [entity_to_response(e) for e in entities]


@router.get("/vessels", response_model=list[EntityResponse])
async def get_vessels(
    bbox: Optional[str] = Query(None, description="Bounding box: min_lon,min_lat,max_lon,max_lat"),
    limit: int = Query(100, ge=1, le=500)
):
    """Get live vessel data."""
    bbox_tuple = None
    if bbox:
        try:
            parts = [float(x.strip()) for x in bbox.split(",")]
            if len(parts) == 4:
                bbox_tuple = tuple(parts)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid bbox format")
    
    entities = await vessel_provider.fetch(bbox=bbox_tuple, limit=limit)
    return [entity_to_response(e) for e in entities]


@router.get("/satellites", response_model=list[EntityResponse])
async def get_satellites(
    group: str = Query("stations", description="Satellite group: stations, weather, noaa, etc."),
    limit: int = Query(50, ge=1, le=200)
):
    """Get satellite positions from TLE data."""
    entities = await satellite_provider.fetch(group=group, limit=limit)
    return [entity_to_response(e) for e in entities]


@router.get("/earthquakes", response_model=list[EntityResponse])
async def get_earthquakes(
    days: int = Query(7, ge=1, le=30, description="Time window in days"),
    min_magnitude: float = Query(2.5, ge=0.0, le=10.0, description="Minimum magnitude"),
    limit: int = Query(100, ge=1, le=500)
):
    """Get recent earthquake data."""
    entities = await earthquake_provider.fetch(days=days, min_magnitude=min_magnitude, limit=limit)
    return [entity_to_response(e) for e in entities]


@router.get("/fires", response_model=list[EntityResponse])
async def get_fires(
    days: int = Query(1, ge=1, le=7, description="Time window in days"),
    source: str = Query("VIIRS_SNPP_NRT", description="Fire data source"),
    bbox: Optional[str] = Query(None, description="Bounding box: min_lon,min_lat,max_lon,max_lat"),
    limit: int = Query(500, ge=1, le=2000)
):
    """Get active fire detection data."""
    bbox_tuple = None
    if bbox:
        try:
            parts = [float(x.strip()) for x in bbox.split(",")]
            if len(parts) == 4:
                bbox_tuple = tuple(parts)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid bbox format")
    
    entities = await fire_provider.fetch(days=days, source=source, bbox=bbox_tuple, limit=limit)
    return [entity_to_response(e) for e in entities]


@router.get("/provider-health", response_model=list[ProviderHealthResponse])
async def get_provider_health():
    """Get health status of all live data providers."""
    providers = [
        aircraft_provider,
        military_provider,
        vessel_provider,
        satellite_provider,
        earthquake_provider,
        fire_provider
    ]
    return [ProviderHealthResponse(**p.health()) for p in providers]


@router.post("/track/{entity_id}")
async def track_entity(entity_id: UUID):
    """Start tracking an entity."""
    # In a real implementation, would look up entity from cache/database
    # For now, return success
    return {"status": "tracking", "entity_id": str(entity_id)}


@router.delete("/track/{entity_id}")
async def untrack_entity(entity_id: UUID):
    """Stop tracking an entity."""
    return {"status": "untracked", "entity_id": str(entity_id)}


@router.post("/select/{entity_id}")
async def select_entity(entity_id: UUID):
    """Select an entity for detailed view."""
    return {"status": "selected", "entity_id": str(entity_id)}


@router.delete("/select")
async def deselect_entity():
    """Deselect current entity."""
    return {"status": "deselected"}


@router.get("/trail/{entity_id}")
async def get_entity_trail(entity_id: UUID):
    """Get trail history for a tracked entity."""
    trail = tracker.get_trail(entity_id)
    return {
        "entity_id": str(entity_id),
        "points": [
            {
                "latitude": p.latitude,
                "longitude": p.longitude,
                "altitude": p.altitude,
                "timestamp": p.timestamp.isoformat()
            }
            for p in trail
        ]
    }


@router.post("/satellites/pass")
async def predict_satellite_pass(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    norad_id: int = Query(..., description="NORAD ID of satellite")
):
    """Predict next satellite pass over a location."""
    # Placeholder implementation - real implementation would use SGP4
    from datetime import datetime, timedelta
    
    # Mock prediction
    now = datetime.utcnow()
    rise_time = now + timedelta(hours=2)
    culmination_time = rise_time + timedelta(minutes=5)
    set_time = culmination_time + timedelta(minutes=5)
    
    return PassPredictionResponse(
        satellite=f"Satellite {norad_id}",
        norad_id=norad_id,
        rise_time=rise_time.isoformat(),
        culmination_time=culmination_time.isoformat(),
        set_time=set_time.isoformat(),
        max_elevation=45.0,
        source_epoch=now.isoformat()
    )
