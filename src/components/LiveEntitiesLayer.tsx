import { useEffect, useState } from 'react';
import { Entity, PointGraphics, PolylineGraphics, LabelGraphics } from 'resium';
import { Cartesian3, Color, Cartesian2, Cartographic, Math as CesiumMath } from 'cesium';

interface LiveEntity {
  id: string;
  entity_type: string;
  provider: string;
  latitude: number;
  longitude: number;
  altitude?: number;
  heading?: number;
  speed?: number;
  observed_at: string;
  retrieved_at: string;
  freshness: string;
  knowledge_state: string;
  metadata: Record<string, any>;
}

interface TrailPoint {
  latitude: number;
  longitude: number;
  altitude?: number;
  timestamp: string;
}

interface LiveEntitiesLayerProps {
  entityType: string;
  enabled: boolean;
  selectedEntityId?: string | null;
  trackedEntityIds?: string[];
  onEntityClick?: (entity: LiveEntity) => void;
  apiEndpoint: string;
  refreshInterval?: number;
  bbox?: [number, number, number, number];
}

// Color schemes for different entity types
const ENTITY_COLORS: Record<string, Color> = {
  AIRCRAFT: Color.fromCssColorString('#00d4ff'),
  MILITARY_AIRCRAFT: Color.fromCssColorString('#ff6b35'),
  VESSEL: Color.fromCssColorString('#00ff88'),
  SATELLITE: Color.fromCssColorString('#a855f7'),
  EARTHQUAKE: Color.fromCssColorString('#ff3366'),
  FIRE_DETECTION: Color.fromCssColorString('#ffd700'),
};

// Size schemes for different entity types
const ENTITY_SIZES: Record<string, number> = {
  AIRCRAFT: 8,
  MILITARY_AIRCRAFT: 10,
  VESSEL: 10,
  SATELLITE: 6,
  EARTHQUAKE: 12,
  FIRE_DETECTION: 8,
};

export function LiveEntitiesLayer({
  entityType,
  enabled,
  selectedEntityId,
  trackedEntityIds = [],
  onEntityClick,
  apiEndpoint,
  refreshInterval = 30000,
  bbox,
}: LiveEntitiesLayerProps) {
  const [entities, setEntities] = useState<LiveEntity[]>([]);
  const [trails, setTrails] = useState<Record<string, TrailPoint[]>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!enabled) {
      setEntities([]);
      return;
    }

    const fetchEntities = async () => {
      setLoading(true);
      setError(null);

      try {
        let url = apiEndpoint;
        if (bbox) {
          const bboxParam = `${bbox[0]},${bbox[1]},${bbox[2]},${bbox[3]}`;
          url += `?bbox=${bboxParam}`;
        }

        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        setEntities(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchEntities();
    const interval = setInterval(fetchEntities, refreshInterval);

    return () => clearInterval(interval);
  }, [enabled, apiEndpoint, refreshInterval, bbox]);

  // Fetch trails for tracked entities
  useEffect(() => {
    if (!trackedEntityIds.length) return;

    const fetchTrails = async () => {
      const newTrails: Record<string, TrailPoint[]> = {};

      for (const entityId of trackedEntityIds) {
        try {
          const response = await fetch(`/api/v1/live/trail/${entityId}`);
          if (response.ok) {
            const data = await response.json();
            newTrails[entityId] = data.points;
          }
        } catch (err) {
          console.error(`Failed to fetch trail for ${entityId}:`, err);
        }
      }

      setTrails(newTrails);
    };

    fetchTrails();
    const interval = setInterval(fetchTrails, 10000);

    return () => clearInterval(interval);
  }, [trackedEntityIds]);

  if (!enabled || entities.length === 0) {
    return null;
  }

  const color = ENTITY_COLORS[entityType] || Color.WHITE;
  const size = ENTITY_SIZES[entityType] || 8;

  return (
    <>
      {entities.map((entity) => {
        const isSelected = selectedEntityId === entity.id;
        const isTracked = trackedEntityIds.includes(entity.id);
        const position = Cartesian3.fromDegrees(
          entity.longitude,
          entity.latitude,
          entity.altitude || 0
        );

        // Determine point color based on selection/tracking state
        let pointColor = color;
        if (isSelected) {
          pointColor = Color.WHITE;
        } else if (isTracked) {
          pointColor = Color.YELLOW;
        }

        // Adjust size for selection
        const pointSize = isSelected ? size * 1.5 : size;

        return (
          <Entity
            key={entity.id}
            position={position}
            onClick={() => onEntityClick?.(entity)}
          >
            <PointGraphics
              pixelSize={pointSize}
              color={pointColor}
              outlineColor={Color.BLACK}
              outlineWidth={1}
              //@ts-ignore
              disableDepthTestDistance={Number.POSITIVE_INFINITY}
            />
            
            {/* Label for selected entity */}
            {isSelected && (
              <LabelGraphics
                text={getEntityLabel(entity)}
                font="12px sans-serif"
                fillColor={Color.WHITE}
                outlineColor={Color.BLACK}
                outlineWidth={2}
                style={1} // FILL_AND_OUTLINE
                pixelOffset={new Cartesian2(0, -20)}
                //@ts-ignore
                disableDepthTestDistance={Number.POSITIVE_INFINITY}
              />
            )}
          </Entity>
        );
      })}

      {/* Render trails for tracked entities */}
      {Object.entries(trails).map(([entityId, trail]) => {
        if (trail.length < 2) return null;

        const positions = trail.flatMap((point) => [
          point.longitude,
          point.latitude,
          point.altitude || 0,
        ]);

        return (
          <Entity key={`trail-${entityId}`}>
            <PolylineGraphics
              positions={Cartesian3.fromDegreesArrayHeights(positions)}
              width={2}
              material={Color.YELLOW.withAlpha(0.6)}
              clampToGround={false}
            />
          </Entity>
        );
      })}
    </>
  );
}

function getEntityLabel(entity: LiveEntity): string {
  const meta = entity.metadata;

  switch (entity.entity_type) {
    case 'AIRCRAFT':
      return meta.callsign || meta.icao24 || 'Aircraft';
    case 'MILITARY_AIRCRAFT':
      return meta.callsign || 'Military';
    case 'VESSEL':
      return meta.name || meta.mmsi?.toString() || 'Vessel';
    case 'SATELLITE':
      return meta.name || `NORAD ${meta.norad_id}`;
    case 'EARTHQUAKE':
      return `M${meta.magnitude?.toFixed(1)}`;
    case 'FIRE_DETECTION':
      return meta.satellite || 'Fire';
    default:
      return 'Entity';
  }
}

// Component for earthquake-specific rendering (magnitude-based sizing)
export function EarthquakeLayer(props: Omit<LiveEntitiesLayerProps, 'entityType'>) {
  return <LiveEntitiesLayer {...props} entityType="EARTHQUAKE" />;
}

// Component for fire detection rendering
export function FireDetectionLayer(props: Omit<LiveEntitiesLayerProps, 'entityType'>) {
  return <LiveEntitiesLayer {...props} entityType="FIRE_DETECTION" />;
}

// Component for satellite rendering with orbit lines
export function SatelliteLayer({
  enabled,
  selectedEntityId,
  trackedEntityIds = [],
  onEntityClick,
  refreshInterval = 60000,
}: Omit<LiveEntitiesLayerProps, 'entityType' | 'apiEndpoint' | 'bbox'>) {
  return (
    <LiveEntitiesLayer
      entityType="SATELLITE"
      enabled={enabled}
      selectedEntityId={selectedEntityId}
      trackedEntityIds={trackedEntityIds}
      onEntityClick={onEntityClick}
      apiEndpoint="/api/v1/live/satellites"
      refreshInterval={refreshInterval}
    />
  );
}
