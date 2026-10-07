import { motion } from 'framer-motion';
import { apiEndpoints } from '../data/platform';
import { Server, Lock, Unlock } from 'lucide-react';

const container = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.04 } } };
const item = { hidden: { opacity: 0, y: 15 }, show: { opacity: 1, y: 0 } };

const methodColors: Record<string, string> = {
  GET: '#00d4ff',
  POST: '#00ff88',
  PUT: '#ffd700',
  DELETE: '#ff3366',
};

export function APIPage() {
  return (
    <motion.div variants={container} initial="hidden" animate="show" className="space-y-6">
      {/* Header */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <div className="flex items-center gap-3 mb-4">
          <Server size={20} className="text-neon-blue" />
          <h3 className="text-lg font-semibold text-white">REST API — v1</h3>
        </div>
        <p className="text-xs text-earth-400 mb-4">
          FastAPI-based REST API with typed request/response models, structured error format,
          pagination support, and trace ID propagation.
        </p>

        {/* Error Format */}
        <div className="p-4 rounded-lg bg-earth-900/50 border border-earth-600/30 font-mono text-[11px]">
          <div className="text-neon-red mb-2"># Error Response Format</div>
          <div className="text-earth-300">
            <div>{'{'}</div>
            <div className="pl-4">"error": {'{'}</div>
            <div className="pl-8">"code": "<span className="text-neon-orange">OBSERVATION_NOT_FOUND</span>",</div>
            <div className="pl-8">"message": "<span className="text-earth-200">Observation with id ... not found</span>",</div>
            <div className="pl-8">"trace_id": "<span className="text-neon-blue">uuid</span>",</div>
            <div className="pl-8">"details": {'{}'}</div>
            <div className="pl-4">{'}'}</div>
            <div>{'}'}</div>
          </div>
        </div>
      </motion.div>

      {/* Endpoints */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">Endpoints</h3>
        <div className="space-y-2">
          {apiEndpoints.map((ep, i) => (
            <motion.div
              key={`${ep.method}-${ep.path}`}
              variants={item}
              className="flex items-center gap-4 p-3 rounded-lg bg-earth-700/20 border border-earth-600/20 hover:bg-earth-700/40 transition-colors"
            >
              <span
                className="px-2 py-1 text-[10px] font-bold font-mono rounded min-w-[50px] text-center"
                style={{ backgroundColor: `${methodColors[ep.method]}15`, color: methodColors[ep.method] }}
              >
                {ep.method}
              </span>
              <code className="text-xs text-white font-mono flex-1">{ep.path}</code>
              <span className="text-[11px] text-earth-400 hidden md:block">{ep.description}</span>
              {ep.auth ? (
                <Lock size={12} className="text-neon-orange" />
              ) : (
                <Unlock size={12} className="text-neon-green" />
              )}
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Tracing */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">Tracing & Correlation</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 rounded-lg bg-earth-700/20 border border-earth-600/30">
            <h4 className="text-xs font-semibold text-neon-blue mb-2">X-Trace-ID Header</h4>
            <ul className="space-y-1 text-[11px] text-earth-400">
              <li>• Accept valid UUID from client</li>
              <li>• Generate new UUID if missing</li>
              <li>• Return in response headers</li>
              <li>• Include in all structured logs</li>
              <li>• Propagate to event bus</li>
            </ul>
          </div>
          <div className="p-4 rounded-lg bg-earth-700/20 border border-earth-600/30">
            <h4 className="text-xs font-semibold text-neon-green mb-2">Structured Logging</h4>
            <ul className="space-y-1 text-[11px] text-earth-400">
              <li>• timestamp (ISO 8601)</li>
              <li>• level (DEBUG/INFO/WARNING/ERROR)</li>
              <li>• service name</li>
              <li>• environment</li>
              <li>• trace_id + correlation_id</li>
              <li>• message + context</li>
            </ul>
          </div>
        </div>
      </motion.div>

      {/* Pagination */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">Pagination</h3>
        <div className="p-4 rounded-lg bg-earth-900/50 border border-earth-600/30 font-mono text-[11px] text-earth-300">
          <div className="text-neon-green mb-2"># Query Parameters</div>
          <div>?page=1&per_page=20</div>
          <div className="mt-3 text-neon-green mb-2"># Response</div>
          <div>{'{'}</div>
          <div className="pl-4">"items": [...],</div>
          <div className="pl-4">"pagination": {'{'}</div>
          <div className="pl-8">"page": 1,</div>
          <div className="pl-8">"per_page": 20,</div>
          <div className="pl-8">"total": 150,</div>
          <div className="pl-8">"total_pages": 8</div>
          <div className="pl-4">{'}'}</div>
          <div>{'}'}</div>
        </div>
      </motion.div>

      {/* Service Architecture */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">Service Layer Separation</h3>
        <div className="flex flex-wrap items-center gap-3">
          <div className="px-4 py-3 rounded-lg bg-earth-700/30 border border-neon-blue/30 text-center">
            <div className="text-[10px] text-neon-blue mb-1">API Layer</div>
            <div className="text-xs text-white">FastAPI Routes</div>
            <div className="text-[9px] text-earth-400">Validation, serialization</div>
          </div>
          <span className="text-earth-500">→</span>
          <div className="px-4 py-3 rounded-lg bg-earth-700/30 border border-neon-green/30 text-center">
            <div className="text-[10px] text-neon-green mb-1">Service Layer</div>
            <div className="text-xs text-white">Business Logic</div>
            <div className="text-[9px] text-earth-400">Use cases, orchestration</div>
          </div>
          <span className="text-earth-500">→</span>
          <div className="px-4 py-3 rounded-lg bg-earth-700/30 border border-neon-purple/30 text-center">
            <div className="text-[10px] text-neon-purple mb-1">Repository Layer</div>
            <div className="text-xs text-white">Data Access</div>
            <div className="text-[9px] text-earth-400">SQLAlchemy, queries</div>
          </div>
          <span className="text-earth-500">→</span>
          <div className="px-4 py-3 rounded-lg bg-earth-700/30 border border-neon-yellow/30 text-center">
            <div className="text-[10px] text-neon-yellow mb-1">Infrastructure</div>
            <div className="text-xs text-white">PostgreSQL, S3, Kafka</div>
            <div className="text-[9px] text-earth-400">External systems</div>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}
