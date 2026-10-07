"""Live data API routes."""

from typing import Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from packages.live.models import LiveEntity, EntityType, FreshnessState
from packages.live.providers import (
    AircraftProvider, MilitaryAircraftProvider, VesselProvider,
    SatelliteProvider, EarthquakeProvider, FireProvider
)
from packages.live.tracking import EntityTracker, SelectionState
from packages.live.demo_fixtures import get_all_demo_entities
from packages.orbital.tle_parser import TLEParser
from packages.orbital.propagation import SatellitePropagator
from packages.orbital.pass_prediction import PassPredictor

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

# Demo mode flag - can be toggled via API
DEMO_MODE = False

def set_demo_mode(enabled: bool):
    """Enable or disable demo mode."""
    global DEMO_MODE
    DEMO_MODE = enabled

def is_demo_mode() -> bool:
    """Check if demo mode is enabled."""
    return DEMO_MODE


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
    altitude: float = Query(0.0, description="Observer altitude in meters"),
    norad_id: int = Query(..., description="NORAD ID of satellite"),
    hours: int = Query(24, ge=1, le=168, description="Prediction window in hours"),
    min_elevation: float = Query(10.0, ge=0, le=90, description="Minimum elevation in degrees")
):
    """Predict next satellite pass over a location using real SGP4 propagation."""
    try:
        # Fetch TLE data for the satellite
        tle_data = await satellite_provider.fetch_tle_for_satellite(norad_id)
        
        if not tle_data:
            raise HTTPException(
                status_code=404,
                detail=f"TLE data not found for NORAD ID {norad_id}"
            )
        
        # Parse TLE
        tles = TLEParser.parse(tle_data)
        if not tles:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to parse TLE for NORAD ID {norad_id}"
            )
        
        tle = tles[0]
        
        # Create propagator and pass predictor
        propagator = SatellitePropagator(tle)
        predictor = PassPredictor(propagator)
        
        # Predict next pass
        next_pass = predictor.predict_next_pass(
            observer_lat=latitude,
            observer_lon=longitude,
            observer_alt_m=altitude,
            min_elevation_deg=min_elevation
        )
        
        if not next_pass:
            return {
                "norad_id": norad_id,
                "satellite_name": tle.name,
                "status": "no_pass_predicted",
                "message": f"No pass found within {hours} hours with minimum elevation {min_elevation}°",
                "observer": {
                    "latitude": latitude,
                    "longitude": longitude,
                    "altitude_m": altitude
                },
                "tle_epoch": tle.epoch_datetime.isoformat(),
                "prediction_time": datetime.utcnow().isoformat()
            }
        
        return {
            "norad_id": norad_id,
            "satellite_name": tle.name,
            "status": "pass_predicted",
            "rise_time": next_pass['rise_time'].isoformat(),
            "rise_azimuth_deg": next_pass['rise_azimuth_deg'],
            "culmination_time": next_pass['culmination_time'].isoformat(),
            "culmination_elevation_deg": next_pass['culmination_elevation_deg'],
            "culmination_azimuth_deg": next_pass['culmination_azimuth_deg'],
            "set_time": next_pass['set_time'].isoformat(),
            "set_azimuth_deg": next_pass['set_azimuth_deg'],
            "max_elevation_deg": next_pass['max_elevation_deg'],
            "duration_seconds": next_pass['duration_seconds'],
            "observer": {
                "latitude": latitude,
                "longitude": longitude,
                "altitude_m": altitude
            },
            "tle_epoch": tle.epoch_datetime.isoformat(),
            "prediction_time": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Pass prediction failed: {str(e)}"
        )


# Demo mode endpoints
@router.post("/demo/enable")
async def enable_demo_mode():
    """Enable demo mode with deterministic fixtures."""
    set_demo_mode(True)
    return {"status": "demo_mode_enabled", "message": "Demo mode activated. Using deterministic fixtures."}


@router.post("/demo/disable")
async def disable_demo_mode():
    """Disable demo mode and return to live data."""
    set_demo_mode(False)
    return {"status": "demo_mode_disabled", "message": "Demo mode deactivated. Using live data."}


@router.get("/demo/status")
async def get_demo_status():
    """Get current demo mode status."""
    return {
        "demo_mode": is_demo_mode(),
        "message": "DEMO DATA" if is_demo_mode() else "LIVE DATA"
    }


# Update existing endpoints to support demo mode
@router.get("/aircraft", response_model=list[EntityResponse])
async def get_aircraft(
    bbox: Optional[str] = Query(None, description="Bounding box: min_lon,min_lat,max_lon,max_lat"),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get live aircraft data."""
    if is_demo_mode():
        demo_data = get_all_demo_entities()
        return [entity_to_response(e) for e in demo_data["aircraft"][:limit]]
    
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
    if is_demo_mode():
        demo_data = get_all_demo_entities()
        return [entity_to_response(e) for e in demo_data["military_aircraft"][:limit]]
    
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
    if is_demo_mode():
        demo_data = get_all_demo_entities()
        return [entity_to_response(e) for e in demo_data["vessels"][:limit]]
    
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
    if is_demo_mode():
        demo_data = get_all_demo_entities()
        return [entity_to_response(e) for e in demo_data["satellites"][:limit]]
    
    entities = await satellite_provider.fetch(group=group, limit=limit)
    return [entity_to_response(e) for e in entities]


@router.get("/earthquakes", response_model=list[EntityResponse])
async def get_earthquakes(
    days: int = Query(7, ge=1, le=30, description="Time window in days"),
    min_magnitude: float = Query(2.5, ge=0.0, le=10.0, description="Minimum magnitude"),
    limit: int = Query(100, ge=1, le=500)
):
    """Get recent earthquake data."""
    if is_demo_mode():
        demo_data = get_all_demo_entities()
        return [entity_to_response(e) for e in demo_data["earthquakes"][:limit]]
    
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
    if is_demo_mode():
        demo_data = get_all_demo_entities()
        return [entity_to_response(e) for e in demo_data["fires"][:limit]]
    
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
