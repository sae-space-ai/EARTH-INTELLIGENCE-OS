import { motion } from 'framer-motion';
import { GitBranch, ArrowRight, Database, Server, Radio, Shield, Cpu } from 'lucide-react';

const container = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.08 } } };
const item = { hidden: { opacity: 0, y: 20 }, show: { opacity: 1, y: 0 } };

const layers = [
  {
    name: 'Presentation Layer',
    color: '#00d4ff',
    components: ['Control Room UI', 'API Gateway', 'STAC Endpoints'],
    description: 'User interfaces and external API surface'
  },
  {
    name: 'Application Layer',
    color: '#00ff88',
    components: ['FastAPI App', 'Worker Service', 'Outbox Relay'],
    description: 'Application services, use cases, and background processing'
  },
  {
    name: 'Domain Layer',
    color: '#a855f7',
    components: ['Observation', 'Constellation', 'Planetary Memory', 'Earth Events', 'Intelligence', 'Mission', 'Provenance', 'Security'],
    description: 'Core business logic and bounded contexts'
  },
  {
    name: 'Infrastructure Layer',
    color: '#ffd700',
    components: ['PostgreSQL/PostGIS', 'pgvector', 'MinIO (S3)', 'Redpanda', 'OpenTelemetry'],
    description: 'External systems and infrastructure adapters'
  }
];

const packages = [
  { name: 'core', desc: 'Shared utilities, settings, logging, tracing', color: '#00d4ff' },
  { name: 'contracts', desc: 'Event schemas, domain contracts, versioning', color: '#00ff88' },
  { name: 'geospatial', desc: 'Geometry operations, projections, STAC', color: '#a855f7' },
  { name: 'storage', desc: 'S3 client, checksums, immutability', color: '#ffd700' },
  { name: 'events', desc: 'Publisher, consumer, outbox, topics', color: '#ff6b35' },
  { name: 'ml', desc: 'Model interfaces, registry, embeddings', color: '#ff3366' },
  { name: 'security', desc: 'Auth, policies, boundaries, audit', color: '#ef4444' },
];

export function ArchitecturePage() {
  return (
    <motion.div variants={container} initial="hidden" animate="show" className="space-y-8">
      {/* Architecture Principles */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">Architecture Principles</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {[
            { label: 'Modular Monorepo', desc: 'Clear boundaries, single deployment' },
            { label: 'Event-Driven', desc: 'Loose coupling, async processing' },
            { label: 'API-First', desc: 'Contracts before implementation' },
            { label: 'Cloud-Native', desc: 'Container-ready, observable' },
            { label: 'Geospatial-First', desc: 'PostGIS, STAC, SRID 4326' },
            { label: 'Secure by Design', desc: 'AI boundary, audit, encryption' },
            { label: 'Reproducible', desc: 'Provenance, versioning, checksums' },
            { label: 'Testable', desc: 'Unit, integration, contract tests' },
          ].map(p => (
            <div key={p.label} className="p-3 rounded-lg bg-earth-700/30 border border-earth-600/30">
              <div className="text-xs font-semibold text-white mb-1">{p.label}</div>
              <div className="text-[10px] text-earth-400">{p.desc}</div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Layered Architecture */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-6">Layered Architecture</h3>
        <div className="space-y-3">
          {layers.map((layer, i) => (
            <div key={layer.name} className="relative">
              <div className="flex items-stretch gap-4 p-4 rounded-lg border border-earth-600/30" style={{ borderColor: `${layer.color}30` }}>
                <div className="flex flex-col items-center justify-center w-8">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: layer.color }} />
                  {i < layers.length - 1 && <div className="w-0.5 flex-1 bg-earth-600/50 mt-1" />}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h4 className="text-sm font-semibold" style={{ color: layer.color }}>{layer.name}</h4>
                    <span className="text-[10px] text-earth-500 font-mono">{layer.description}</span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {layer.components.map(c => (
                      <span key={c} className="px-2 py-1 text-[10px] font-mono rounded bg-earth-700/50 text-earth-200 border border-earth-600/30">
                        {c}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Package Structure */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">Monorepo Package Structure</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {packages.map(pkg => (
            <div key={pkg.name} className="p-4 rounded-lg border border-earth-600/30 bg-earth-700/20 hover:bg-earth-700/40 transition-colors">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: pkg.color }} />
                <code className="text-xs font-bold text-white">packages/{pkg.name}</code>
              </div>
              <p className="text-[11px] text-earth-400">{pkg.desc}</p>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Directory Structure */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">Project Structure</h3>
        <div className="font-mono text-xs text-earth-300 leading-relaxed bg-earth-900/50 rounded-lg p-4 overflow-x-auto">
          <pre>{`earth-intelligence-os/
├── QWEN.md                    # Project memory & rules
├── README.md                  # Project documentation
├── pyproject.toml             # Python packaging
├── Makefile                   # Development commands
├── docker-compose.yml         # Local infrastructure
├── .env.example               # Configuration template
│
├── apps/
│   ├── api/                   # FastAPI application
│   ├── worker/                # Background worker
│   └── control-room/          # Web UI (this interface)
│
├── packages/
│   ├── core/                  # Settings, logging, tracing
│   ├── contracts/             # Event schemas, domain contracts
│   ├── geospatial/            # Geometry, STAC, projections
│   ├── storage/               # S3 client, checksums
│   ├── events/                # Publisher, consumer, outbox
│   ├── ml/                    # Model interfaces, registry
│   └── security/              # Auth, policies, audit
│
├── services/
│   ├── asset_registry/        # Asset lifecycle management
│   ├── science_ingest/        # Data ingestion pipeline
│   ├── orbit_state/           # Orbital mechanics (future)
│   └── provenance/            # Lineage tracking
│
├── infrastructure/
│   ├── kubernetes/            # K8s manifests + Kustomize
│   ├── postgres/              # DB init scripts
│   ├── redpanda/              # Event bus config
│   ├── minio/                 # Object storage config
│   └── observability/         # OTEL, Prometheus
│
├── migrations/                # Alembic migrations
├── schemas/                   # JSON schemas for events
├── config/                    # Environment configs
├── docs/                      # Architecture, ADRs, security
├── scripts/                   # Utility scripts
├── tests/                     # Unit, integration, contracts
└── .github/workflows/         # CI/CD pipelines`}</pre>
        </div>
      </motion.div>

      {/* Data Flow */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">Data Flow Architecture</h3>
        <div className="flex flex-wrap items-center justify-center gap-3 py-4">
          {[
            { label: 'Satellite', icon: '🛰️', color: '#ff6b35' },
            { label: 'Downlink', icon: '📡', color: '#ffd700' },
            { label: 'Ingest API', icon: '⬇️', color: '#00d4ff' },
            { label: 'Database', icon: '🗄️', color: '#a855f7' },
            { label: 'Outbox', icon: '📬', color: '#00ff88' },
            { label: 'Event Bus', icon: '📡', color: '#ffd700' },
            { label: 'Worker', icon: '⚙️', color: '#00d4ff' },
            { label: 'Processing', icon: '🔬', color: '#a855f7' },
            { label: 'Storage', icon: '💾', color: '#ff6b35' },
          ].map((node, i) => (
            <div key={node.label} className="flex items-center gap-2">
              <div className="flex flex-col items-center gap-1 px-3 py-2 rounded-lg border border-earth-600/30 bg-earth-700/30">
                <span className="text-lg">{node.icon}</span>
                <span className="text-[9px] font-mono" style={{ color: node.color }}>{node.label}</span>
              </div>
              {i < 8 && <ArrowRight size={14} className="text-earth-500" />}
            </div>
          ))}
        </div>
      </motion.div>

      {/* Tech Stack */}
      <motion.div variants={item} className="rounded-xl border border-earth-600/50 bg-earth-800/50 p-6">
        <h3 className="text-sm font-semibold text-earth-300 uppercase tracking-wider mb-4">Technology Stack</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[
            { category: 'Language & Framework', items: ['Python 3.11+', 'FastAPI', 'Pydantic v2', 'SQLAlchemy 2.x', 'Alembic'] },
            { category: 'Database', items: ['PostgreSQL 16', 'PostGIS 3.4', 'pgvector', 'SRID 4326'] },
            { category: 'Object Storage', items: ['S3-compatible API', 'MinIO (local)', 'SHA-256 checksums', 'Immutable raw data'] },
            { category: 'Event Bus', items: ['Kafka-compatible', 'Redpanda (local)', 'Transactional outbox', 'Versioned schemas'] },
            { category: 'Geospatial', items: ['GeoJSON', 'STAC', 'Shapely', 'pyproj'] },
            { category: 'Observability', items: ['Structured logging', 'OpenTelemetry', 'Prometheus', 'Trace IDs'] },
            { category: 'ML (Future)', items: ['PyTorch 2.x', 'torchvision', 'torch-geometric', 'CPU tests, CUDA optional'] },
            { category: 'Quality', items: ['pytest', 'Ruff', 'mypy', 'pre-commit'] },
            { category: 'Infrastructure', items: ['Docker', 'Docker Compose', 'Kubernetes', 'Kustomize'] },
          ].map(cat => (
            <div key={cat.category} className="p-4 rounded-lg border border-earth-600/30 bg-earth-700/20">
              <h5 className="text-xs font-semibold text-white mb-2">{cat.category}</h5>
              <ul className="space-y-1">
                {cat.items.map(i => (
                  <li key={i} className="text-[11px] text-earth-400 flex items-center gap-2">
                    <div className="w-1 h-1 rounded-full bg-neon-blue" />
                    {i}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </motion.div>
    </motion.div>
  );
}
