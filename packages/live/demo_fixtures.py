"""Demo mode fixtures for testing without live providers."""

from datetime import datetime, timedelta
from uuid import uuid4

from packages.live.models import (
    AircraftEntity, MilitaryAircraftEntity, VesselEntity,
    SatelliteEntity, EarthquakeEntity, FireDetectionEntity,
    EntityType, KnowledgeState, FreshnessState
)


def get_demo_aircraft() -> list[AircraftEntity]:
    """Generate demo aircraft data."""
    now = datetime.utcnow()
    
    return [
        AircraftEntity(
            entity_type=EntityType.AIRCRAFT,
            provider="DEMO",
            latitude=37.7749,
            longitude=-122.4194,
            altitude=10000,
            heading=90,
            speed=250,
            observed_at=now - timedelta(seconds=30),
            icao24="A1B2C3",
            callsign="DEMO001",
            registration="N12345",
            aircraft_type="B738",
            metadata={"country": "United States", "on_ground": False}
        ),
        AircraftEntity(
            entity_type=EntityType.AIRCRAFT,
            provider="DEMO",
            latitude=40.7128,
            longitude=-74.0060,
            altitude=8000,
            heading=180,
            speed=220,
            observed_at=now - timedelta(seconds=45),
            icao24="D4E5F6",
            callsign="DEMO002",
            registration="G-EUPA",
            aircraft_type="A320",
            metadata={"country": "United Kingdom", "on_ground": False}
        ),
        AircraftEntity(
            entity_type=EntityType.AIRCRAFT,
            provider="DEMO",
            latitude=51.5074,
            longitude=-0.1278,
            altitude=12000,
            heading=270,
            speed=280,
            observed_at=now - timedelta(seconds=60),
            icao24="789ABC",
            callsign="DEMO003",
            registration="F-GSPZ",
            aircraft_type="B77W",
            metadata={"country": "France", "on_ground": False}
        ),
    ]


def get_demo_military_aircraft() -> list[MilitaryAircraftEntity]:
    """Generate demo military aircraft data."""
    now = datetime.utcnow()
    
    return [
        MilitaryAircraftEntity(
            entity_type=EntityType.MILITARY_AIRCRAFT,
            provider="DEMO",
            latitude=38.8977,
            longitude=-77.0365,
            altitude=15000,
            heading=45,
            speed=300,
            observed_at=now - timedelta(seconds=90),
            icao24="AE1234",
            callsign="DUKE01",
            aircraft_type="C17",
            classification_source="PUBLIC_ADS_B",
            metadata={"squawk": "7700", "category": "A3"}
        ),
    ]


def get_demo_vessels() -> list[VesselEntity]:
    """Generate demo vessel data."""
    now = datetime.utcnow()
    
    return [
        VesselEntity(
            entity_type=EntityType.VESSEL,
            provider="DEMO",
            latitude=34.0522,
            longitude=-118.2437,
            speed=15,
            heading=180,
            observed_at=now - timedelta(minutes=2),
            mmsi=366789012,
            name="DEMO CONTAINER",
            ship_type="Cargo",
            course=180,
            destination="US LAX",
            navigation_status="Under way using engine",
            metadata={"length": 200, "flag": "Panama"}
        ),
        VesselEntity(
            entity_type=EntityType.VESSEL,
            provider="DEMO",
            latitude=51.9244,
            longitude=4.4777,
            speed=12,
            heading=90,
            observed_at=now - timedelta(minutes=3),
            mmsi=244760123,
            name="DEMO TANKER",
            ship_type="Tanker",
            course=90,
            destination="NL RTM",
            navigation_status="Under way using engine",
            metadata={"length": 180, "flag": "Netherlands"}
        ),
    ]


def get_demo_satellites() -> list[SatelliteEntity]:
    """Generate demo satellite data with real orbital elements."""
    now = datetime.utcnow()
    
    # ISS - real TLE data (example)
    iss_tle = """ISS (ZARYA)
1 25544U 98067A   24001.50000000  .00016717  00000-0  10270-3 0  9993
2 25544  51.6400 200.0000 0001234  90.0000 270.0000 15.49000000100001"""
    
    from packages.orbital.tle_parser import TLEParser
    from packages.orbital.propagation import SatellitePropagator
    
    satellites = []
    
    try:
        tles = TLEParser.parse(iss_tle)
        if tles:
            tle = tles[0]
            propagator = SatellitePropagator(tle)
            position = propagator.propagate()
            
            satellites.append(SatelliteEntity(
                entity_type=EntityType.SATELLITE,
                provider="DEMO",
                latitude=position['latitude_deg'],
                longitude=position['longitude_deg'],
                altitude=position['altitude_m'],
                observed_at=position['datetime'],
                norad_id=tle.norad_id,
                name=tle.name,
                orbit_class=propagator.orbit_type,
                element_epoch=tle.epoch_datetime,
                orbital_elements_source="DEMO TLE",
                is_propagated=True,
                knowledge_state=KnowledgeState.INFERRED,
                metadata={
                    'mean_motion': tle.mean_motion,
                    'inclination': tle.inclination,
                    'orbital_period_minutes': propagator.orbital_period_minutes,
                }
            ))
    except Exception:
        pass
    
    # Add more demo satellites
    for i, (name, norad_id) in enumerate([
        ("STARLINK-1234", 50000 + i) for i in range(3)
    ]):
        satellites.append(SatelliteEntity(
            entity_type=EntityType.SATELLITE,
            provider="DEMO",
            latitude=45.0 + i * 10,
            longitude=-100.0 + i * 20,
            altitude=550000,
            observed_at=now - timedelta(minutes=5),
            norad_id=norad_id,
            name=name,
            orbit_class="LEO",
            element_epoch=now - timedelta(days=1),
            orbital_elements_source="DEMO",
            is_propagated=True,
            knowledge_state=KnowledgeState.INFERRED,
            metadata={'demo': True}
        ))
    
    return satellites


def get_demo_earthquakes() -> list[EarthquakeEntity]:
    """Generate demo earthquake data."""
    now = datetime.utcnow()
    
    return [
        EarthquakeEntity(
            entity_type=EntityType.EARTHQUAKE,
            provider="DEMO",
            latitude=35.6762,
            longitude=139.6503,
            altitude=-10000,
            observed_at=now - timedelta(hours=2),
            event_id="demo_eq_001",
            magnitude=5.2,
            depth_km=10,
            place="Tokyo, Japan",
            source_url="https://earthquake.usgs.gov/earthquakes/eventpage/demo_eq_001",
            metadata={"type": "earthquake", "status": "reviewed"}
        ),
        EarthquakeEntity(
            entity_type=EntityType.EARTHQUAKE,
            provider="DEMO",
            latitude=34.0522,
            longitude=-118.2437,
            altitude=-5000,
            observed_at=now - timedelta(hours=5),
            event_id="demo_eq_002",
            magnitude=3.8,
            depth_km=5,
            place="Los Angeles, California",
            source_url="https://earthquake.usgs.gov/earthquakes/eventpage/demo_eq_002",
            metadata={"type": "earthquake", "status": "automatic"}
        ),
        EarthquakeEntity(
            entity_type=EntityType.EARTHQUAKE,
            provider="DEMO",
            latitude=-33.4489,
            longitude=-70.6693,
            altitude=-15000,
            observed_at=now - timedelta(hours=8),
            event_id="demo_eq_003",
            magnitude=6.1,
            depth_km=15,
            place="Santiago, Chile",
            source_url="https://earthquake.usgs.gov/earthquakes/eventpage/demo_eq_003",
            metadata={"type": "earthquake", "status": "reviewed", "tsunami": False}
        ),
    ]


def get_demo_fires() -> list[FireDetectionEntity]:
    """Generate demo fire detection data."""
    now = datetime.utcnow()
    
    return [
        FireDetectionEntity(
            entity_type=EntityType.FIRE_DETECTION,
            provider="DEMO",
            latitude=37.7749,
            longitude=-122.4194,
            observed_at=now - timedelta(minutes=30),
            satellite="Suomi-NPP",
            instrument="VIIRS",
            confidence="high",
            frp=15.5,
            metadata={"daynight": "D", "demo": True}
        ),
        FireDetectionEntity(
            entity_type=EntityType.FIRE_DETECTION,
            provider="DEMO",
            latitude=-33.8688,
            longitude=151.2093,
            observed_at=now - timedelta(minutes=45),
            satellite="NOAA-20",
            instrument="VIIRS",
            confidence="nominal",
            frp=8.2,
            metadata={"daynight": "D", "demo": True}
        ),
        FireDetectionEntity(
            entity_type=EntityType.FIRE_DETECTION,
            provider="DEMO",
            latitude=55.7558,
            longitude=37.6176,
            observed_at=now - timedelta(hours=1),
            satellite="Terra",
            instrument="MODIS",
            confidence="low",
            frp=3.1,
            metadata={"daynight": "N", "demo": True}
        ),
        FireDetectionEntity(
            entity_type=EntityType.FIRE_DETECTION,
            provider="DEMO",
            latitude=-23.5505,
            longitude=-46.6333,
            observed_at=now - timedelta(hours=2),
            satellite="Aqua",
            instrument="MODIS",
            confidence="nominal",
            frp=12.7,
            metadata={"daynight": "D", "demo": True}
        ),
        FireDetectionEntity(
            entity_type=EntityType.FIRE_DETECTION,
            provider="DEMO",
            latitude=28.6139,
            longitude=77.2090,
            observed_at=now - timedelta(hours=3),
            satellite="Suomi-NPP",
            instrument="VIIRS",
            confidence="high",
            frp=22.3,
            metadata={"daynight": "D", "demo": True}
        ),
    ]


def get_all_demo_entities() -> dict[str, list]:
    """Get all demo entities grouped by type."""
    return {
        "aircraft": get_demo_aircraft(),
        "military_aircraft": get_demo_military_aircraft(),
        "vessels": get_demo_vessels(),
        "satellites": get_demo_satellites(),
        "earthquakes": get_demo_earthquakes(),
        "fires": get_demo_fires(),
    }
