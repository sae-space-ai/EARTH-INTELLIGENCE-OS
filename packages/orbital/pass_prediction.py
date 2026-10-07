"""Satellite pass prediction with topocentric visibility."""

from datetime import datetime, timedelta
from typing import Optional
import math

from packages.orbital.propagation import SatellitePropagator
from packages.orbital.tle_parser import TLE


class PassPredictor:
    """Predict satellite passes over observer location."""
    
    def __init__(self, propagator: SatellitePropagator):
        """Initialize with satellite propagator."""
        self.propagator = propagator
    
    def predict_passes(self, observer_lat: float, observer_lon: float,
                      observer_alt_m: float, start_time: datetime,
                      duration_hours: int = 24, min_elevation_deg: float = 10.0,
                      max_passes: int = 10) -> list[dict]:
        """
        Predict satellite passes over observer location.
        
        Args:
            observer_lat: Observer latitude (degrees)
            observer_lon: Observer longitude (degrees)
            observer_alt_m: Observer altitude (meters)
            start_time: Start time for prediction
            duration_hours: Prediction duration in hours
            min_elevation_deg: Minimum elevation for visibility
            max_passes: Maximum number of passes to return
        
        Returns:
            List of pass predictions with rise/set/culmination data
        """
        passes = []
        step_seconds = 30  # Check every 30 seconds
        
        current_time = start_time
        end_time = start_time + timedelta(hours=duration_hours)
        
        in_pass = False
        current_pass = None
        
        while current_time < end_time and len(passes) < max_passes:
            try:
                # Get satellite position
                sat_pos = self.propagator.propagate(current_time)
                
                # Calculate topocentric coordinates
                az, el, range_km = self._calculate_topocentric(
                    sat_pos['latitude_deg'],
                    sat_pos['longitude_deg'],
                    sat_pos['altitude_km'],
                    observer_lat,
                    observer_lon,
                    observer_alt_m / 1000.0  # Convert to km
                )
                
                # Check if satellite is above minimum elevation
                is_visible = el >= min_elevation_deg
                
                if is_visible and not in_pass:
                    # Pass starts
                    in_pass = True
                    current_pass = {
                        'rise_time': current_time,
                        'rise_azimuth_deg': az,
                        'culmination_time': current_time,
                        'culmination_elevation_deg': el,
                        'culmination_azimuth_deg': az,
                        'set_time': None,
                        'set_azimuth_deg': None,
                        'max_elevation_deg': el,
                        'duration_seconds': 0,
                    }
                
                elif is_visible and in_pass:
                    # Update culmination if this is highest point
                    if el > current_pass['max_elevation_deg']:
                        current_pass['culmination_time'] = current_time
                        current_pass['culmination_elevation_deg'] = el
                        current_pass['culmination_azimuth_deg'] = az
                        current_pass['max_elevation_deg'] = el
                
                elif not is_visible and in_pass:
                    # Pass ends
                    in_pass = False
                    current_pass['set_time'] = current_time - timedelta(seconds=step_seconds)
                    current_pass['set_azimuth_deg'] = az
                    current_pass['duration_seconds'] = (
                        current_pass['set_time'] - current_pass['rise_time']
                    ).total_seconds()
                    
                    passes.append(current_pass)
                    current_pass = None
                
            except Exception:
                # Skip propagation errors
                pass
            
            current_time += timedelta(seconds=step_seconds)
        
        # Handle pass that extends beyond prediction window
        if in_pass and current_pass:
            current_pass['set_time'] = current_time
            current_pass['duration_seconds'] = (
                current_pass['set_time'] - current_pass['rise_time']
            ).total_seconds()
            passes.append(current_pass)
        
        return passes
    
    def _calculate_topocentric(self, sat_lat: float, sat_lon: float, sat_alt_km: float,
                               obs_lat: float, obs_lon: float, obs_alt_km: float) -> tuple:
        """
        Calculate topocentric coordinates (azimuth, elevation, range).
        
        Args:
            sat_lat: Satellite latitude (degrees)
            sat_lon: Satellite longitude (degrees)
            sat_alt_km: Satellite altitude (km)
            obs_lat: Observer latitude (degrees)
            obs_lon: Observer longitude (degrees)
            obs_alt_km: Observer altitude (km)
        
        Returns:
            (azimuth_deg, elevation_deg, range_km)
        """
        # Convert to radians
        sat_lat_rad = math.radians(sat_lat)
        sat_lon_rad = math.radians(sat_lon)
        obs_lat_rad = math.radians(obs_lat)
        obs_lon_rad = math.radians(obs_lon)
        
        # Earth radius (km)
        R = 6371.0
        
        # Convert satellite and observer to ECEF
        sat_r = R + sat_alt_km
        obs_r = R + obs_alt_km
        
        # Satellite ECEF
        sat_x = sat_r * math.cos(sat_lat_rad) * math.cos(sat_lon_rad)
        sat_y = sat_r * math.cos(sat_lat_rad) * math.sin(sat_lon_rad)
        sat_z = sat_r * math.sin(sat_lat_rad)
        
        # Observer ECEF
        obs_x = obs_r * math.cos(obs_lat_rad) * math.cos(obs_lon_rad)
        obs_y = obs_r * math.cos(obs_lat_rad) * math.sin(obs_lon_rad)
        obs_z = obs_r * math.sin(obs_lat_rad)
        
        # Vector from observer to satellite
        dx = sat_x - obs_x
        dy = sat_y - obs_y
        dz = sat_z - obs_z
        
        # Range
        range_km = math.sqrt(dx * dx + dy * dy + dz * dz)
        
        if range_km < 1e-6:
            return (0.0, 90.0, 0.0)
        
        # Convert to topocentric (South, East, Zenith) coordinate system
        sin_lat = math.sin(obs_lat_rad)
        cos_lat = math.cos(obs_lat_rad)
        sin_lon = math.sin(obs_lon_rad)
        cos_lon = math.cos(obs_lon_rad)
        
        # South component
        s = -sin_lat * cos_lon * dx - sin_lat * sin_lon * dy + cos_lat * dz
        
        # East component
        e = -sin_lon * dx + cos_lon * dy
        
        # Zenith (up) component
        z = cos_lat * cos_lon * dx + cos_lat * sin_lon * dy + sin_lat * dz
        
        # Azimuth (from North, clockwise)
        azimuth_rad = math.atan2(e, -s)  # Note: -s because we want from North
        azimuth_deg = math.degrees(azimuth_rad)
        if azimuth_deg < 0:
            azimuth_deg += 360.0
        
        # Elevation
        horizontal_range = math.sqrt(s * s + e * e)
        elevation_rad = math.atan2(z, horizontal_range)
        elevation_deg = math.degrees(elevation_rad)
        
        return (azimuth_deg, elevation_deg, range_km)
    
    def predict_next_pass(self, observer_lat: float, observer_lon: float,
                         observer_alt_m: float, start_time: Optional[datetime] = None,
                         min_elevation_deg: float = 10.0) -> Optional[dict]:
        """
        Predict the next satellite pass.
        
        Args:
            observer_lat: Observer latitude (degrees)
            observer_lon: Observer longitude (degrees)
            observer_alt_m: Observer altitude (meters)
            start_time: Start time (default: now)
            min_elevation_deg: Minimum elevation for visibility
        
        Returns:
            Next pass prediction or None
        """
        if start_time is None:
            start_time = datetime.utcnow()
        
        passes = self.predict_passes(
            observer_lat, observer_lon, observer_alt_m,
            start_time, duration_hours=48,
            min_elevation_deg=min_elevation_deg,
            max_passes=1
        )
        
        return passes[0] if passes else None
    
    def is_currently_visible(self, observer_lat: float, observer_lon: float,
                            observer_alt_m: float, min_elevation_deg: float = 10.0,
                            time: Optional[datetime] = None) -> tuple[bool, dict]:
        """
        Check if satellite is currently visible.
        
        Args:
            observer_lat: Observer latitude (degrees)
            observer_lon: Observer longitude (degrees)
            observer_alt_m: Observer altitude (meters)
            min_elevation_deg: Minimum elevation for visibility
            time: Time to check (default: now)
        
        Returns:
            (is_visible, topocentric_data)
        """
        if time is None:
            time = datetime.utcnow()
        
        try:
            sat_pos = self.propagator.propagate(time)
            
            az, el, range_km = self._calculate_topocentric(
                sat_pos['latitude_deg'],
                sat_pos['longitude_deg'],
                sat_pos['altitude_km'],
                observer_lat,
                observer_lon,
                observer_alt_m / 1000.0
            )
            
            is_visible = el >= min_elevation_deg
            
            topocentric_data = {
                'azimuth_deg': az,
                'elevation_deg': el,
                'range_km': range_km,
                'satellite_position': sat_pos,
            }
            
            return (is_visible, topocentric_data)
        
        except Exception as e:
            return (False, {'error': str(e)})
