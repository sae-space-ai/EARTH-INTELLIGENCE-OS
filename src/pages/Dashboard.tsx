import { motion } from 'framer-motion';
import {
  Satellite, Eye, Brain, Target, Database, Radio,
  Shield, Zap, CheckCircle2, Clock, AlertTriangle,
  ArrowRight, Globe, Cpu, Lock
} from 'lucide-react';
import { domains, roadmapPhases, knowledgeStates } from '../data/platform';

const container = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.05 } }
};
const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};

export function Dashboard() {
  return (
    <motion.div variants={container} initial="hidden" animate="show" className="space-y-6">
      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-2xl border border-earth-600/50 bg-gradient-to-br from-earth-800 to-earth-900 p-8">
        <div className="absolute inset-0 grid-bg opacity-50" />
        <div className="absolute top-0 right-0 w-96 h-96 bg-neon-blue/5 rounded-full blur-3xl" />
        <div className="absolute bottom-0 left-0 w-64 h-64 bg-neon-purple/5 rounded-full blur-3xl" />
        <div className="relative z-10">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-neon-blue to-neon-green flex items-center justify-center">
              <Globe size={24} className="text-earth-900" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">Earth Intelligence OS</h1>
              <p className="text-sm text-earth-400">Planetary-scale intelligence platform — Phase 0 Foundation</p>
            </div>
          </div>
          <p className="text-earth-300 max-w-2xl leading-relaxed mb-6">
            Building the foundations for a system that observes, understands, and protects our planet.
            Integrating satellite constellations, foundation models, planetary memory, and autonomous intelligence
            into a unified Earth observation and response platform.
          </p>
          <div className="flex flex-wrap gap-3">
            <StatusBadge label="Foundation" status="building" color="#00d4ff" />
            <StatusBadge label="Infrastructure" status="ready" color="#00ff88" />
            <StatusBadge label="Domain Models" status="ready" color="#a855f7" />
            <StatusBadge label="Event System" status="ready" color="#ffd700" />
            <StatusBadge label="API Layer" status="ready" color="#ff6b35" />
          </div>
        </div>
      </div>

      {/* System Cycle */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">Intelligence Cycle</h3>
        <div className="flex flex-wrap gap-2">
          {[
            'OBSERVE', 'GEOLOCALIZE', 'PROCESS', 'FUSE', 'UNDERSTAND',
            'REMEMBER', 'DETECT CHANGE', 'ESTIMATE UNCERTAINTY', 'FORECAST',
            'IDENTIFY GAP', 'PLAN OBSERVATION', 'SIMULATE', 'AUTHORIZE',
            'OBSERVE AGAIN', 'LEARN'
          ].map((step, i) => (
            <div key={step} className="flex items-center gap-2">
              <span className="px-3 py-1.5 text-xs font-mono rounded-lg bg-earth-700/50 border border-earth-600/50 text-earth-200">
                {step}
              </span>
              {i < 14 && <ArrowRight size={12} className="text-earth-500" />}
            </div>
          ))}
        </div>
      </motion.div>

      {/* Domain Overview */}
      <motion.div variants={item}>
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">Bounded Contexts</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {domains.map((domain) => (
            <motion.div
              key={domain.id}
              whileHover={{ scale: 1.02, y: -2 }}
              className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-4 cursor-pointer group"
            >
              <div className="flex items-center gap-3 mb-3">
                <span className="text-2xl">{domain.icon}</span>
                <div>
                  <h4 className="text-sm font-semibold text-white">{domain.name}</h4>
                  <p className="text-[10px] text-earth-400 font-mono">{domain.entities.length} entities</p>
                </div>
              </div>
              <p className="text-xs text-earth-400 leading-relaxed line-clamp-2">{domain.description}</p>
              <div className="mt-3 flex flex-wrap gap-1">
                {domain.entities.slice(0, 3).map(e => (
                  <span key={e} className="px-1.5 py-0.5 text-[9px] font-mono rounded bg-earth-700/50 text-earth-300">
                    {e}
                  </span>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Knowledge States */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">Knowledge State Classification</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {knowledgeStates.map((ks) => (
            <div key={ks.state} className="flex items-start gap-3 p-3 rounded-lg bg-earth-700/30 border border-earth-600/30">
              <span className="text-xl">{ks.icon}</span>
              <div>
                <div className="text-xs font-bold font-mono" style={{ color: ks.color }}>{ks.state}</div>
                <p className="text-[11px] text-earth-400 mt-1">{ks.description}</p>
              </div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Key Metrics */}
      <motion.div variants={item} className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MetricCard icon={<Database size={20} />} label="Domain Entities" value="11" color="#00d4ff" />
        <MetricCard icon={<Radio size={20} />} label="Event Topics" value="26" color="#ffd700" />
        <MetricCard icon={<Shield size={20} />} label="ADRs" value="12" color="#00ff88" />
        <MetricCard icon={<Target size={20} />} label="Roadmap Phases" value="14" color="#a855f7" />
      </motion.div>

      {/* Security Boundary */}
      <motion.div variants={item} className="rounded-xl border border-neon-red/20 bg-neon-red/5 p-6">
        <div className="flex items-start gap-4">
          <div className="w-10 h-10 rounded-lg bg-neon-red/10 flex items-center justify-center flex-shrink-0">
            <Lock size={20} className="text-neon-red" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-neon-red mb-2">Critical Safety Boundary — ADR-008</h3>
            <p className="text-xs text-earth-300 leading-relaxed mb-3">
              Generative AI can analyze, propose, and recommend. It <strong className="text-neon-red">CANNOT</strong> send
              commands directly to spacecraft actuators. All mission proposals must flow through:
            </p>
            <div className="flex flex-wrap items-center gap-2 text-[10px] font-mono">
              {['AI Proposal', 'Mission Planner', 'Digital Twin', 'Policy Engine', 'Authorization', 'Flight Ops', 'Uplink', 'Spacecraft'].map((step, i) => (
                <span key={step} className="flex items-center gap-2">
                  <span className={`px-2 py-1 rounded ${i === 0 ? 'bg-neon-purple/20 text-neon-purple' : i >= 4 ? 'bg-neon-green/20 text-neon-green' : 'bg-earth-700 text-earth-300'}`}>
                    {step}
                  </span>
                  {i < 7 && <ArrowRight size={10} className="text-earth-500" />}
                </span>
              ))}
            </div>
          </div>
        </div>
      </motion.div>

      {/* Ground vs Orbit */}
      <motion.div variants={item} className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-5">
          <div className="flex items-center gap-2 mb-3">
            <Satellite size={16} className="text-neon-orange" />
            <h4 className="text-sm font-semibold text-white">ORBIT (Edge)</h4>
          </div>
          <ul className="space-y-1.5">
            {['Sensor acquisition', 'Essential calibration', 'Compression', 'Small edge encoder', 'Anomaly detection', 'Quality estimation', 'Event generation', 'Priority queue', 'Communications'].map(item => (
              <li key={item} className="flex items-center gap-2 text-xs text-earth-400">
                <div className="w-1 h-1 rounded-full bg-neon-orange" />
                {item}
              </li>
            ))}
          </ul>
        </div>
        <div className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-5">
          <div className="flex items-center gap-2 mb-3">
            <Cpu size={16} className="text-neon-blue" />
            <h4 className="text-sm font-semibold text-white">GROUND (Cloud)</h4>
          </div>
          <ul className="space-y-1.5">
            {['Full foundation model', 'Planetary memory', 'Vector search', 'Earth Event Graph', 'World Model', 'Training', 'Generative AI', 'Global mission planning', 'Digital Twin', 'Model registry', 'Large storage'].map(item => (
              <li key={item} className="flex items-center gap-2 text-xs text-earth-400">
                <div className="w-1 h-1 rounded-full bg-neon-blue" />
                {item}
              </li>
            ))}
          </ul>
        </div>
      </motion.div>
    </motion.div>
  );
}

function StatusBadge({ label, status, color }: { label: string; status: string; color: string }) {
  const statusColors: Record<string, string> = {
    ready: 'bg-neon-green/10 text-neon-green border-neon-green/20',
    building: 'bg-neon-blue/10 text-neon-blue border-neon-blue/20',
    planned: 'bg-earth-700/50 text-earth-400 border-earth-600/50',
  };
  return (
    <span className={`px-2.5 py-1 text-[10px] font-mono rounded-full border ${statusColors[status] || statusColors.planned}`}>
      {label}: {status.toUpperCase()}
    </span>
  );
}

function MetricCard({ icon, label, value, color }: { icon: React.ReactNode; label: string; value: string; color: string }) {
  return (
    <div className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-4 flex items-center gap-4">
      <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ backgroundColor: `${color}15` }}>
        <span style={{ color }}>{icon}</span>
      </div>
      <div>
        <div className="text-2xl font-bold text-white">{value}</div>
        <div className="text-[10px] text-earth-400 uppercase tracking-wider">{label}</div>
      </div>
    </div>
  );
}
