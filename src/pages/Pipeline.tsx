import { motion } from 'framer-motion';
import { observationPipeline } from '../data/platform';
import { Activity, ArrowRight, CheckCircle2, Clock, Circle } from 'lucide-react';

const container = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.08 } } };
const item = { hidden: { opacity: 0, x: -20 }, show: { opacity: 1, x: 0 } };

const statusConfig = {
  active: { color: '#00ff88', icon: <CheckCircle2 size={14} />, bg: 'bg-neon-green/10', border: 'border-neon-green/30' },
  planned: { color: '#ffd700', icon: <Clock size={14} />, bg: 'bg-neon-yellow/10', border: 'border-neon-yellow/30' },
  future: { color: '#6b7280', icon: <Circle size={14} />, bg: 'bg-earth-700/30', border: 'border-earth-600/30' },
};

export function PipelinePage() {
  return (
    <motion.div variants={container} initial="hidden" animate="show" className="space-y-6">
      {/* Header */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <div className="flex items-center gap-3 mb-4">
          <Activity size={20} className="text-neon-orange" />
          <h3 className="text-lg font-semibold text-white">Observation Processing Pipeline</h3>
        </div>
        <p className="text-xs text-earth-400">
          Each observation flows through a series of processing stages. Each stage produces a versioned
          event and may create derived assets. All transformations are tracked via provenance records.
        </p>
      </motion.div>

      {/* Pipeline Visualization */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-6">Pipeline Stages</h3>
        <div className="space-y-4">
          {observationPipeline.map((stage, i) => {
            const config = statusConfig[stage.status];
            return (
              <motion.div key={stage.name} variants={item} className="relative">
                <div className={`flex items-stretch gap-4 p-4 rounded-lg border ${config.border} ${config.bg}`}>
                  {/* Stage number */}
                  <div className="flex flex-col items-center justify-center w-10">
                    <div
                      className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold"
                      style={{ backgroundColor: `${config.color}20`, color: config.color }}
                    >
                      {i + 1}
                    </div>
                    {i < observationPipeline.length - 1 && (
                      <div className="w-0.5 flex-1 mt-2" style={{ backgroundColor: `${config.color}30` }} />
                    )}
                  </div>

                  {/* Content */}
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-1">
                      <h4 className="text-sm font-bold text-white">{stage.name}</h4>
                      <span className="flex items-center gap-1" style={{ color: config.color }}>
                        {config.icon}
                        <span className="text-[9px] font-mono uppercase">{stage.status}</span>
                      </span>
                    </div>
                    <p className="text-[11px] text-earth-400 mb-2">{stage.description}</p>
                    <code className="text-[10px] font-mono px-2 py-0.5 rounded bg-earth-900/50 text-neon-blue">
                      → {stage.event}
                    </code>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </motion.div>

      {/* Asset Transformation Chain */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">Asset Transformation Chain</h3>
        <div className="flex flex-wrap items-center gap-3 py-2">
          {[
            { label: 'RAW', desc: 'Immutable evidence', color: '#ff3366' },
            { label: 'CALIBRATED', desc: 'Radiometric correction', color: '#ff6b35' },
            { label: 'GEOREFERENCED', desc: 'Spatial alignment', color: '#ffd700' },
            { label: 'ALIGNED', desc: 'Coregistered to grid', color: '#00ff88' },
            { label: 'DERIVED', desc: 'Products & analysis', color: '#00d4ff' },
          ].map((asset, i) => (
            <div key={asset.label} className="flex items-center gap-3">
              <div className="px-4 py-3 rounded-lg border text-center" style={{ borderColor: `${asset.color}40`, backgroundColor: `${asset.color}10` }}>
                <div className="text-xs font-bold font-mono" style={{ color: asset.color }}>{asset.label}</div>
                <div className="text-[9px] text-earth-400 mt-0.5">{asset.desc}</div>
              </div>
              {i < 4 && <ArrowRight size={16} className="text-earth-500" />}
            </div>
          ))}
        </div>
        <div className="mt-4 p-3 rounded-lg bg-neon-red/5 border border-neon-red/20">
          <p className="text-[11px] text-neon-red">
            <strong>⚠ RAW DATA IS EVIDENCE.</strong> Raw assets are immutable after creation.
            No silent overwrites. Every transformation creates a new asset with provenance linking back to inputs.
          </p>
        </div>
      </motion.div>

      {/* Provenance */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">Provenance Record</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 rounded-lg bg-earth-900/50 border border-earth-600/30 font-mono text-[11px]">
            <div className="text-neon-green mb-2"># ProvenanceRecord</div>
            <div className="space-y-0.5 text-earth-300">
              <div><span className="text-neon-blue">input_asset_ids</span>: UUID[]</div>
              <div><span className="text-neon-blue">output_asset_ids</span>: UUID[]</div>
              <div><span className="text-neon-blue">operation</span>: str</div>
              <div><span className="text-neon-blue">software_version</span>: str</div>
              <div><span className="text-neon-blue">model_version_id</span>: UUID | null</div>
              <div><span className="text-neon-blue">parameters_hash</span>: str</div>
              <div><span className="text-neon-blue">started_at</span>: datetime</div>
              <div><span className="text-neon-blue">finished_at</span>: datetime</div>
              <div><span className="text-neon-blue">trace_id</span>: UUID</div>
            </div>
          </div>
          <div className="p-4 rounded-lg bg-earth-700/20 border border-earth-600/30">
            <h5 className="text-xs font-semibold text-white mb-3">Provenance Guarantees</h5>
            <ul className="space-y-2">
              {[
                'Every derived asset traces to its inputs',
                'Software version recorded for reproducibility',
                'Parameters hashed for integrity verification',
                'Model version linked when ML is involved',
                'Full trace_id for distributed tracing',
                'Timeline of processing (start → finish)',
              ].map(g => (
                <li key={g} className="flex items-start gap-2 text-[11px] text-earth-300">
                  <div className="w-1.5 h-1.5 rounded-full bg-neon-green mt-1 flex-shrink-0" />
                  {g}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </motion.div>

      {/* Storage */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">Object Storage (S3-Compatible)</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 rounded-lg bg-earth-700/20 border border-earth-600/30">
            <h5 className="text-xs font-semibold text-neon-blue mb-2">StorageClient API</h5>
            <ul className="space-y-1 text-[10px] font-mono text-earth-300">
              <li>upload_file(path, bucket, key)</li>
              <li>put_bytes(data, bucket, key)</li>
              <li>get_bytes(bucket, key)</li>
              <li>exists(bucket, key)</li>
              <li>get_metadata(bucket, key)</li>
            </ul>
          </div>
          <div className="p-4 rounded-lg bg-earth-700/20 border border-earth-600/30">
            <h5 className="text-xs font-semibold text-neon-green mb-2">Asset Metadata</h5>
            <ul className="space-y-1 text-[10px] font-mono text-earth-300">
              <li>bucket: str</li>
              <li>key: str</li>
              <li>size: int</li>
              <li>content_type: str</li>
              <li>sha256: str</li>
              <li>created_at: datetime</li>
            </ul>
          </div>
          <div className="p-4 rounded-lg bg-earth-700/20 border border-earth-600/30">
            <h5 className="text-xs font-semibold text-neon-yellow mb-2">Infrastructure</h5>
            <ul className="space-y-1 text-[10px] text-earth-300">
              <li>• MinIO (local development)</li>
              <li>• S3/GCS (production)</li>
              <li>• SHA-256 checksums</li>
              <li>• Immutable raw data</li>
              <li>• Versioned buckets</li>
            </ul>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}
