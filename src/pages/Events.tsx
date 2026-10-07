import { motion } from 'framer-motion';
import { eventTopics } from '../data/platform';
import { useState } from 'react';
import { Radio, Filter } from 'lucide-react';

const container = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.03 } } };
const item = { hidden: { opacity: 0, y: 10 }, show: { opacity: 1, y: 0 } };

const domainColors: Record<string, string> = {
  CONSTELLATION: '#00ff88',
  OBSERVATION: '#00d4ff',
  INTELLIGENCE: '#ffd700',
  EARTH_EVENTS: '#ff6b35',
  MISSION: '#ff3366',
  SECURITY: '#ef4444',
};

export function EventsPage() {
  const [filter, setFilter] = useState<string>('ALL');
  const domains = ['ALL', ...new Set(eventTopics.map(t => t.domain))];
  const filtered = filter === 'ALL' ? eventTopics : eventTopics.filter(t => t.domain === filter);

  return (
    <motion.div variants={container} initial="hidden" animate="show" className="space-y-6">
      {/* Header */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <div className="flex items-center gap-3 mb-4">
          <Radio size={20} className="text-neon-yellow" />
          <h3 className="text-lg font-semibold text-white">Event Catalog</h3>
          <span className="px-2 py-0.5 text-[10px] font-mono rounded-full bg-neon-yellow/10 text-neon-yellow border border-neon-yellow/20">
            {eventTopics.length} topics
          </span>
        </div>
        <p className="text-xs text-earth-400 mb-4">
          All domain events follow the EventEnvelope contract with versioned schemas. Events flow through
          the Transactional Outbox pattern to guarantee at-least-once delivery.
        </p>

        {/* EventEnvelope Schema */}
        <div className="p-4 rounded-lg bg-earth-900/50 border border-earth-600/30 font-mono text-[11px]">
          <div className="text-neon-green mb-2"># EventEnvelope Contract</div>
          <div className="space-y-0.5 text-earth-300">
            <div><span className="text-neon-blue">event_id</span>: UUID</div>
            <div><span className="text-neon-blue">event_type</span>: str  <span className="text-earth-500"># e.g., "observation.received"</span></div>
            <div><span className="text-neon-blue">schema_version</span>: str  <span className="text-earth-500"># e.g., "v1"</span></div>
            <div><span className="text-neon-blue">occurred_at</span>: datetime</div>
            <div><span className="text-neon-blue">produced_at</span>: datetime</div>
            <div><span className="text-neon-blue">producer</span>: str  <span className="text-earth-500"># service name</span></div>
            <div><span className="text-neon-blue">trace_id</span>: UUID</div>
            <div><span className="text-neon-blue">correlation_id</span>: UUID</div>
            <div><span className="text-neon-blue">payload</span>: dict  <span className="text-earth-500"># typed per event_type</span></div>
          </div>
        </div>
      </motion.div>

      {/* Filter */}
      <motion.div variants={item} className="flex items-center gap-2 flex-wrap">
        <Filter size={14} className="text-earth-400" />
        {domains.map(d => (
          <button
            key={d}
            onClick={() => setFilter(d)}
            className={`px-3 py-1.5 text-[10px] font-mono rounded-lg border transition-all ${
              filter === d
                ? 'bg-earth-600/50 text-white border-earth-500'
                : 'bg-earth-800/50 text-earth-400 border-earth-600/30 hover:text-white'
            }`}
          >
            {d}
          </button>
        ))}
      </motion.div>

      {/* Topics Grid */}
      <motion.div variants={item} className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {filtered.map(topic => (
          <motion.div
            key={topic.name}
            variants={item}
            className="p-4 rounded-lg border border-earth-600/30 bg-earth-800/30 hover:bg-earth-700/30 transition-colors"
          >
            <div className="flex items-center justify-between mb-2">
              <code className="text-xs font-bold text-white">{topic.name}.{topic.version}</code>
              <span
                className="px-2 py-0.5 text-[9px] font-mono rounded-full border"
                style={{
                  color: domainColors[topic.domain],
                  borderColor: `${domainColors[topic.domain]}40`,
                  backgroundColor: `${domainColors[topic.domain]}10`
                }}
              >
                {topic.domain}
              </span>
            </div>
            <p className="text-[11px] text-earth-400 mb-2">{topic.description}</p>
            <div className="flex flex-wrap gap-1">
              {Object.entries(topic.payload).map(([key, type]) => (
                <span key={key} className="px-1.5 py-0.5 text-[9px] font-mono rounded bg-earth-700/50 text-earth-300">
                  {key}: <span className="text-neon-blue">{type}</span>
                </span>
              ))}
            </div>
          </motion.div>
        ))}
      </motion.div>

      {/* Transactional Outbox */}
      <motion.div variants={item} className="rounded-xl border border-neon-green/20 bg-neon-green/5 p-6">
        <h3 className="text-sm font-semibold text-neon-green mb-3">Transactional Outbox Pattern (ADR-005)</h3>
        <div className="flex flex-wrap items-center gap-3 text-xs">
          <div className="px-3 py-2 rounded-lg bg-earth-800 border border-earth-600/50">
            <div className="text-[10px] text-earth-400 mb-1">1. API Request</div>
            <div className="text-white font-mono">POST /observations</div>
          </div>
          <span className="text-earth-500">→</span>
          <div className="px-3 py-2 rounded-lg bg-earth-800 border border-neon-blue/30">
            <div className="text-[10px] text-neon-blue mb-1">2. DB Transaction</div>
            <div className="text-white font-mono">INSERT observation</div>
            <div className="text-white font-mono">INSERT outbox_event</div>
          </div>
          <span className="text-earth-500">→</span>
          <div className="px-3 py-2 rounded-lg bg-earth-800 border border-neon-yellow/30">
            <div className="text-[10px] text-neon-yellow mb-1">3. Worker Polls</div>
            <div className="text-white font-mono">SELECT pending</div>
          </div>
          <span className="text-earth-500">→</span>
          <div className="px-3 py-2 rounded-lg bg-earth-800 border border-neon-green/30">
            <div className="text-[10px] text-neon-green mb-1">4. Publish</div>
            <div className="text-white font-mono">→ Redpanda</div>
          </div>
          <span className="text-earth-500">→</span>
          <div className="px-3 py-2 rounded-lg bg-earth-800 border border-neon-purple/30">
            <div className="text-[10px] text-neon-purple mb-1">5. Mark Sent</div>
            <div className="text-white font-mono">UPDATE status</div>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}
