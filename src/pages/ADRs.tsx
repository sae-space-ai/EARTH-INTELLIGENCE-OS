import { motion } from 'framer-motion';
import { adrs } from '../data/adrs';
import { useState } from 'react';
import { BookOpen, CheckCircle2, Clock, XCircle } from 'lucide-react';

const container = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.05 } } };
const item = { hidden: { opacity: 0, y: 15 }, show: { opacity: 1, y: 0 } };

const statusIcons = {
  accepted: <CheckCircle2 size={12} className="text-neon-green" />,
  proposed: <Clock size={12} className="text-neon-yellow" />,
  deprecated: <XCircle size={12} className="text-neon-red" />,
};

const statusColors = {
  accepted: 'text-neon-green bg-neon-green/10 border-neon-green/20',
  proposed: 'text-neon-yellow bg-neon-yellow/10 border-neon-yellow/20',
  deprecated: 'text-neon-red bg-neon-red/10 border-neon-red/20',
};

export function ADRsPage() {
  const [selected, setSelected] = useState<string | null>(null);
  const active = adrs.find(a => a.id === selected);

  return (
    <motion.div variants={container} initial="hidden" animate="show" className="space-y-6">
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <div className="flex items-center gap-3 mb-4">
          <BookOpen size={20} className="text-neon-green" />
          <h3 className="text-lg font-semibold text-white">Architecture Decision Records</h3>
          <span className="px-2 py-0.5 text-[10px] font-mono rounded-full bg-neon-green/10 text-neon-green border border-neon-green/20">
            {adrs.length} ADRs
          </span>
        </div>
        <p className="text-xs text-earth-400">
          All significant architectural decisions are documented as ADRs following the
          Context → Decision → Consequences → Alternatives format.
        </p>
      </motion.div>

      {/* ADR List */}
      <motion.div variants={item} className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {adrs.map((adr) => (
          <motion.button
            key={adr.id}
            variants={item}
            whileHover={{ scale: 1.01 }}
            onClick={() => setSelected(selected === adr.id ? null : adr.id)}
            className={`text-left p-4 rounded-xl border transition-all duration-200 ${
              selected === adr.id
                ? 'border-neon-green/40 bg-neon-green/5'
                : 'border-earth-600/30 bg-earth-800/30 hover:bg-earth-700/30'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-[10px] font-mono text-earth-500">{adr.id}</span>
              <span className={`px-2 py-0.5 text-[9px] font-mono rounded-full border flex items-center gap-1 ${statusColors[adr.status]}`}>
                {statusIcons[adr.status]}
                {adr.status}
              </span>
            </div>
            <h4 className="text-sm font-semibold text-white mb-1">{adr.title}</h4>
            <p className="text-[11px] text-earth-400 line-clamp-2">{adr.context.slice(0, 150)}...</p>
          </motion.button>
        ))}
      </motion.div>

      {/* ADR Detail */}
      {active && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="rounded-xl border border-neon-green/30 bg-earth-800/50 p-6 space-y-6"
        >
          <div>
            <div className="flex items-center gap-3 mb-2">
              <span className="text-xs font-mono text-neon-green">{active.id}</span>
              <span className={`px-2 py-0.5 text-[9px] font-mono rounded-full border ${statusColors[active.status]}`}>
                {active.status}
              </span>
            </div>
            <h3 className="text-xl font-bold text-white">{active.title}</h3>
          </div>

          <div>
            <h4 className="text-xs font-semibold text-neon-blue uppercase tracking-wider mb-2">Context</h4>
            <p className="text-sm text-earth-300 leading-relaxed">{active.context}</p>
          </div>

          <div>
            <h4 className="text-xs font-semibold text-neon-green uppercase tracking-wider mb-2">Decision</h4>
            <p className="text-sm text-earth-300 leading-relaxed">{active.decision}</p>
          </div>

          <div>
            <h4 className="text-xs font-semibold text-neon-yellow uppercase tracking-wider mb-2">Consequences</h4>
            <ul className="space-y-1.5">
              {active.consequences.map((c, i) => (
                <li key={i} className="flex items-start gap-2 text-xs text-earth-300">
                  <span className="text-neon-yellow mt-0.5">•</span>
                  {c}
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="text-xs font-semibold text-neon-purple uppercase tracking-wider mb-2">Alternatives Considered</h4>
            <div className="flex flex-wrap gap-2">
              {active.alternatives.map(a => (
                <span key={a} className="px-2 py-1 text-[10px] font-mono rounded bg-earth-700/50 text-earth-300 border border-earth-600/30">
                  {a}
                </span>
              ))}
            </div>
          </div>
        </motion.div>
      )}
    </motion.div>
  );
}
