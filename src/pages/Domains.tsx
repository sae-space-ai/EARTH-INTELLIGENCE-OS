import { motion } from 'framer-motion';
import { domains } from '../data/platform';
import { useState } from 'react';

const container = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.05 } } };
const item = { hidden: { opacity: 0, y: 20 }, show: { opacity: 1, y: 0 } };

export function DomainsPage() {
  const [selected, setSelected] = useState<string | null>(null);
  const active = domains.find(d => d.id === selected);

  return (
    <motion.div variants={container} initial="hidden" animate="show" className="space-y-6">
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-2">Bounded Contexts</h3>
        <p className="text-xs text-earth-400 mb-6">
          Earth Intelligence OS is organized into 8 bounded contexts, each with clear responsibilities,
          entities, and interfaces. Click a domain to explore its details.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {domains.map(domain => (
            <motion.button
              key={domain.id}
              variants={item}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setSelected(selected === domain.id ? null : domain.id)}
              className={`text-left p-5 rounded-xl border transition-all duration-200 ${
                selected === domain.id
                  ? 'border-opacity-50 bg-opacity-10'
                  : 'border-earth-600/30 bg-earth-700/20 hover:bg-earth-700/40'
              }`}
              style={selected === domain.id ? { borderColor: domain.color, backgroundColor: `${domain.color}10` } : {}}
            >
              <div className="flex items-center gap-3 mb-3">
                <span className="text-3xl">{domain.icon}</span>
                <div>
                  <h4 className="text-sm font-bold text-white">{domain.name}</h4>
                  <p className="text-[10px] font-mono" style={{ color: domain.color }}>{domain.id}</p>
                </div>
              </div>
              <p className="text-xs text-earth-400 leading-relaxed">{domain.description}</p>
            </motion.button>
          ))}
        </div>
      </motion.div>

      {/* Domain Detail */}
      {active && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="rounded-xl border bg-earth-800/50 p-6"
          style={{ borderColor: `${active.color}40` }}
        >
          <div className="flex items-center gap-3 mb-6">
            <span className="text-4xl">{active.icon}</span>
            <div>
              <h3 className="text-xl font-bold text-white">{active.name} Domain</h3>
              <p className="text-xs font-mono" style={{ color: active.color }}>{active.id}</p>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Entities */}
            <div>
              <h4 className="text-xs font-semibold text-earth-300 uppercase tracking-wider mb-3">Entities</h4>
              <div className="space-y-2">
                {active.entities.map(entity => (
                  <div key={entity} className="flex items-center gap-3 p-3 rounded-lg bg-earth-700/30 border border-earth-600/30">
                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: active.color }} />
                    <code className="text-xs font-mono text-white">{entity}</code>
                  </div>
                ))}
              </div>
            </div>

            {/* Responsibilities */}
            <div>
              <h4 className="text-xs font-semibold text-earth-300 uppercase tracking-wider mb-3">Responsibilities</h4>
              <div className="space-y-2">
                {active.responsibilities.map(resp => (
                  <div key={resp} className="flex items-start gap-3 p-3 rounded-lg bg-earth-700/30 border border-earth-600/30">
                    <div className="w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0" style={{ backgroundColor: active.color }} />
                    <span className="text-xs text-earth-300">{resp}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </motion.div>
      )}

      {/* Entity Model Summary */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">Core Domain Models</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[
            { name: 'Satellite', fields: ['id: UUID', 'name: str', 'platform_type: enum', 'status: enum', 'created_at: datetime'], color: '#00ff88' },
            { name: 'Sensor', fields: ['id: UUID', 'satellite_id: UUID', 'sensor_type: enum', 'name: str', 'status: enum', 'metadata: dict'], color: '#00d4ff' },
            { name: 'Observation', fields: ['id: UUID', 'satellite_id: UUID', 'sensor_id: UUID', 'acquired_at: datetime', 'footprint: Geometry', 'bbox: BBox', 'processing_level: str', 'quality_score: float'], color: '#a855f7' },
            { name: 'EarthEvent', fields: ['id: UUID', 'event_type: str', 'geometry: Geometry', 'first_seen: datetime', 'last_seen: datetime', 'confidence: float', 'priority: int', 'knowledge_state: enum'], color: '#ff6b35' },
            { name: 'MissionRequest', fields: ['id: UUID', 'aoi: Geometry', 'priority: int', 'requested_by: str', 'status: enum', 'created_at: datetime'], color: '#ff3366' },
            { name: 'ModelVersion', fields: ['id: UUID', 'model_name: str', 'semantic_version: str', 'git_commit: str', 'framework: str', 'checkpoint_uri: str', 'checkpoint_sha256: str', 'status: enum'], color: '#ffd700' },
          ].map(model => (
            <div key={model.name} className="p-4 rounded-lg border border-earth-600/30 bg-earth-700/20">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: model.color }} />
                <code className="text-xs font-bold text-white">{model.name}</code>
              </div>
              <div className="space-y-1">
                {model.fields.map(f => (
                  <div key={f} className="text-[10px] font-mono text-earth-400">{f}</div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* IDs Convention */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">ID Convention</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-2">
          {['satellite_id', 'sensor_id', 'observation_id', 'asset_id', 'earth_event_id', 'mission_id', 'model_version_id', 'dataset_version_id', 'trace_id', 'correlation_id'].map(id => (
            <code key={id} className="px-2 py-1.5 text-[10px] font-mono rounded bg-earth-700/50 text-neon-blue border border-earth-600/30 text-center">
              {id}
            </code>
          ))}
        </div>
        <p className="text-[11px] text-earth-400 mt-3">All internal IDs use UUID v4. Conceptual IDs follow the naming convention above for traceability.</p>
      </motion.div>
    </motion.div>
  );
}
