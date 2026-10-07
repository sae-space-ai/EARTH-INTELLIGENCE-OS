import { motion } from 'framer-motion';
import { knowledgeStates } from '../data/platform';
import { Brain, Eye, Shield, Zap } from 'lucide-react';

const container = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.06 } } };
const item = { hidden: { opacity: 0, y: 20 }, show: { opacity: 1, y: 0 } };

export function KnowledgePage() {
  return (
    <motion.div variants={container} initial="hidden" animate="show" className="space-y-6">
      {/* Header */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <div className="flex items-center gap-3 mb-4">
          <Brain size={20} className="text-neon-purple" />
          <h3 className="text-lg font-semibold text-white">Knowledge State Classification</h3>
          <span className="px-2 py-0.5 text-[10px] font-mono rounded-full bg-neon-purple/10 text-neon-purple border border-neon-purple/20">
            ADR-009
          </span>
        </div>
        <p className="text-xs text-earth-400">
          Every piece of knowledge produced by the platform carries an explicit epistemic classification.
          This prevents silent confusion between observations, inferences, forecasts, and simulations.
          Users can always determine the confidence level and source of any information.
        </p>
      </motion.div>

      {/* Knowledge States */}
      <motion.div variants={item} className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {knowledgeStates.map((ks) => (
          <motion.div
            key={ks.state}
            whileHover={{ scale: 1.02 }}
            className="rounded-xl border p-6 transition-all"
            style={{ borderColor: `${ks.color}40`, backgroundColor: `${ks.color}08` }}
          >
            <div className="flex items-center gap-3 mb-4">
              <span className="text-4xl">{ks.icon}</span>
              <div>
                <h4 className="text-lg font-bold font-mono" style={{ color: ks.color }}>{ks.state}</h4>
                <p className="text-xs text-earth-400">{ks.description}</p>
              </div>
            </div>
            <div className="space-y-2">
              {ks.state === 'OBSERVED' && (
                <>
                  <InfoRow label="Source" value="Direct sensor measurement" color={ks.color} />
                  <InfoRow label="Confidence" value="Highest — empirical data" color={ks.color} />
                  <InfoRow label="Examples" value="Raw satellite imagery, telemetry, LiDAR point clouds" color={ks.color} />
                  <InfoRow label="Immutability" value="RAW data is evidence — never modified" color={ks.color} />
                </>
              )}
              {ks.state === 'INFERRED' && (
                <>
                  <InfoRow label="Source" value="Model analysis of observations" color={ks.color} />
                  <InfoRow label="Confidence" value="High — includes uncertainty estimate" color={ks.color} />
                  <InfoRow label="Examples" value="Land classification, change magnitude, anomaly scores" color={ks.color} />
                  <InfoRow label="Traceability" value="Linked to model version + input observations" color={ks.color} />
                </>
              )}
              {ks.state === 'FORECAST' && (
                <>
                  <InfoRow label="Source" value="Predictive model + trends" color={ks.color} />
                  <InfoRow label="Confidence" value="Medium — degrades with horizon" color={ks.color} />
                  <InfoRow label="Examples" value="Future land cover, flood risk, deforestation trajectory" color={ks.color} />
                  <InfoRow label="Validation" value="Backtested against historical observations" color={ks.color} />
                </>
              )}
              {ks.state === 'SIMULATED' && (
                <>
                  <InfoRow label="Source" value="Digital Twin / World Model" color={ks.color} />
                  <InfoRow label="Confidence" value="Scenario-dependent — for planning" color={ks.color} />
                  <InfoRow label="Examples" value="Mission simulation outcomes, what-if scenarios" color={ks.color} />
                  <InfoRow label="Purpose" value="Planning, validation, gap identification" color={ks.color} />
                </>
              )}
            </div>
          </motion.div>
        ))}
      </motion.div>

      {/* Rules */}
      <motion.div variants={item} className="rounded-xl border border-neon-purple/30 bg-neon-purple/5 p-6">
        <h3 className="text-sm font-semibold text-neon-purple mb-4">Classification Rules</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-3">
            <RuleItem text="All domain entities carrying knowledge MUST include knowledge_state field" />
            <RuleItem text="States MUST NOT be mixed silently in the same response without clear labeling" />
            <RuleItem text="UI MUST visually distinguish between states (color, icon, badge)" />
            <RuleItem text="APIs MUST support filtering by knowledge_state" />
          </div>
          <div className="space-y-3">
            <RuleItem text="Transitions between states require explicit operation (e.g., OBSERVED → INFERRED)" />
            <RuleItem text="FORECAST entities must include forecast_horizon and model_version" />
            <RuleItem text="SIMULATED entities must reference their simulation run" />
            <RuleItem text="Provenance records link all states back to their origin" />
          </div>
        </div>
      </motion.div>

      {/* Model Registry */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">Model Version Lifecycle</h3>
        <div className="flex flex-wrap items-center gap-3 py-2">
          {[
            { state: 'REGISTERED', color: '#6b7280' },
            { state: 'VALIDATING', color: '#ffd700' },
            { state: 'VALIDATED', color: '#00d4ff' },
            { state: 'PROMOTED', color: '#00ff88' },
            { state: 'DEPLOYED', color: '#a855f7' },
            { state: 'RETIRED', color: '#ff3366' },
          ].map((s, i) => (
            <div key={s.state} className="flex items-center gap-3">
              <div className="px-3 py-2 rounded-lg border text-center" style={{ borderColor: `${s.color}40`, backgroundColor: `${s.color}10` }}>
                <div className="text-[10px] font-bold font-mono" style={{ color: s.color }}>{s.state}</div>
              </div>
              {i < 5 && <ArrowRight size={14} className="text-earth-500" />}
            </div>
          ))}
        </div>
        <div className="mt-4 p-3 rounded-lg bg-earth-700/20 border border-earth-600/30">
          <p className="text-[11px] text-earth-400">
            <strong className="text-white">Rejected</strong> models are also tracked (status: REJECTED) with failure reasons.
            No model is used for inference without passing through VALIDATED → PROMOTED → DEPLOYED.
          </p>
        </div>
      </motion.div>

      {/* Latent Representation */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">Latent Representation (Future)</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 rounded-lg bg-earth-900/50 border border-earth-600/30 font-mono text-[11px]">
            <div className="text-neon-green mb-2"># LatentRepresentation</div>
            <div className="space-y-0.5 text-earth-300">
              <div><span className="text-neon-blue">embedding</span>: float[] <span className="text-earth-500"># target: 256 dims</span></div>
              <div><span className="text-neon-blue">embedding_dim</span>: int</div>
              <div><span className="text-neon-blue">model_version</span>: ModelVersion</div>
              <div><span className="text-neon-blue">modalities</span>: str[] <span className="text-earth-500"># e.g., ["optical", "SAR"]</span></div>
              <div><span className="text-neon-blue">quality_metadata</span>: dict</div>
              <div><span className="text-neon-blue">created_at</span>: datetime</div>
            </div>
          </div>
          <div className="p-4 rounded-lg bg-earth-700/20 border border-earth-600/30">
            <h5 className="text-xs font-semibold text-white mb-3">ML Interfaces (Future)</h5>
            <div className="space-y-3">
              <div className="p-2 rounded bg-earth-800/50">
                <code className="text-[10px] text-neon-blue">encode(observation) → LatentRepresentation</code>
                <p className="text-[9px] text-earth-400 mt-1">Generate embedding from observation</p>
              </div>
              <div className="p-2 rounded bg-earth-800/50">
                <code className="text-[10px] text-neon-green">analyze(embeddings) → AnalysisResult</code>
                <p className="text-[9px] text-earth-400 mt-1">Run analysis on embedding set</p>
              </div>
            </div>
            <p className="text-[10px] text-earth-400 mt-3 italic">
              No fake outputs. Interfaces defined for Phase 3+ implementation.
            </p>
          </div>
        </div>
      </motion.div>

      {/* STAC Mapping */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">STAC Item Mapping (ADR-007)</h3>
        <div className="p-4 rounded-lg bg-earth-900/50 border border-earth-600/30 font-mono text-[11px]">
          <div className="text-neon-green mb-2"># Observation → STAC Item</div>
          <div className="space-y-0.5 text-earth-300">
            <div><span className="text-neon-blue">type</span>: "Feature"</div>
            <div><span className="text-neon-blue">stac_version</span>: "1.0.0"</div>
            <div><span className="text-neon-blue">id</span>: observation.id</div>
            <div><span className="text-neon-blue">geometry</span>: observation.footprint (GeoJSON)</div>
            <div><span className="text-neon-blue">bbox</span>: observation.bbox</div>
            <div><span className="text-neon-blue">properties</span>:</div>
            <div className="pl-4">datetime: observation.acquired_at</div>
            <div className="pl-4">platform: sensor.satellite.name</div>
            <div className="pl-4">instruments: [sensor.name]</div>
            <div className="pl-4">processing_level: observation.processing_level</div>
            <div className="pl-4">quality_score: observation.quality_score</div>
            <div className="pl-4">knowledge_state: observation.knowledge_state</div>
            <div><span className="text-neon-blue">assets</span>:</div>
            <div className="pl-4">raw: {'{ href, type, checksum }'}</div>
            <div className="pl-4">processed: {'{ href, type, checksum }'} (if exists)</div>
            <div><span className="text-neon-blue">links</span>: [self, parent, root, collection]</div>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}

function InfoRow({ label, value, color }: { label: string; value: string; color: string }) {
  return (
    <div className="flex items-start gap-2">
      <span className="text-[10px] font-semibold uppercase tracking-wider flex-shrink-0 w-24" style={{ color }}>{label}</span>
      <span className="text-[11px] text-earth-300">{value}</span>
    </div>
  );
}

function RuleItem({ text }: { text: string }) {
  return (
    <div className="flex items-start gap-2 p-2 rounded bg-earth-700/20">
      <Shield size={12} className="text-neon-purple mt-0.5 flex-shrink-0" />
      <span className="text-[11px] text-earth-300">{text}</span>
    </div>
  );
}

function ArrowRight(props: { size: number; className: string }) {
  return (
    <svg width={props.size} height={props.size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={props.className}>
      <path d="M5 12h14M12 5l7 7-7 7" />
    </svg>
  );
}
