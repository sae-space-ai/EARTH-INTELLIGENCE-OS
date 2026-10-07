import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Globe } from '../components/Globe';
import { LiveEntitiesLayer, SatelliteLayer, EarthquakeLayer, FireDetectionLayer } from '../components/LiveEntitiesLayer';
import { EntityDetailsPanel } from '../components/EntityDetailsPanel';
import {
  Globe as GlobeIcon, Layers, Radio, Satellite, Cloud,
  Zap, Shield, Activity, Eye, Settings, ChevronRight,
  ChevronDown, Search, Crosshair, Navigation, Camera,
  Flame, Droplet, Wind, MapPin, Wifi, Truck, Bus
} from 'lucide-react';

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

type Context = 'NEUTRAL' | 'LIVE_CONTACTS' | 'SPACE_MISSIONS' | 'ENVIRONMENTAL' | 'EUROPEAN_SPACE' | 'EARTH_EVENTS';
type VisualStyle = 'NORMAL' | 'NVG' | 'FLIR' | 'CRT' | 'NOIR';

interface LayerState {
  id: string;
  name: string;
  icon: React.ReactNode;
  enabled: boolean;
  category: string;
  provider?: string;
  status?: string;
  color: string;
}

const initialLayers: LayerState[] = [
  // Movement
  { id: 'aircraft', name: 'Live Aircraft', icon: <Zap size={14} />, enabled: false, category: 'MOVEMENT', provider: 'OpenSky', status: 'PORTED', color: '#00d4ff' },
  { id: 'military', name: 'Military ADS-B', icon: <Shield size={14} />, enabled: false, category: 'MOVEMENT', provider: 'adsb.lol', status: 'PORTED', color: '#ff6b35' },
  { id: 'vessels', name: 'Live Vessels', icon: <Droplet size={14} />, enabled: false, category: 'MOVEMENT', provider: 'AISStream', status: 'PORTED', color: '#00d4ff' },
  { id: 'traffic', name: 'Traffic', icon: <Truck size={14} />, enabled: false, category: 'MOVEMENT', provider: 'OSM/TomTom', status: 'REGISTERED', color: '#ffd700' },
  { id: 'transit', name: 'Public Transit', icon: <Bus size={14} />, enabled: false, category: 'MOVEMENT', provider: 'GTFS-RT', status: 'REGISTERED', color: '#00ff88' },

  // Orbital
  { id: 'satellites', name: 'Satellites', icon: <Satellite size={14} />, enabled: true, category: 'ORBITAL', provider: 'CelesTrak', status: 'PORTED', color: '#a855f7' },
  { id: 'space-missions', name: 'Space Missions', icon: <Rocket size={14} />, enabled: false, category: 'ORBITAL', provider: 'Launch Library 2', status: 'REGISTERED', color: '#ff3366' },
  { id: 'european-missions', name: 'European Missions', icon: <Satellite size={14} />, enabled: true, category: 'ORBITAL', provider: 'European Space Federation', status: 'ACTIVE', color: '#00d4ff' },

  // Earth Observation
  { id: 'recent-imagery', name: 'Recent Imagery', icon: <Eye size={14} />, enabled: false, category: 'EARTH_OBSERVATION', provider: 'Copernicus CDSE', status: 'ACTIVE', color: '#00ff88' },
  { id: 'sentinel', name: 'Sentinel', icon: <Satellite size={14} />, enabled: false, category: 'EARTH_OBSERVATION', provider: 'Copernicus', status: 'ACTIVE', color: '#00d4ff' },

  // Environment
  { id: 'earthquakes', name: 'Earthquakes', icon: <Activity size={14} />, enabled: false, category: 'ENVIRONMENT', provider: 'USGS', status: 'PORTED', color: '#ff3366' },
  { id: 'fires', name: 'Active Fires', icon: <Flame size={14} />, enabled: false, category: 'ENVIRONMENT', provider: 'NASA FIRMS', status: 'PORTED', color: '#ff6b35' },
  { id: 'fire-perimeters', name: 'Fire Perimeters', icon: <Flame size={14} />, enabled: false, category: 'ENVIRONMENT', provider: 'NIFC', status: 'REGISTERED', color: '#ffd700' },

  // Weather
  { id: 'wind', name: 'Wind', icon: <Wind size={14} />, enabled: false, category: 'WEATHER', provider: 'NOAA GFS / ECMWF', status: 'REGISTERED', color: '#00d4ff' },
  { id: 'radar', name: 'Rain Radar', icon: <Cloud size={14} />, enabled: false, category: 'WEATHER', provider: 'NOAA', status: 'REGISTERED', color: '#a855f7' },
  { id: 'clouds', name: 'Satellite Clouds', icon: <Cloud size={14} />, enabled: false, category: 'WEATHER', provider: 'NOAA GOES', status: 'REGISTERED', color: '#00d4ff' },
  { id: 'lightning', name: 'Lightning', icon: <Zap size={14} />, enabled: false, category: 'WEATHER', provider: 'NOAA', status: 'REGISTERED', color: '#ffd700' },
  { id: 'cyclones', name: 'Cyclones', icon: <Cloud size={14} />, enabled: false, category: 'WEATHER', provider: 'NHC/CPHC', status: 'REGISTERED', color: '#ff6b35' },

  // Cameras
  { id: 'cctv', name: 'Public Cameras', icon: <Camera size={14} />, enabled: false, category: 'CAMERAS', provider: 'Multiple', status: 'REGISTERED', color: '#00ff88' },
  { id: 'alpr', name: 'ALPR Infrastructure', icon: <Camera size={14} />, enabled: false, category: 'CAMERAS', provider: 'OpenStreetMap', status: 'REGISTERED', color: '#ffd700' },

  // Space Environment
  { id: 'space-weather', name: 'Space Weather', icon: <Zap size={14} />, enabled: false, category: 'SPACE_ENVIRONMENT', provider: 'ESA Space Weather', status: 'ACTIVE', color: '#ff3366' },
  { id: 'ssa', name: 'Space Safety', icon: <Shield size={14} />, enabled: false, category: 'SPACE_ENVIRONMENT', provider: 'EU SST', status: 'ACTIVE', color: '#ff6b35' },

  // Infrastructure
  { id: 'datacenters', name: 'Datacenters', icon: <Wifi size={14} />, enabled: false, category: 'INFRASTRUCTURE', provider: 'OSM', status: 'REGISTERED', color: '#00d4ff' },
  { id: 'dams', name: 'Dams', icon: <Droplet size={14} />, enabled: false, category: 'INFRASTRUCTURE', provider: 'OSM', status: 'REGISTERED', color: '#00ff88' },
];

function Rocket(props: { size: number }) {
  return (
    <svg width={props.size} height={props.size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z" />
      <path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z" />
      <path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0" />
      <path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5" />
    </svg>
  );
}

export function ControlRoomPage() {
  const [context, setContext] = useState<Context>('NEUTRAL');
  const [layers, setLayers] = useState<LayerState[]>(initialLayers);
  const [visualStyle, setVisualStyle] = useState<VisualStyle>('NORMAL');
  const [showLayers, setShowLayers] = useState(true);
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set(['ORBITAL', 'EARTH_OBSERVATION']));
  const [globeCenter, setGlobeCenter] = useState({ lon: 0, lat: 20, height: 15000000 });
  const [showFirstLaunch, setShowFirstLaunch] = useState(true);
  
  // Live entity state
  const [selectedEntity, setSelectedEntity] = useState<LiveEntity | null>(null);
  const [trackedEntityIds, setTrackedEntityIds] = useState<string[]>([]);

  // Apply context presets
  useEffect(() => {
    const contextLayers: Record<Context, string[]> = {
      NEUTRAL: [],
      LIVE_CONTACTS: ['aircraft', 'vessels', 'traffic'],
      SPACE_MISSIONS: ['satellites', 'space-missions', 'european-missions'],
      ENVIRONMENTAL: ['earthquakes', 'fires', 'wind', 'radar'],
      EUROPEAN_SPACE: ['european-missions', 'sentinel', 'recent-imagery', 'space-weather'],
      EARTH_EVENTS: ['earthquakes', 'fires', 'fire-perimeters'],
    };

    const enabled = new Set(contextLayers[context]);
    setLayers(prev => prev.map(l => ({
      ...l,
      enabled: enabled.has(l.id) || l.enabled,
    })));
  }, [context]);

  const toggleLayer = (id: string) => {
    setLayers(prev => prev.map(l => l.id === id ? { ...l, enabled: !l.enabled } : l));
  };

  const toggleCategory = (cat: string) => {
    setExpandedCategories(prev => {
      const next = new Set(prev);
      if (next.has(cat)) next.delete(cat);
      else next.add(cat);
      return next;
    });
  };

  const categories = Array.from(new Set(layers.map(l => l.category)));
  const enabledCount = layers.filter(l => l.enabled).length;

  return (
    <div className="relative w-full h-full overflow-hidden bg-earth-900">
      {/* 3D Globe */}
      <div className="absolute inset-0">
        <Globe center={globeCenter} visualStyle={visualStyle}>
          {/* Live Entity Layers */}
          {layers.find(l => l.id === 'aircraft')?.enabled && (
            <LiveEntitiesLayer
              entityType="AIRCRAFT"
              enabled={true}
              selectedEntityId={selectedEntity?.id}
              trackedEntityIds={trackedEntityIds}
              onEntityClick={setSelectedEntity}
              apiEndpoint="/api/v1/live/aircraft"
              refreshInterval={30000}
            />
          )}
          
          {layers.find(l => l.id === 'military')?.enabled && (
            <LiveEntitiesLayer
              entityType="MILITARY_AIRCRAFT"
              enabled={true}
              selectedEntityId={selectedEntity?.id}
              trackedEntityIds={trackedEntityIds}
              onEntityClick={setSelectedEntity}
              apiEndpoint="/api/v1/live/military-aircraft"
              refreshInterval={60000}
            />
          )}
          
          {layers.find(l => l.id === 'vessels')?.enabled && (
            <LiveEntitiesLayer
              entityType="VESSEL"
              enabled={true}
              selectedEntityId={selectedEntity?.id}
              trackedEntityIds={trackedEntityIds}
              onEntityClick={setSelectedEntity}
              apiEndpoint="/api/v1/live/vessels"
              refreshInterval={60000}
            />
          )}
          
          {layers.find(l => l.id === 'satellites')?.enabled && (
            <SatelliteLayer
              enabled={true}
              selectedEntityId={selectedEntity?.id}
              trackedEntityIds={trackedEntityIds}
              onEntityClick={setSelectedEntity}
              refreshInterval={60000}
            />
          )}
          
          {layers.find(l => l.id === 'earthquakes')?.enabled && (
            <EarthquakeLayer
              enabled={true}
              selectedEntityId={selectedEntity?.id}
              trackedEntityIds={trackedEntityIds}
              onEntityClick={setSelectedEntity}
              apiEndpoint="/api/v1/live/earthquakes"
              refreshInterval={300000}
            />
          )}
          
          {layers.find(l => l.id === 'fires')?.enabled && (
            <FireDetectionLayer
              enabled={true}
              selectedEntityId={selectedEntity?.id}
              trackedEntityIds={trackedEntityIds}
              onEntityClick={setSelectedEntity}
              apiEndpoint="/api/v1/live/fires"
              refreshInterval={600000}
            />
          )}
        </Globe>
      </div>

      {/* Entity Details Panel */}
      <EntityDetailsPanel
        entity={selectedEntity}
        onClose={() => setSelectedEntity(null)}
        onTrack={(id) => setTrackedEntityIds(prev => [...prev, id])}
        onUntrack={(id) => setTrackedEntityIds(prev => prev.filter(eid => eid !== id))}
        isTracked={selectedEntity ? trackedEntityIds.includes(selectedEntity.id) : false}
      />

      {/* First Launch Chooser */}
      <AnimatePresence>
        {showFirstLaunch && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 z-50 flex items-center justify-center bg-earth-900/90 backdrop-blur-sm"
          >
            <div className="max-w-2xl w-full mx-4">
              <div className="text-center mb-8">
                <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-neon-blue to-neon-green flex items-center justify-center">
                  <GlobeIcon size={32} className="text-earth-900" />
                </div>
                <h1 className="text-2xl font-bold text-white mb-2">Earth Intelligence Control Room</h1>
                <p className="text-sm text-earth-400">Choose your mission profile to configure the globe</p>
              </div>

              <div className="grid grid-cols-2 gap-3 mb-6">
                {[
                  { ctx: 'LIVE_CONTACTS' as Context, label: 'Live Contacts', icon: <Zap size={20} />, desc: 'Aircraft, vessels, traffic', color: '#00d4ff' },
                  { ctx: 'SPACE_MISSIONS' as Context, label: 'Space Missions', icon: <Satellite size={20} />, desc: 'Satellites, launches, orbits', color: '#a855f7' },
                  { ctx: 'ENVIRONMENTAL' as Context, label: 'Environmental', icon: <Activity size={20} />, desc: 'Earthquakes, fires, weather', color: '#ff6b35' },
                  { ctx: 'EUROPEAN_SPACE' as Context, label: 'European Space', icon: <Shield size={20} />, desc: 'Copernicus, ESA, EUMETSAT', color: '#00ff88' },
                ].map(option => (
                  <button
                    key={option.ctx}
                    onClick={() => { setContext(option.ctx); setShowFirstLaunch(false); }}
                    className="p-4 rounded-xl border border-earth-600/50 bg-earth-800/50 hover:bg-earth-700/50 transition-all text-left group"
                  >
                    <div className="flex items-center gap-3 mb-2">
                      <span style={{ color: option.color }}>{option.icon}</span>
                      <span className="text-sm font-semibold text-white">{option.label}</span>
                    </div>
                    <p className="text-[11px] text-earth-400">{option.desc}</p>
                  </button>
                ))}
              </div>

              <button
                onClick={() => setShowFirstLaunch(false)}
                className="w-full py-2 text-xs text-earth-400 hover:text-white transition-colors"
              >
                Explore Manually →
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Top Bar */}
      <div className="absolute top-0 left-0 right-0 z-30 flex items-center justify-between px-4 py-2 bg-gradient-to-b from-earth-900/90 to-transparent">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-earth-800/80 border border-earth-600/50">
            <GlobeIcon size={14} className="text-neon-blue" />
            <span className="text-xs font-semibold text-white">EARTH INTELLIGENCE OS</span>
            <span className="px-1.5 py-0.5 text-[9px] font-mono rounded bg-neon-blue/10 text-neon-blue">v0.1</span>
          </div>

          {/* Context Selector */}
          <div className="flex items-center gap-1 px-2 py-1 rounded-lg bg-earth-800/80 border border-earth-600/50">
            {(['NEUTRAL', 'LIVE_CONTACTS', 'SPACE_MISSIONS', 'ENVIRONMENTAL', 'EUROPEAN_SPACE'] as Context[]).map(ctx => (
              <button
                key={ctx}
                onClick={() => setContext(ctx)}
                className={`px-2 py-1 text-[10px] font-mono rounded transition-all ${
                  context === ctx ? 'bg-neon-blue/20 text-neon-blue' : 'text-earth-400 hover:text-white'
                }`}
              >
                {ctx.replace('_', ' ')}
              </button>
            ))}
          </div>
        </div>

        <div className="flex items-center gap-2">
          {/* Visual Style */}
          <div className="flex items-center gap-1 px-2 py-1 rounded-lg bg-earth-800/80 border border-earth-600/50">
            {(['NORMAL', 'NVG', 'FLIR', 'CRT'] as VisualStyle[]).map(style => (
              <button
                key={style}
                onClick={() => setVisualStyle(style)}
                className={`px-2 py-1 text-[10px] font-mono rounded transition-all ${
                  visualStyle === style ? 'bg-neon-green/20 text-neon-green' : 'text-earth-400 hover:text-white'
                }`}
              >
                {style}
              </button>
            ))}
          </div>

          {/* Status */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-earth-800/80 border border-earth-600/50">
            <div className="w-2 h-2 rounded-full bg-neon-green animate-pulse" />
            <span className="text-[10px] font-mono text-earth-300">{enabledCount} LAYERS ACTIVE</span>
          </div>
        </div>
      </div>

      {/* Layers Panel */}
      <AnimatePresence>
        {showLayers && (
          <motion.div
            initial={{ x: -300, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: -300, opacity: 0 }}
            className="absolute left-3 top-16 bottom-3 w-72 z-20 rounded-xl border border-earth-600/50 bg-earth-800/90 backdrop-blur-sm overflow-hidden flex flex-col"
          >
            <div className="p-3 border-b border-earth-600/50 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Layers size={14} className="text-neon-blue" />
                <span className="text-xs font-semibold text-white">LAYERS</span>
                <span className="text-[10px] text-earth-400 font-mono">{enabledCount}/{layers.length}</span>
              </div>
            </div>

            <div className="flex-1 overflow-y-auto p-2 space-y-1">
              {categories.map(cat => {
                const catLayers = layers.filter(l => l.category === cat);
                const isExpanded = expandedCategories.has(cat);
                return (
                  <div key={cat}>
                    <button
                      onClick={() => toggleCategory(cat)}
                      className="w-full flex items-center justify-between px-2 py-1.5 text-[10px] font-semibold text-earth-400 uppercase tracking-wider hover:text-white transition-colors"
                    >
                      <span>{cat.replace('_', ' ')}</span>
                      {isExpanded ? <ChevronDown size={12} /> : <ChevronRight size={12} />}
                    </button>
                    {isExpanded && (
                      <div className="space-y-0.5 mb-2">
                        {catLayers.map(layer => (
                          <button
                            key={layer.id}
                            onClick={() => toggleLayer(layer.id)}
                            className={`w-full flex items-center gap-2 px-2 py-1.5 rounded text-left transition-all ${
                              layer.enabled ? 'bg-earth-700/50' : 'hover:bg-earth-700/30'
                            }`}
                          >
                            <span style={{ color: layer.enabled ? layer.color : '#6b7280' }}>
                              {layer.icon}
                            </span>
                            <span className={`text-[11px] flex-1 ${layer.enabled ? 'text-white' : 'text-earth-400'}`}>
                              {layer.name}
                            </span>
                            <span className={`w-1.5 h-1.5 rounded-full ${layer.enabled ? '' : 'bg-earth-600'}`} style={layer.enabled ? { backgroundColor: layer.color } : {}} />
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Toggle Layers Button */}
      <button
        onClick={() => setShowLayers(!showLayers)}
        className="absolute left-3 top-16 z-10 w-8 h-8 rounded-lg bg-earth-800/80 border border-earth-600/50 flex items-center justify-center text-earth-400 hover:text-white transition-colors"
        style={{ display: showLayers ? 'none' : 'flex' }}
      >
        <Layers size={14} />
      </button>

      {/* Bottom Bar - Attribution & Provider Status */}
      <div className="absolute bottom-0 left-0 right-0 z-30 flex items-center justify-between px-4 py-2 bg-gradient-to-t from-earth-900/90 to-transparent">
        <div className="flex items-center gap-3 text-[10px] text-earth-400">
          <span>© OpenStreetMap contributors</span>
          <span>•</span>
          <span>Powered by Esri</span>
          <span>•</span>
          <span>European Space Federation: 10 providers</span>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowFirstLaunch(true)}
            className="px-2 py-1 text-[10px] text-earth-400 hover:text-white rounded bg-earth-800/50 border border-earth-600/30"
          >
            Reset Mission
          </button>
          <button className="px-2 py-1 text-[10px] text-earth-400 hover:text-white rounded bg-earth-800/50 border border-earth-600/30 flex items-center gap-1">
            <Settings size={10} />
            Providers
          </button>
        </div>
      </div>

      {/* Ask Earth Button */}
      <div className="absolute bottom-16 right-4 z-30">
        <button className="px-4 py-2 rounded-xl bg-gradient-to-r from-neon-blue to-neon-green text-earth-900 text-xs font-bold shadow-lg hover:shadow-xl transition-all flex items-center gap-2">
          <span>🌍</span>
          <span>ASK EARTH</span>
        </button>
      </div>
    </div>
  );
}
