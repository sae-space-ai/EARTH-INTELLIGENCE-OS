"""Satellite propagation using real SGP4 library."""

from datetime import datetime, timedelta
from typing import Optional
import math

from sgp4.api import Satrec, WGS72
from sgp4.earth_gravity import wgs72
from sgp4.ext import invjday
from sgp4.model import Satellite

from packages.orbital.tle_parser import TLE


class SatellitePropagator:
    """Propagate satellite positions using SGP4."""
    
    def __init__(self, tle: TLE):
        """Initialize with TLE orbital elements."""
        self.tle = tle
        self.satellite = self._create_satrec()
    
    def _create_satrec(self) -> Satrec:
        """Create SGP4 satellite record from TLE."""
        # Parse TLE lines into Satrec
        sat = Satrec.twoline2rv(self.tle.line1, self.tle.line2, WGS72)
        return sat
    
    def propagate(self, dt: Optional[datetime] = None) -> dict:
        """
        Propagate satellite to given time.
        
        Args:
            dt: Time to propagate to (default: now)
        
        Returns:
            dict with position (lat, lon, alt) and velocity
        """
        if dt is None:
            dt = datetime.utcnow()
        
        # Convert datetime to Julian date
        jd, fr = self._datetime_to_jd(dt)
        
        # Propagate using SGP4
        error_code, position, velocity = self.satellite.sgp4(jd, fr)
        
        if error_code != 0:
            raise RuntimeError(f"SGP4 propagation error: {error_code}")
        
        # Position is in km (TEME coordinate system)
        # Velocity is in km/s
        
        # Convert from TEME to ECEF
        ecef_pos = self._teme_to_ecef(position, dt)
        
        # Convert ECEF to geodetic (lat, lon, alt)
        lat, lon, alt = self._ecef_to_geodetic(ecef_pos)
        
        return {
            'datetime': dt,
            'position_teme_km': position,
            'position_ecef_km': ecef_pos,
            'velocity_teme_kms': velocity,
            'latitude_deg': lat,
            'longitude_deg': lon,
            'altitude_km': alt,
            'altitude_m': alt * 1000,
        }
    
    def propagate_orbit(self, start_time: datetime, duration_minutes: int, 
                       step_seconds: int = 60) -> list[dict]:
        """
        Propagate satellite orbit over time period.
        
        Args:
            start_time: Start time
            duration_minutes: Duration in minutes
            step_seconds: Time step in seconds
        
        Returns:
            List of position dicts
        """
        positions = []
        end_time = start_time + timedelta(minutes=duration_minutes)
        current_time = start_time
        
        while current_time <= end_time:
            try:
                pos = self.propagate(current_time)
                positions.append(pos)
            except Exception:
                # Skip propagation errors
                pass
            
            current_time += timedelta(seconds=step_seconds)
        
        return positions
    
    def _datetime_to_jd(self, dt: datetime) -> tuple[float, float]:
        """Convert datetime to Julian date and fraction."""
        # Julian date calculation
        year = dt.year
        month = dt.month
        day = dt.day
        hour = dt.hour
        minute = dt.minute
        second = dt.second + dt.microsecond / 1e6
        
        if month <= 2:
            year -= 1
            month += 12
        
        A = int(year / 100)
        B = 2 - A + int(A / 4)
        
        jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5
        
        # Add time fraction
        day_fraction = (hour + minute / 60 + second / 3600) / 24
        jd += day_fraction
        
        # Split into integer and fraction for SGP4
        jd_int = int(jd)
        jd_frac = jd - jd_int
        
        return float(jd_int), float(jd_frac)
    
    def _teme_to_ecef(self, teme_pos: tuple, dt: datetime) -> tuple:
        """
        Convert TEME (True Equator Mean Equinox) to ECEF.
        
        Simplified rotation using GMST (Greenwich Mean Sidereal Time).
        """
        # Calculate GMST
        jd, fr = self._datetime_to_jd(dt)
        jd_full = jd + fr
        
        # Julian centuries from J2000
        T = (jd_full - 2451545.0) / 36525.0
        
        # GMST in radians
        gmst = (280.46061837 + 360.98564736629 * (jd_full - 2451545.0) + 
                0.000387933 * T * T - T * T * T / 38710000.0)
        gmst = math.radians(gmst % 360)
        
        # Rotation matrix (Z-axis rotation by GMST)
        x_teme, y_teme, z_teme = teme_pos
        
        x_ecef = x_teme * math.cos(gmst) + y_teme * math.sin(gmst)
        y_ecef = -x_teme * math.sin(gmst) + y_teme * math.cos(gmst)
        z_ecef = z_teme
        
        return (x_ecef, y_ecef, z_ecef)
    
    def _ecef_to_geodetic(self, ecef_pos: tuple) -> tuple:
        """
        Convert ECEF coordinates to geodetic (lat, lon, alt).
        
        Uses iterative method for accuracy.
        """
        x, y, z = ecef_pos
        
        # WGS84 ellipsoid parameters
        a = 6378.137  # semi-major axis (km)
        f = 1 / 298.257223563  # flattening
        e2 = 2 * f - f * f  # eccentricity squared
        
        # Longitude
        lon = math.atan2(y, x)
        
        # Distance from Z-axis
        p = math.sqrt(x * x + y * y)
        
        # Initial latitude estimate
        lat = math.atan2(z, p * (1 - e2))
        
        # Iterative refinement
        for _ in range(5):
            N = a / math.sqrt(1 - e2 * math.sin(lat) * math.sin(lat))
            lat_new = math.atan2(z + e2 * N * math.sin(lat), p)
            
            if abs(lat_new - lat) < 1e-12:
                break
            lat = lat_new
        
        # Altitude
        N = a / math.sqrt(1 - e2 * math.sin(lat) * math.sin(lat))
        alt = p / math.cos(lat) - N
        
        # Convert to degrees
        lat_deg = math.degrees(lat)
        lon_deg = math.degrees(lon)
        
        return (lat_deg, lon_deg, alt)
    
    def get_ground_track(self, start_time: datetime, duration_orbits: int = 1,
                        points_per_orbit: int = 100) -> list[dict]:
        """
        Generate ground track (lat/lon) for satellite.
        
        Args:
            start_time: Start time
            duration_orbits: Number of orbits to track
            points_per_orbit: Points per orbit
        
        Returns:
            List of ground track points
        """
        # Calculate orbital period from mean motion
        orbital_period_minutes = 24 * 60 / self.tle.mean_motion
        total_minutes = orbital_period_minutes * duration_orbits
        
        total_points = points_per_orbit * duration_orbits
        step_minutes = total_minutes / total_points
        
        ground_track = []
        current_time = start_time
        
        for _ in range(total_points):
            try:
                pos = self.propagate(current_time)
                ground_track.append({
                    'datetime': current_time,
                    'latitude_deg': pos['latitude_deg'],
                    'longitude_deg': pos['longitude_deg'],
                    'altitude_km': pos['altitude_km'],
                })
            except Exception:
                pass
            
            current_time += timedelta(minutes=step_minutes)
        
        return ground_track
    
    @property
    def orbital_period_minutes(self) -> float:
        """Get orbital period in minutes."""
        return 24 * 60 / self.tle.mean_motion
    
    @property
    def is_geostationary(self) -> bool:
        """Check if satellite is geostationary."""
        # Geostationary: ~24 hour period, low inclination, low eccentricity
        return (abs(self.orbital_period_minutes - 1436) < 10 and
                self.tle.inclination < 1.0 and
                self.tle.eccentricity < 0.01)
    
    @property
    def orbit_type(self) -> str:
        """Classify orbit type."""
        if self.is_geostationary:
            return "GEO"
        elif self.tle.mean_motion > 11:  # ~100 min period
            return "LEO"
        elif self.tle.mean_motion > 2:  # ~12 hour period
            return "MEO"
        else:
            return "HEO"
