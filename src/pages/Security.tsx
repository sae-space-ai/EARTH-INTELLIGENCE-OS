import { motion } from 'framer-motion';
import { threatModelItems } from '../data/platform';
import { Shield, AlertTriangle, Lock, ArrowRight, Eye } from 'lucide-react';

const container = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.05 } } };
const item = { hidden: { opacity: 0, y: 15 }, show: { opacity: 1, y: 0 } };

const riskColors: Record<string, string> = {
  critical: '#ff3366',
  high: '#ff6b35',
  medium: '#ffd700',
  low: '#00ff88',
};

const controlStatusColors: Record<string, string> = {
  active: '#00ff88',
  designed: '#00d4ff',
  planned: '#ffd700',
  future: '#6b7280',
};

export function SecurityPage() {
  return (
    <motion.div variants={container} initial="hidden" animate="show" className="space-y-6">
      {/* Header */}
      <motion.div variants={item} className="rounded-xl border border-neon-red/20 bg-neon-red/5 p-6">
        <div className="flex items-center gap-3 mb-4">
          <Shield size={20} className="text-neon-red" />
          <h3 className="text-lg font-semibold text-white">Security & Threat Model</h3>
        </div>
        <p className="text-xs text-earth-400">
          Comprehensive threat identification and mitigation strategy for Earth Intelligence OS.
          Security is designed into the architecture from the ground up.
        </p>
      </motion.div>

      {/* Critical Boundary */}
      <motion.div variants={item} className="rounded-xl border border-neon-red/30 bg-earth-800/50 p-6">
        <div className="flex items-center gap-3 mb-4">
          <Lock size={18} className="text-neon-red" />
          <h3 className="text-sm font-bold text-neon-red">CRITICAL: AI/Command Boundary (ADR-008)</h3>
        </div>
        <p className="text-xs text-earth-300 mb-4">
          Generative AI has NO direct network path to spacecraft actuators. This is a hard architectural
          boundary enforced at the network, application, and policy levels.
        </p>
        <div className="flex flex-wrap items-center gap-2">
          {[
            { label: 'AI Layer', color: '#a855f7', desc: 'Analyze & Propose' },
            { label: 'Mission Planner', color: '#00d4ff', desc: 'Plan & Validate' },
            { label: 'Digital Twin', color: '#00ff88', desc: 'Simulate' },
            { label: 'Policy Engine', color: '#ffd700', desc: 'Enforce Rules' },
            { label: 'Human Auth', color: '#ff6b35', desc: 'Approve/Reject' },
            { label: 'Flight Ops', color: '#00d4ff', desc: 'Execute' },
            { label: 'Uplink', color: '#ff3366', desc: 'Transmit' },
            { label: 'Spacecraft', color: '#ef4444', desc: 'Actuate' },
          ].map((step, i) => (
            <div key={step.label} className="flex items-center gap-2">
              <div className="px-3 py-2 rounded-lg border text-center min-w-[80px]" style={{ borderColor: `${step.color}40`, backgroundColor: `${step.color}10` }}>
                <div className="text-[10px] font-bold" style={{ color: step.color }}>{step.label}</div>
                <div className="text-[8px] text-earth-400">{step.desc}</div>
              </div>
              {i < 7 && <ArrowRight size={12} className="text-earth-500" />}
            </div>
          ))}
        </div>
        <div className="mt-4 p-3 rounded-lg bg-neon-red/10 border border-neon-red/20">
          <p className="text-[11px] text-neon-red font-semibold">
            ⚠️ NO DIRECT PATH exists between AI Layer and Flight Ops/Uplink/Spacecraft.
            All proposals must traverse the full chain with human authorization.
          </p>
        </div>
      </motion.div>

      {/* Threat Model Table */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">Threat Register</h3>
        <div className="space-y-2">
          {threatModelItems.map((threat) => (
            <div
              key={threat.threat}
              className="flex items-center gap-4 p-3 rounded-lg bg-earth-700/20 border border-earth-600/20"
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-semibold text-white">{threat.threat}</span>
                  <span
                    className="px-1.5 py-0.5 text-[8px] font-bold font-mono rounded uppercase"
                    style={{
                      color: riskColors[threat.risk],
                      backgroundColor: `${riskColors[threat.risk]}15`,
                    }}
                  >
                    {threat.risk}
                  </span>
                </div>
                <p className="text-[10px] text-earth-400 truncate">{threat.control}</p>
              </div>
              <span
                className="px-2 py-0.5 text-[9px] font-mono rounded-full border flex-shrink-0"
                style={{
                  color: controlStatusColors[threat.status],
                  borderColor: `${controlStatusColors[threat.status]}40`,
                  backgroundColor: `${controlStatusColors[threat.status]}10`,
                }}
              >
                {threat.status}
              </span>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Security Controls */}
      <motion.div variants={item} className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-5">
          <h4 className="text-xs font-semibold text-neon-green uppercase tracking-wider mb-3">Active Controls</h4>
          <ul className="space-y-2">
            {[
              'Immutable raw data policy (SHA-256)',
              'No hardcoded secrets in codebase',
              'Pre-commit secret detection',
              'Structured audit logging',
              'AI/command boundary enforced',
              '.env.example without real secrets',
              'Typed configuration validation',
            ].map(c => (
              <li key={c} className="flex items-center gap-2 text-[11px] text-earth-300">
                <div className="w-1.5 h-1.5 rounded-full bg-neon-green" />
                {c}
              </li>
            ))}
          </ul>
        </div>
        <div className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-5">
          <h4 className="text-xs font-semibold text-neon-yellow uppercase tracking-wider mb-3">Planned Controls</h4>
          <ul className="space-y-2">
            {[
              'Vault integration for secrets',
              'mTLS between services',
              'RBAC/IAM system',
              'WAF / Rate limiting',
              'Dependency vulnerability scanning',
              'SBOM generation',
              'Encryption at rest (DB + S3)',
              'Model checkpoint signing',
              'Prompt injection defenses',
              'Supply chain verification',
            ].map(c => (
              <li key={c} className="flex items-center gap-2 text-[11px] text-earth-300">
                <div className="w-1.5 h-1.5 rounded-full bg-neon-yellow" />
                {c}
              </li>
            ))}
          </ul>
        </div>
      </motion.div>

      {/* Audit Model */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">Audit Record Model</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 rounded-lg bg-earth-900/50 border border-earth-600/30 font-mono text-[11px]">
            <div className="text-neon-green mb-2"># AuditRecord</div>
            <div className="space-y-0.5 text-earth-300">
              <div><span className="text-neon-blue">actor_type</span>: enum  <span className="text-earth-500"># user|system|ai|service</span></div>
              <div><span className="text-neon-blue">actor_id</span>: str</div>
              <div><span className="text-neon-blue">action</span>: str  <span className="text-earth-500"># e.g., "observation.create"</span></div>
              <div><span className="text-neon-blue">resource_type</span>: str</div>
              <div><span className="text-neon-blue">resource_id</span>: UUID</div>
              <div><span className="text-neon-blue">timestamp</span>: datetime</div>
              <div><span className="text-neon-blue">trace_id</span>: UUID</div>
              <div><span className="text-neon-blue">metadata</span>: dict</div>
            </div>
          </div>
          <div className="p-4 rounded-lg bg-earth-700/20 border border-earth-600/30">
            <h5 className="text-xs font-semibold text-white mb-2">Distinction</h5>
            <div className="space-y-2">
              <div className="p-2 rounded bg-earth-800/50">
                <div className="text-[10px] font-bold text-neon-blue mb-1">Operational Logs</div>
                <div className="text-[10px] text-earth-400">System behavior, debugging, performance</div>
              </div>
              <div className="p-2 rounded bg-earth-800/50">
                <div className="text-[10px] font-bold text-neon-red mb-1">Security Audit</div>
                <div className="text-[10px] text-earth-400">Who did what, when, to which resource</div>
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}
