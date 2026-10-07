"""TLE (Two-Line Element) parser for orbital elements."""

from datetime import datetime
from typing import Optional
from dataclasses import dataclass


@dataclass
class TLE:
    """Parsed TLE orbital elements."""
    name: str
    line1: str
    line2: str
    
    # Parsed fields
    norad_id: int
    classification: str
    launch_year: int
    launch_number: int
    launch_piece: str
    epoch_year: int
    epoch_day: float
    mean_motion_dot: float
    mean_motion_ddot: float
    bstar: float
    ephemeris_type: int
    element_set_number: int
    
    inclination: float  # degrees
    raan: float  # degrees
    eccentricity: float
    arg_perigee: float  # degrees
    mean_anomaly: float  # degrees
    mean_motion: float  # revolutions per day
    revolution_number: int
    
    @property
    def epoch_datetime(self) -> datetime:
        """Convert epoch to datetime."""
        # TLE epoch year: 00-56 = 2000-2056, 57-99 = 1957-1999
        if self.epoch_year < 57:
            year = 2000 + self.epoch_year
        else:
            year = 1900 + self.epoch_year
        
        # Day of year (fractional)
        return datetime(year, 1, 1) + timedelta(days=self.epoch_day - 1)
    
    @property
    def age_days(self) -> float:
        """Age of TLE in days from epoch to now."""
        from datetime import timedelta
        return (datetime.utcnow() - self.epoch_datetime).total_seconds() / 86400


class TLEParser:
    """Parse TLE format into orbital elements."""
    
    @staticmethod
    def parse(tle_text: str) -> list[TLE]:
        """Parse TLE text (can contain multiple satellites)."""
        lines = [line.strip() for line in tle_text.strip().split('\n') if line.strip()]
        tles = []
        
        i = 0
        while i < len(lines):
            # Check if we have a name line + 2 TLE lines
            if i + 2 < len(lines):
                name = lines[i]
                line1 = lines[i + 1]
                line2 = lines[i + 2]
                
                # Validate TLE format
                if line1.startswith('1 ') and line2.startswith('2 '):
                    try:
                        tle = TLEParser._parse_single(name, line1, line2)
                        tles.append(tle)
                        i += 3
                        continue
                    except Exception as e:
                        # Skip malformed TLE
                        pass
            
            i += 1
        
        return tles
    
    @staticmethod
    def _parse_single(name: str, line1: str, line2: str) -> TLE:
        """Parse a single TLE (name + 2 lines)."""
        # Line 1 parsing
        norad_id = int(line1[2:7].strip())
        classification = line1[7].strip()
        launch_year = int(line1[9:11].strip())
        launch_number = int(line1[11:14].strip())
        launch_piece = line1[14:17].strip()
        epoch_year = int(line1[18:20].strip())
        epoch_day = float(line1[20:32].strip())
        mean_motion_dot = float(line1[33:43].strip())
        mean_motion_ddot = float(f"0.{line1[44:50].strip()}e{line1[50:52].strip()}")
        bstar = float(f"0.{line1[53:59].strip()}e{line1[59:61].strip()}")
        ephemeris_type = int(line1[62].strip())
        element_set_number = int(line1[64:68].strip())
        
        # Line 2 parsing
        inclination = float(line2[8:16].strip())
        raan = float(line2[17:25].strip())
        eccentricity = float(f"0.{line2[26:33].strip()}")
        arg_perigee = float(line2[34:42].strip())
        mean_anomaly = float(line2[43:51].strip())
        mean_motion = float(line2[52:63].strip())
        revolution_number = int(line2[63:68].strip())
        
        return TLE(
            name=name,
            line1=line1,
            line2=line2,
            norad_id=norad_id,
            classification=classification,
            launch_year=launch_year,
            launch_number=launch_number,
            launch_piece=launch_piece,
            epoch_year=epoch_year,
            epoch_day=epoch_day,
            mean_motion_dot=mean_motion_dot,
            mean_motion_ddot=mean_motion_ddot,
            bstar=bstar,
            ephemeris_type=ephemeris_type,
            element_set_number=element_set_number,
            inclination=inclination,
            raan=raan,
            eccentricity=eccentricity,
            arg_perigee=arg_perigee,
            mean_anomaly=mean_anomaly,
            mean_motion=mean_motion,
            revolution_number=revolution_number,
        )
    
    @staticmethod
    def validate_checksum(line: str) -> bool:
        """Validate TLE line checksum."""
        if len(line) < 69:
            return False
        
        checksum_char = line[68]
        if not checksum_char.isdigit():
            return False
        
        expected_checksum = int(checksum_char)
        calculated = 0
        
        for i, char in enumerate(line[:68]):
            if char.isdigit():
                calculated += int(char)
            elif char == '-':
                calculated += 1
        
        return (calculated % 10) == expected_checksum
