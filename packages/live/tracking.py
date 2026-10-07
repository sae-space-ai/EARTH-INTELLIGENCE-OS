"""Entity tracking and selection state management."""

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from packages.live.models import LiveEntity, EntityType


class SelectionState:
    """Manages selected entity state."""
    
    def __init__(self):
        self._selected_entity_id: Optional[UUID] = None
        self._selected_entity: Optional[LiveEntity] = None
    
    @property
    def selected_entity(self) -> Optional[LiveEntity]:
        """Get currently selected entity."""
        return self._selected_entity
    
    @property
    def selected_entity_id(self) -> Optional[UUID]:
        """Get ID of selected entity."""
        return self._selected_entity_id
    
    def select(self, entity: LiveEntity) -> None:
        """Select an entity."""
        self._selected_entity = entity
        self._selected_entity_id = entity.id
    
    def deselect(self) -> None:
        """Deselect current entity."""
        self._selected_entity = None
        self._selected_entity_id = None
    
    def update(self, entity: LiveEntity) -> None:
        """Update selected entity with new data."""
        if self._selected_entity_id == entity.id:
            self._selected_entity = entity
    
    def is_selected(self, entity_id: UUID) -> bool:
        """Check if entity is currently selected."""
        return self._selected_entity_id == entity_id


class TrailPoint:
    """A point in an entity's trail."""
    
    def __init__(self, latitude: float, longitude: float, altitude: Optional[float],
                 timestamp: datetime):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.timestamp = timestamp


class EntityTracker:
    """Manages entity tracking state and trails."""
    
    def __init__(self, max_trail_points: int = 100, max_trail_duration_hours: float = 2.0):
        self._tracked_entities: dict[UUID, LiveEntity] = {}
        self._trails: dict[UUID, list[TrailPoint]] = defaultdict(list)
        self._max_trail_points = max_trail_points
        self._max_trail_duration = timedelta(hours=max_trail_duration_hours)
    
    @property
    def tracked_entities(self) -> dict[UUID, LiveEntity]:
        """Get all tracked entities."""
        return self._tracked_entities.copy()
    
    def track(self, entity: LiveEntity) -> None:
        """Start tracking an entity."""
        self._tracked_entities[entity.id] = entity
        
        # Add initial trail point
        self._add_trail_point(entity)
    
    def untrack(self, entity_id: UUID) -> None:
        """Stop tracking an entity."""
        if entity_id in self._tracked_entities:
            del self._tracked_entities[entity_id]
            # Keep trail for visualization
            # del self._trails[entity_id]  # Optionally clear trail
    
    def is_tracked(self, entity_id: UUID) -> bool:
        """Check if entity is being tracked."""
        return entity_id in self._tracked_entities
    
    def update_entity(self, entity: LiveEntity) -> None:
        """Update tracked entity with new position/data."""
        if entity.id in self._tracked_entities:
            self._tracked_entities[entity.id] = entity
            self._add_trail_point(entity)
    
    def get_trail(self, entity_id: UUID) -> list[TrailPoint]:
        """Get trail points for an entity."""
        return self._trails.get(entity_id, [])
    
    def _add_trail_point(self, entity: LiveEntity) -> None:
        """Add a point to entity's trail."""
        trail = self._trails[entity.id]
        
        # Add new point
        point = TrailPoint(
            latitude=entity.latitude,
            longitude=entity.longitude,
            altitude=entity.altitude,
            timestamp=entity.observed_at
        )
        trail.append(point)
        
        # Enforce limits
        self._enforce_trail_limits(trail)
    
    def _enforce_trail_limits(self, trail: list[TrailPoint]) -> None:
        """Enforce trail point count and duration limits."""
        # Remove points older than max duration
        cutoff_time = datetime.utcnow() - self._max_trail_duration
        trail[:] = [p for p in trail if p.timestamp > cutoff_time]
        
        # Remove oldest points if over max count
        if len(trail) > self._max_trail_points:
            trail[:] = trail[-self._max_trail_points:]
    
    def clear_all_trails(self) -> None:
        """Clear all trails."""
        self._trails.clear()
    
    def get_nearest_entity(self, latitude: float, longitude: float,
                          entity_type: Optional[EntityType] = None,
                          max_distance_km: float = 100.0) -> Optional[LiveEntity]:
        """Find nearest entity to a location.
        
        Args:
            latitude: Target latitude
            longitude: Target longitude
            entity_type: Optional filter by entity type
            max_distance_km: Maximum search radius in kilometers
        
        Returns:
            Nearest entity or None if none found within radius
        """
        nearest = None
        min_distance = float('inf')
        
        for entity in self._tracked_entities.values():
            # Filter by type if specified
            if entity_type and entity.entity_type != entity_type:
                continue
            
            # Calculate distance using Haversine formula
            distance = self._calculate_distance(
                latitude, longitude,
                entity.latitude, entity.longitude
            )
            
            if distance < min_distance and distance <= max_distance_km:
                min_distance = distance
                nearest = entity
        
        return nearest
    
    def _calculate_distance(self, lat1: float, lon1: float,
                           lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula.
        
        Returns:
            Distance in kilometers
        """
        import math
        
        # Earth radius in kilometers
        R = 6371.0
        
        # Convert to radians
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        # Haversine formula
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c


class ViewportFilter:
    """Filters entities by viewport bounds."""
    
    def __init__(self, min_lat: float, max_lat: float,
                 min_lon: float, max_lon: float):
        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_lon = min_lon
        self.max_lon = max_lon
    
    def contains(self, entity: LiveEntity) -> bool:
        """Check if entity is within viewport."""
        return (self.min_lat <= entity.latitude <= self.max_lat and
                self.min_lon <= entity.longitude <= self.max_lon)
    
    def filter_entities(self, entities: list[LiveEntity]) -> list[LiveEntity]:
        """Filter entities by viewport bounds."""
        return [e for e in entities if self.contains(e)]
