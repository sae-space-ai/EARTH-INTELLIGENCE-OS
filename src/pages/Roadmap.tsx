import { motion } from 'framer-motion';
import { roadmapPhases } from '../data/platform';
import { Map, CheckCircle2, ArrowRight, Clock, Circle } from 'lucide-react';

const container = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.06 } } };
const item = { hidden: { opacity: 0, y: 20 }, show: { opacity: 1, y: 0 } };

const statusConfig = {
  current: { color: '#00d4ff', icon: <CheckCircle2 size={14} />, label: 'IN PROGRESS' },
  next: { color: '#00ff88', icon: <ArrowRight size={14} />, label: 'NEXT' },
  planned: { color: '#ffd700', icon: <Clock size={14} />, label: 'PLANNED' },
  future: { color: '#6b7280', icon: <Circle size={14} />, label: 'FUTURE' },
};

export function RoadmapPage() {
  return (
    <motion.div variants={container} initial="hidden" animate="show" className="space-y-6">
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <div className="flex items-center gap-3 mb-4">
          <Map size={20} className="text-neon-purple" />
          <h3 className="text-lg font-semibold text-white">Platform Roadmap</h3>
          <span className="px-2 py-0.5 text-[10px] font-mono rounded-full bg-neon-purple/10 text-neon-purple border border-neon-purple/20">
            14 Phases
          </span>
        </div>
        <p className="text-xs text-earth-400">
          Progressive development from foundation to full planetary intelligence platform.
          Each phase builds on previous ones with clear inputs, outputs, and acceptance criteria.
        </p>
      </motion.div>

      {/* Timeline */}
      <div className="relative">
        {/* Timeline line */}
        <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gradient-to-b from-neon-blue via-neon-green via-neon-yellow to-earth-600" />

        <div className="space-y-4">
          {roadmapPhases.map((phase) => {
            const config = statusConfig[phase.status];
            return (
              <motion.div key={phase.id} variants={item} className="relative pl-14">
                {/* Timeline dot */}
                <div
                  className="absolute left-4 top-4 w-4 h-4 rounded-full border-2 flex items-center justify-center"
                  style={{ borderColor: config.color, backgroundColor: `${config.color}20` }}
                >
                  <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: config.color }} />
                </div>

                <div className={`rounded-xl border p-5 transition-all ${
                  phase.status === 'current'
                    ? 'border-neon-blue/40 bg-neon-blue/5'
                    : phase.status === 'next'
                    ? 'border-neon-green/30 bg-neon-green/5'
                    : 'border-earth-600/30 bg-earth-800/30'
                }`}>
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <span className="text-xs font-mono text-earth-500">Phase {phase.id}</span>
                      <h4 className="text-sm font-bold text-white">{phase.name}</h4>
                    </div>
                    <span
                      className="px-2 py-0.5 text-[9px] font-mono rounded-full border flex items-center gap-1"
                      style={{ color: config.color, borderColor: `${config.color}40`, backgroundColor: `${config.color}10` }}
                    >
                      {config.icon}
                      {config.label}
                    </span>
                  </div>

                  <p className="text-xs text-earth-300 mb-4">{phase.goal}</p>

                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
                    <div>
                      <h5 className="text-[10px] font-semibold text-neon-blue uppercase tracking-wider mb-1.5">Inputs</h5>
                      <ul className="space-y-0.5">
                        {phase.inputs.map(i => (
                          <li key={i} className="text-[10px] text-earth-400 flex items-center gap-1.5">
                            <span className="text-neon-blue">→</span> {i}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <h5 className="text-[10px] font-semibold text-neon-green uppercase tracking-wider mb-1.5">Outputs</h5>
                      <ul className="space-y-0.5">
                        {phase.outputs.map(o => (
                          <li key={o} className="text-[10px] text-earth-400 flex items-center gap-1.5">
                            <span className="text-neon-green">→</span> {o}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <h5 className="text-[10px] font-semibold text-neon-yellow uppercase tracking-wider mb-1.5">Dependencies</h5>
                      <ul className="space-y-0.5">
                        {phase.dependencies.map(d => (
                          <li key={d} className="text-[10px] text-earth-400 flex items-center gap-1.5">
                            <span className="text-neon-yellow">→</span> {d}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <h5 className="text-[10px] font-semibold text-neon-purple uppercase tracking-wider mb-1.5">Acceptance</h5>
                      <ul className="space-y-0.5">
                        {phase.acceptanceCriteria.map(a => (
                          <li key={a} className="text-[10px] text-earth-400 flex items-center gap-1.5">
                            <span className="text-neon-purple">✓</span> {a}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </motion.div>
  );
}
