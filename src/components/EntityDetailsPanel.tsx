import { X, Navigation, Clock, MapPin, Activity, Satellite as SatelliteIcon, Flame, Plane, Ship } from 'lucide-react';

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

interface EntityDetailsPanelProps {
  entity: LiveEntity | null;
  onClose: () => void;
  onTrack?: (entityId: string) => void;
  onUntrack?: (entityId: string) => void;
  isTracked?: boolean;
}

const ENTITY_ICONS: Record<string, any> = {
  AIRCRAFT: Plane,
  MILITARY_AIRCRAFT: Plane,
  VESSEL: Ship,
  SATELLITE: SatelliteIcon,
  EARTHQUAKE: Activity,
  FIRE_DETECTION: Flame,
};

const FRESHNESS_COLORS: Record<string, string> = {
  LIVE: 'text-neon-green',
  DELAYED: 'text-neon-yellow',
  STALE: 'text-neon-red',
  UNAVAILABLE: 'text-gray-500',
};

export function EntityDetailsPanel({
  entity,
  onClose,
  onTrack,
  onUntrack,
  isTracked = false,
}: EntityDetailsPanelProps) {
  if (!entity) return null;

  const Icon = ENTITY_ICONS[entity.entity_type] || MapPin;
  const freshnessColor = FRESHNESS_COLORS[entity.freshness] || 'text-gray-400';

  const observedTime = new Date(entity.observed_at);
  const retrievedTime = new Date(entity.retrieved_at);
  const ageSeconds = Math.floor((Date.now() - observedTime.getTime()) / 1000);

  return (
    <div className="absolute right-4 top-20 w-80 bg-earth-800 border border-earth-600 rounded-lg shadow-xl z-40">
      {/* Header */}
      <div className="flex items-center justify-between p-3 border-b border-earth-600">
        <div className="flex items-center gap-2">
          <Icon size={18} className="text-neon-blue" />
          <h3 className="text-sm font-semibold text-white">
            {getEntityTitle(entity)}
          </h3>
        </div>
        <button
          onClick={onClose}
          className="text-earth-400 hover:text-white transition-colors"
        >
          <X size={16} />
        </button>
      </div>

      {/* Content */}
      <div className="p-3 space-y-3">
        {/* Identity Section */}
        <Section title="IDENTITY">
          <InfoRow label="Type" value={formatEntityType(entity.entity_type)} />
          {entity.metadata.callsign && (
            <InfoRow label="Callsign" value={entity.metadata.callsign} />
          )}
          {entity.metadata.name && (
            <InfoRow label="Name" value={entity.metadata.name} />
          )}
          {entity.metadata.icao24 && (
            <InfoRow label="ICAO24" value={entity.metadata.icao24} />
          )}
          {entity.metadata.mmsi && (
            <InfoRow label="MMSI" value={entity.metadata.mmsi} />
          )}
          {entity.metadata.norad_id && (
            <InfoRow label="NORAD ID" value={entity.metadata.norad_id} />
          )}
          {entity.metadata.registration && (
            <InfoRow label="Registration" value={entity.metadata.registration} />
          )}
        </Section>

        {/* Location Section */}
        <Section title="LOCATION">
          <InfoRow
            label="Coordinates"
            value={`${entity.latitude.toFixed(4)}°, ${entity.longitude.toFixed(4)}°`}
          />
          {entity.altitude !== undefined && (
            <InfoRow
              label="Altitude"
              value={formatAltitude(entity.altitude, entity.entity_type)}
            />
          )}
          {entity.heading !== undefined && (
            <InfoRow label="Heading" value={`${entity.heading.toFixed(0)}°`} />
          )}
          {entity.speed !== undefined && (
            <InfoRow label="Speed" value={formatSpeed(entity.speed, entity.entity_type)} />
          )}
        </Section>

        {/* Status Section */}
        <Section title="STATUS">
          <div className="flex items-center justify-between">
            <span className="text-xs text-earth-400">Freshness</span>
            <span className={`text-xs font-mono ${freshnessColor}`}>
              {entity.freshness}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-xs text-earth-400">Knowledge State</span>
            <span className="text-xs font-mono text-neon-purple">
              {entity.knowledge_state}
            </span>
          </div>
          {entity.metadata.status && (
            <InfoRow label="Status" value={entity.metadata.status} />
          )}
          {entity.metadata.navigation_status && (
            <InfoRow label="Nav Status" value={entity.metadata.navigation_status} />
          )}
        </Section>

        {/* Time Section */}
        <Section title="TIME">
          <div className="flex items-center justify-between">
            <span className="text-xs text-earth-400">Observed</span>
            <span className="text-xs font-mono text-earth-200">
              {formatTimestamp(observedTime)}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-xs text-earth-400">Age</span>
            <span className="text-xs font-mono text-earth-200">
              {formatAge(ageSeconds)}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-xs text-earth-400">Retrieved</span>
            <span className="text-xs font-mono text-earth-200">
              {formatTimestamp(retrievedTime)}
            </span>
          </div>
        </Section>

        {/* Provider Section */}
        <Section title="PROVIDER">
          <InfoRow label="Source" value={entity.provider} />
          {entity.metadata.source_url && (
            <a
              href={entity.metadata.source_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-neon-blue hover:underline"
            >
              View Source →
            </a>
          )}
        </Section>

        {/* Type-Specific Data */}
        {getTypeSpecificData(entity).length > 0 && (
          <Section title="DETAILS">
            {getTypeSpecificData(entity).map(({ label, value }) => (
              <InfoRow key={label} label={label} value={value} />
            ))}
          </Section>
        )}

        {/* Actions */}
        <div className="flex gap-2 pt-2 border-t border-earth-600">
          {onTrack && (
            <button
              onClick={() => isTracked ? onUntrack?.(entity.id) : onTrack(entity.id)}
              className={`flex-1 px-3 py-1.5 text-xs rounded transition-colors ${
                isTracked
                  ? 'bg-neon-yellow/20 text-neon-yellow hover:bg-neon-yellow/30'
                  : 'bg-neon-blue/20 text-neon-blue hover:bg-neon-blue/30'
              }`}
            >
              {isTracked ? 'Untrack' : 'Track'}
            </button>
          )}
          <button
            onClick={() => {
              // Center camera on entity
              window.postMessage({
                type: 'CENTER_CAMERA',
                latitude: entity.latitude,
                longitude: entity.longitude,
                altitude: entity.altitude || 10000,
              }, '*');
            }}
            className="flex-1 px-3 py-1.5 text-xs rounded bg-earth-700 text-earth-200 hover:bg-earth-600 transition-colors"
          >
            Center
          </button>
        </div>
      </div>
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div>
      <h4 className="text-[10px] font-semibold text-earth-400 uppercase tracking-wider mb-1">
        {title}
      </h4>
      <div className="space-y-1">{children}</div>
    </div>
  );
}

function InfoRow({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-xs text-earth-400">{label}</span>
      <span className="text-xs font-mono text-earth-200">{value}</span>
    </div>
  );
}

function getEntityTitle(entity: LiveEntity): string {
  const meta = entity.metadata;
  
  switch (entity.entity_type) {
    case 'AIRCRAFT':
      return meta.callsign || meta.icao24 || 'Aircraft';
    case 'MILITARY_AIRCRAFT':
      return meta.callsign || 'Military Aircraft';
    case 'VESSEL':
      return meta.name || `MMSI ${meta.mmsi}` || 'Vessel';
    case 'SATELLITE':
      return meta.name || `NORAD ${meta.norad_id}`;
    case 'EARTHQUAKE':
      return `Earthquake M${meta.magnitude?.toFixed(1)}`;
    case 'FIRE_DETECTION':
      return `${meta.satellite || 'Fire'} Detection`;
    default:
      return 'Entity';
  }
}

function formatEntityType(type: string): string {
  return type
    .split('_')
    .map(word => word.charAt(0) + word.slice(1).toLowerCase())
    .join(' ');
}

function formatAltitude(altitude: number, entityType: string): string {
  if (entityType === 'EARTHQUAKE') {
    return `${Math.abs(altitude / 1000).toFixed(1)} km depth`;
  }
  if (altitude > 1000) {
    return `${(altitude / 1000).toFixed(1)} km`;
  }
  return `${altitude.toFixed(0)} m`;
}

function formatSpeed(speed: number, entityType: string): string {
  if (entityType === 'VESSEL') {
    // Convert m/s to knots
    return `${(speed * 1.94384).toFixed(1)} kn`;
  }
  // Convert m/s to km/h
  return `${(speed * 3.6).toFixed(0)} km/h`;
}

function formatTimestamp(date: Date): string {
  return date.toISOString().replace('T', ' ').substring(0, 19) + ' UTC';
}

function formatAge(seconds: number): string {
  if (seconds < 60) return `${seconds}s ago`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  return `${Math.floor(seconds / 86400)}d ago`;
}

function getTypeSpecificData(entity: LiveEntity): Array<{ label: string; value: string }> {
  const meta = entity.metadata;
  const data: Array<{ label: string; value: string }> = [];

  switch (entity.entity_type) {
    case 'AIRCRAFT':
    case 'MILITARY_AIRCRAFT':
      if (meta.aircraft_type) data.push({ label: 'Type', value: meta.aircraft_type });
      if (meta.squawk) data.push({ label: 'Squawk', value: meta.squawk });
      if (meta.vertical_rate) {
        data.push({ label: 'V/Rate', value: `${meta.vertical_rate.toFixed(0)} m/s` });
      }
      if (meta.country) data.push({ label: 'Country', value: meta.country });
      break;

    case 'VESSEL':
      if (meta.ship_type) data.push({ label: 'Ship Type', value: meta.ship_type });
      if (meta.destination) data.push({ label: 'Destination', value: meta.destination });
      if (meta.course) data.push({ label: 'Course', value: `${meta.course.toFixed(0)}°` });
      break;

    case 'SATELLITE':
      if (meta.orbit_class) data.push({ label: 'Orbit', value: meta.orbit_class });
      if (meta.mission) data.push({ label: 'Mission', value: meta.mission });
      if (meta.element_epoch) {
        data.push({ label: 'Epoch', value: formatTimestamp(new Date(meta.element_epoch)) });
      }
      if (meta.is_propagated) {
        data.push({ label: 'Position', value: 'Propagated' });
      }
      break;

    case 'EARTHQUAKE':
      if (meta.place) data.push({ label: 'Place', value: meta.place });
      if (meta.magnitude) data.push({ label: 'Magnitude', value: meta.magnitude.toFixed(1) });
      if (meta.tsunami) data.push({ label: 'Tsunami', value: meta.tsunami ? 'Yes' : 'No' });
      if (meta.felt) data.push({ label: 'Felt Reports', value: meta.felt.toString() });
      break;

    case 'FIRE_DETECTION':
      if (meta.satellite) data.push({ label: 'Satellite', value: meta.satellite });
      if (meta.instrument) data.push({ label: 'Instrument', value: meta.instrument });
      if (meta.confidence) data.push({ label: 'Confidence', value: meta.confidence });
      if (meta.frp) data.push({ label: 'FRP', value: `${meta.frp.toFixed(1)} MW` });
      break;
  }

  return data;
}
