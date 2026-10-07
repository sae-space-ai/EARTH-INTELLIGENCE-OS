"""Provider adapter interfaces and implementations."""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Optional
import httpx
from packages.live.models import (
    LiveEntity, AircraftEntity, MilitaryAircraftEntity, VesselEntity,
    SatelliteEntity, EarthquakeEntity, FireDetectionEntity,
    FreshnessState, KnowledgeState, EntityType
)


class ProviderHealthState:
    """Provider health states."""
    AVAILABLE = "AVAILABLE"
    DEGRADED = "DEGRADED"
    AUTH_REQUIRED = "AUTH_REQUIRED"
    RATE_LIMITED = "RATE_LIMITED"
    UNAVAILABLE = "UNAVAILABLE"
    NOT_CONFIGURED = "NOT_CONFIGURED"


class BaseProvider(ABC):
    """Base provider interface for live data sources."""
    
    def __init__(self, name: str, base_url: Optional[str] = None):
        self.name = name
        self.base_url = base_url
        self.health_state = ProviderHealthState.NOT_CONFIGURED
        self.last_error: Optional[str] = None
        self.last_success: Optional[datetime] = None
    
    @abstractmethod
    async def fetch(self, **kwargs) -> list[LiveEntity]:
        """Fetch live entities from provider."""
        pass
    
    @abstractmethod
    def normalize(self, raw_data: Any) -> list[LiveEntity]:
        """Normalize raw provider data to LiveEntity models."""
        pass
    
    def health(self) -> dict[str, Any]:
        """Return provider health status."""
        return {
            "provider": self.name,
            "state": self.health_state,
            "last_success": self.last_success.isoformat() if self.last_success else None,
            "last_error": self.last_error,
        }
    
    async def _http_get(self, url: str, params: Optional[dict] = None, 
                        timeout: float = 10.0) -> Optional[dict]:
        """Perform HTTP GET with error handling."""
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                self.last_success = datetime.utcnow()
                self.last_error = None
                return response.json()
        except httpx.TimeoutException:
            self.health_state = ProviderHealthState.UNAVAILABLE
            self.last_error = "Request timeout"
            return None
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                self.health_state = ProviderHealthState.RATE_LIMITED
                self.last_error = "Rate limited"
            elif e.response.status_code in (401, 403):
                self.health_state = ProviderHealthState.AUTH_REQUIRED
                self.last_error = "Authentication required"
            else:
                self.health_state = ProviderHealthState.UNAVAILABLE
                self.last_error = f"HTTP {e.response.status_code}"
            return None
        except Exception as e:
            self.health_state = ProviderHealthState.UNAVAILABLE
            self.last_error = str(e)
            return None


class AircraftProvider(BaseProvider):
    """Provider for civil aircraft tracking (OpenSky Network)."""
    
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        super().__init__("OpenSky Network", "https://opensky-network.org/api")
        self.username = username
        self.password = password
        if username and password:
            self.health_state = ProviderHealthState.AVAILABLE
        else:
            self.health_state = ProviderHealthState.AUTH_REQUIRED
    
    async def fetch(self, bbox: Optional[tuple[float, float, float, float]] = None,
                    limit: int = 1000) -> list[LiveEntity]:
        """Fetch aircraft from OpenSky Network."""
        if self.health_state == ProviderHealthState.AUTH_REQUIRED:
            return []
        
        params = {}
        if bbox:
            # OpenSky uses lamin, lomin, lamax, lomax
            params["lamin"] = bbox[1]  # min lat
            params["lomin"] = bbox[0]  # min lon
            params["lamax"] = bbox[3]  # max lat
            params["lomax"] = bbox[2]  # max lon
        
        url = f"{self.base_url}/states/all"
        data = await self._http_get(url, params=params)
        
        if data is None:
            return []
        
        return self.normalize(data)[:limit]
    
    def normalize(self, raw_data: dict) -> list[AircraftEntity]:
        """Normalize OpenSky states to AircraftEntity."""
        entities = []
        states = raw_data.get("states", [])
        
        for state in states:
            if len(state) < 17:
                continue
            
            icao24 = state[0]
            callsign = state[1].strip() if state[1] else None
            country = state[2]
            lon = state[5]
            lat = state[6]
            altitude = state[7]  # geometric altitude
            ground = state[8]
            speed = state[9]  # ground speed
            heading = state[10]  # true track
            vertical_rate = state[11]  # vertical rate
            squawk = state[14]
            timestamp = state[13]  # last contact
            
            if lon is None or lat is None:
                continue
            
            try:
                observed_at = datetime.utcfromtimestamp(timestamp) if timestamp else datetime.utcnow()
            except (ValueError, TypeError):
                observed_at = datetime.utcnow()
            
            entity = AircraftEntity(
                entity_type=EntityType.AIRCRAFT,
                provider=self.name,
                latitude=lat,
                longitude=lon,
                altitude=altitude,
                heading=heading,
                speed=speed,
                observed_at=observed_at,
                icao24=icao24,
                callsign=callsign,
                ground_speed=speed if ground else None,
                vertical_rate=vertical_rate,
                squawk=str(squawk) if squawk else None,
                metadata={"country": country, "on_ground": ground}
            )
            entity.freshness = entity.calculate_freshness()
            entities.append(entity)
        
        return entities


class MilitaryAircraftProvider(BaseProvider):
    """Provider for public military ADS-B data (adsb.lol)."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__("adsb.lol", "https://api.adsb.lol")
        self.api_key = api_key
        # adsb.lol is free and doesn't require API key for basic access
        self.health_state = ProviderHealthState.AVAILABLE
    
    async def fetch(self, bbox: Optional[tuple[float, float, float, float]] = None,
                    limit: int = 500) -> list[LiveEntity]:
        """Fetch military aircraft from adsb.lol."""
        params = {}
        if bbox:
            # adsb.lol uses lat, lon, dist for radius search
            center_lat = (bbox[1] + bbox[3]) / 2
            center_lon = (bbox[0] + bbox[2]) / 2
            # Calculate approximate distance in miles
            lat_diff = abs(bbox[3] - bbox[1])
            lon_diff = abs(bbox[2] - bbox[0])
            dist_miles = max(lat_diff, lon_diff) * 69  # rough conversion
            params["lat"] = center_lat
            params["lon"] = center_lon
            params["dist"] = min(dist_miles, 250)  # max 250 miles
        
        url = f"{self.base_url}/v2/aircraft"
        data = await self._http_get(url, params=params)
        
        if data is None:
            return []
        
        return self.normalize(data)[:limit]
    
    def normalize(self, raw_data: dict) -> list[MilitaryAircraftEntity]:
        """Normalize adsb.lol data to MilitaryAircraftEntity."""
        entities = []
        aircraft_list = raw_data.get("ac", [])
        
        for ac in aircraft_list:
            # Filter for military aircraft (hex starts with specific ranges)
            # This is a simplified check - real implementation would check ICAO ranges
            icao = ac.get("hex", "").upper()
            if not icao:
                continue
            
            lat = ac.get("lat")
            lon = ac.get("lon")
            
            if lat is None or lon is None:
                continue
            
            # Parse timestamp
            seen = ac.get("seen", 0)
            observed_at = datetime.utcnow() - timedelta(seconds=seen)
            
            entity = MilitaryAircraftEntity(
                entity_type=EntityType.MILITARY_AIRCRAFT,
                provider=self.name,
                latitude=lat,
                longitude=lon,
                altitude=ac.get("alt_baro"),
                heading=ac.get("track"),
                speed=ac.get("gs"),
                observed_at=observed_at,
                icao24=icao,
                callsign=ac.get("flight", "").strip() or None,
                aircraft_type=ac.get("t"),
                ground_speed=ac.get("gs") if ac.get("alt_baro") == "ground" else None,
                vertical_rate=ac.get("baro_rate"),
                metadata={"squawk": ac.get("squawk"), "category": ac.get("category")}
            )
            entity.freshness = entity.calculate_freshness()
            entities.append(entity)
        
        return entities


class VesselProvider(BaseProvider):
    """Provider for vessel tracking (AISStream)."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__("AISStream", "https://stream.aisstream.io")
        self.api_key = api_key
        if api_key:
            self.health_state = ProviderHealthState.AVAILABLE
        else:
            self.health_state = ProviderHealthState.AUTH_REQUIRED
    
    async def fetch(self, bbox: Optional[tuple[float, float, float, float]] = None,
                    limit: int = 500) -> list[LiveEntity]:
        """Fetch vessels from AISStream."""
        if self.health_state == ProviderHealthState.AUTH_REQUIRED:
            return []
        
        # AISStream uses WebSocket for real-time, but we'll use REST API if available
        # For now, return empty list as AISStream requires WebSocket connection
        # TODO: Implement WebSocket client for real-time AIS data
        return []
    
    def normalize(self, raw_data: Any) -> list[VesselEntity]:
        """Normalize AISStream data to VesselEntity."""
        # Placeholder for when WebSocket implementation is added
        return []


class SatelliteProvider(BaseProvider):
    """Provider for satellite tracking (CelesTrak TLE)."""
    
    def __init__(self):
        super().__init__("CelesTrak", "https://celestrak.org")
        self.health_state = ProviderHealthState.AVAILABLE
    
    async def fetch(self, group: str = "stations", limit: int = 100) -> list[LiveEntity]:
        """Fetch satellite TLE data from CelesTrak."""
        url = f"{self.base_url}/pub/TLE/{group}.txt"
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                self.last_success = datetime.utcnow()
                
                return self.normalize(response.text)[:limit]
        except Exception as e:
            self.health_state = ProviderHealthState.UNAVAILABLE
            self.last_error = str(e)
            return []
    
    def normalize(self, raw_data: str) -> list[SatelliteEntity]:
        """Normalize TLE data to SatelliteEntity with SGP4 propagation."""
        # Parse TLE format (3 lines per satellite: name, line1, line2)
        lines = raw_data.strip().split('\n')
        entities = []
        
        for i in range(0, len(lines) - 2, 3):
            if i + 2 >= len(lines):
                break
            
            name = lines[i].strip()
            line1 = lines[i + 1].strip()
            line2 = lines[i + 2].strip()
            
            # Validate TLE format
            if not line1.startswith('1 ') or not line2.startswith('2 '):
                continue
            
            try:
                # Parse epoch from line 1 (columns 19-32)
                epoch_str = line1[18:32].strip()
                epoch_year = int(epoch_str[:2])
                epoch_day = float(epoch_str[2:])
                
                # Convert to datetime
                if epoch_year < 57:
                    year = 2000 + epoch_year
                else:
                    year = 1900 + epoch_year
                
                epoch = datetime(year, 1, 1) + timedelta(days=epoch_day - 1)
                
                # Parse NORAD ID from line 1 (columns 3-7)
                norad_id = int(line1[2:7].strip())
                
                # Parse orbital elements from line 2
                inclination = float(line2[8:16].strip())
                raan = float(line2[17:25].strip())
                eccentricity = float('0.' + line2[26:33].strip())
                arg_perigee = float(line2[34:42].strip())
                mean_anomaly = float(line2[43:51].strip())
                mean_motion = float(line2[52:63].strip())  # revolutions per day
                
                # Calculate current position using simplified SGP4
                # For full SGP4, would use sgp4 library
                lat, lon, alt = self._propagate_position(
                    inclination, raan, eccentricity, arg_perigee, 
                    mean_anomaly, mean_motion, epoch
                )
                
                # Determine orbit class from mean motion
                if mean_motion > 11:
                    orbit_class = "LEO"
                elif mean_motion > 2:
                    orbit_class = "MEO"
                else:
                    orbit_class = "GEO"
                
                entity = SatelliteEntity(
                    entity_type=EntityType.SATELLITE,
                    provider=self.name,
                    latitude=lat,
                    longitude=lon,
                    altitude=alt * 1000,  # Convert km to m
                    observed_at=datetime.utcnow(),
                    norad_id=norad_id,
                    name=name,
                    orbit_class=orbit_class,
                    element_epoch=epoch,
                    orbital_elements_source="CelesTrak TLE",
                    is_propagated=True,
                    knowledge_state=KnowledgeState.INFERRED
                )
                entity.freshness = entity.calculate_freshness()
                entities.append(entity)
                
            except (ValueError, IndexError) as e:
                # Skip malformed TLE entries
                continue
        
        return entities
    
    def _propagate_position(self, inc: float, raan: float, ecc: float, 
                           argp: float, ma: float, n: float, 
                           epoch: datetime) -> tuple[float, float, float]:
        """Simplified position propagation (placeholder for full SGP4)."""
        # This is a simplified calculation - real implementation should use sgp4 library
        # For now, return approximate position based on orbital elements
        
        import math
        
        # Time since epoch in minutes
        dt_minutes = (datetime.utcnow() - epoch).total_seconds() / 60
        
        # Mean anomaly at current time
        current_ma = ma + (360 * n * dt_minutes / 1440)  # degrees
        current_ma = current_ma % 360
        
        # Simplified position calculation (circular orbit approximation)
        # Real SGP4 would be much more complex
        lat = inc * math.sin(math.radians(current_ma))
        lon = (raan + argp + current_ma - 360 * dt_minutes / 1440) % 360
        if lon > 180:
            lon -= 360
        
        # Approximate altitude from mean motion (very rough)
        # Real calculation would use orbital mechanics
        alt = 700 if n > 11 else (2000 if n > 2 else 35786)
        
        return lat, lon, alt


class EarthquakeProvider(BaseProvider):
    """Provider for earthquake data (USGS)."""
    
    def __init__(self):
        super().__init__("USGS Earthquake Hazards Program", 
                        "https://earthquake.usgs.gov")
        self.health_state = ProviderHealthState.AVAILABLE
    
    async def fetch(self, days: int = 7, min_magnitude: float = 2.5,
                    limit: int = 500) -> list[LiveEntity]:
        """Fetch earthquake data from USGS."""
        url = f"{self.base_url}/fdsnws/event/1/query"
        params = {
            "format": "geojson",
            "starttime": (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d"),
            "minmagnitude": min_magnitude,
            "limit": limit,
            "orderby": "time"
        }
        
        data = await self._http_get(url, params=params)
        if data is None:
            return []
        
        return self.normalize(data)
    
    def normalize(self, raw_data: dict) -> list[EarthquakeEntity]:
        """Normalize USGS GeoJSON to EarthquakeEntity."""
        entities = []
        features = raw_data.get("features", [])
        
        for feature in features:
            props = feature.get("properties", {})
            geom = feature.get("geometry", {})
            
            if geom.get("type") != "Point":
                continue
            
            coords = geom.get("coordinates", [])
            if len(coords) < 2:
                continue
            
            lon, lat, depth = coords[0], coords[1], coords[2] if len(coords) > 2 else 0
            
            # Parse time
            time_ms = props.get("time")
            if time_ms:
                observed_at = datetime.utcfromtimestamp(time_ms / 1000)
            else:
                observed_at = datetime.utcnow()
            
            # Parse updated time
            updated_ms = props.get("updated")
            updated_at = datetime.utcfromtimestamp(updated_ms / 1000) if updated_ms else None
            
            entity = EarthquakeEntity(
                entity_type=EntityType.EARTHQUAKE,
                provider=self.name,
                latitude=lat,
                longitude=lon,
                altitude=-depth * 1000,  # Depth in meters (negative = below surface)
                observed_at=observed_at,
                event_id=props.get("id", ""),
                magnitude=props.get("mag", 0.0),
                depth_km=depth,
                place=props.get("place"),
                source_url=props.get("url"),
                updated_at=updated_at,
                metadata={
                    "type": props.get("type"),
                    "status": props.get("status"),
                    "tsunami": props.get("tsunami"),
                    "felt": props.get("felt"),
                    "alert": props.get("alert")
                }
            )
            entity.freshness = entity.calculate_freshness()
            entities.append(entity)
        
        return entities


class FireProvider(BaseProvider):
    """Provider for fire detection data (NASA FIRMS)."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__("NASA FIRMS", "https://firms.modaps.eosdis.nasa.gov")
        self.api_key = api_key
        if api_key:
            self.health_state = ProviderHealthState.AVAILABLE
        else:
            self.health_state = ProviderHealthState.AUTH_REQUIRED
    
    async def fetch(self, days: int = 1, source: str = "VIIRS_SNPP_NRT",
                    bbox: Optional[tuple[float, float, float, float]] = None,
                    limit: int = 1000) -> list[LiveEntity]:
        """Fetch fire detection data from NASA FIRMS."""
        if self.health_state == ProviderHealthState.AUTH_REQUIRED:
            return []
        
        # FIRMS API endpoint
        url = f"{self.base_url}/api/area/{source}/{days}"
        params = {"key": self.api_key}
        
        if bbox:
            # FIRMS uses area coordinates
            params["area"] = f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}"
        
        data = await self._http_get(url, params=params)
        if data is None:
            return []
        
        return self.normalize(data)[:limit]
    
    def normalize(self, raw_data: dict) -> list[FireDetectionEntity]:
        """Normalize FIRMS data to FireDetectionEntity."""
        entities = []
        fires = raw_data.get("data", [])
        
        for fire in fires:
            lat = fire.get("latitude")
            lon = fire.get("longitude")
            
            if lat is None or lon is None:
                continue
            
            # Parse acquisition date/time
            acq_date = fire.get("acq_date")
            acq_time = fire.get("acq_time", 0)
            
            if acq_date:
                # FIRMS format: YYYY-MM-DD, time as HHMM
                try:
                    hour = acq_time // 100
                    minute = acq_time % 100
                    observed_at = datetime.strptime(
                        f"{acq_date} {hour:02d}:{minute:02d}",
                        "%Y-%m-%d %H:%M"
                    )
                except ValueError:
                    observed_at = datetime.utcnow()
            else:
                observed_at = datetime.utcnow()
            
            entity = FireDetectionEntity(
                entity_type=EntityType.FIRE_DETECTION,
                provider=self.name,
                latitude=lat,
                longitude=lon,
                observed_at=observed_at,
                satellite=fire.get("satellite"),
                instrument=fire.get("instrument"),
                confidence=fire.get("confidence"),
                frp=fire.get("frp"),
                acquisition_time=observed_at,
                metadata={
                    "bright_ti4": fire.get("bright_ti4"),
                    "bright_ti5": fire.get("bright_ti5"),
                    "daynight": fire.get("daynight")
                }
            )
            entity.freshness = entity.calculate_freshness()
            entities.append(entity)
        
        return entities
