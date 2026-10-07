export interface ADR {
  id: string;
  title: string;
  status: 'accepted' | 'proposed' | 'deprecated';
  context: string;
  decision: string;
  consequences: string[];
  alternatives: string[];
}

export const adrs: ADR[] = [
  {
    id: 'ADR-001',
    title: 'Modular Monorepo Architecture',
    status: 'accepted',
    context: 'Earth Intelligence OS requires multiple bounded contexts that must evolve independently while sharing core contracts. A full microservices approach would create excessive operational complexity for Phase 0. A monolith would prevent future extraction.',
    decision: 'Adopt a modular monorepo with clear package boundaries (packages/, services/, apps/). Each module exposes typed interfaces and communicates via events. Services can be extracted to independent deployments when scaling demands it.',
    consequences: [
      'Single deployment unit in early phases reduces operational overhead',
      'Clear module boundaries allow future extraction without rewrites',
      'Shared contracts package prevents contract drift',
      'Single CI/CD pipeline for core platform',
      'Requires discipline to maintain boundaries'
    ],
    alternatives: ['Full microservices from day 1', 'Pure monolith', 'Multi-repo with shared libraries']
  },
  {
    id: 'ADR-002',
    title: 'PostgreSQL/PostGIS as Geospatial Core',
    status: 'accepted',
    context: 'The platform requires robust geospatial operations, spatial indexing, and integration with vector embeddings for future ML capabilities. The database must support complex spatial queries, reprojections, and serve as the system of record.',
    decision: 'Use PostgreSQL with PostGIS extension as the primary data store. Use pgvector for initial vector storage. SRID 4326 (WGS84) for all geographic data.',
    consequences: [
      'Mature, battle-tested geospatial engine',
      'Rich spatial indexing (GiST) for fast queries',
      'pgvector enables future embedding search without separate vector DB',
      'Well-understood operational characteristics',
      'Requires PostGIS expertise for advanced operations'
    ],
    alternatives: ['MongoDB with geospatial', 'Dedicated spatial DB (e.g., CrateDB)', 'Separate PostGIS + vector DB']
  },
  {
    id: 'ADR-003',
    title: 'S3-Compatible Object Storage with Immutable Raw Data',
    status: 'accepted',
    context: 'Satellite observations produce large binary assets that constitute scientific evidence. Raw data must never be silently overwritten. Processing pipelines produce derived assets that must be traceable to their inputs.',
    decision: 'Use S3-compatible object storage (MinIO locally, S3/GCS in production). Raw assets are immutable after creation. Each asset has SHA-256 checksums. Transformation lineage is recorded via provenance records.',
    consequences: [
      'Raw data integrity guaranteed by immutability policy',
      'SHA-256 enables content-addressable deduplication',
      'Provenance records create auditable transformation chains',
      'S3-compatible API enables cloud portability',
      'Storage costs grow linearly with observation volume'
    ],
    alternatives: ['Local filesystem', 'HDFS', 'Dedicated scientific archive']
  },
  {
    id: 'ADR-004',
    title: 'Event-Driven Architecture',
    status: 'accepted',
    context: 'The observation pipeline involves multiple stages (receive, validate, calibrate, georeference, coregister, quality-score). Each stage must be independently scalable, retryable, and observable. The system must support future consumers without modifying producers.',
    decision: 'Implement event-driven architecture using Kafka-compatible message bus (Redpanda locally). All domain events are versioned (schema_version field). Events flow through a transactional outbox to guarantee at-least-once delivery.',
    consequences: [
      'Loose coupling between pipeline stages',
      'New consumers can be added without modifying producers',
      'Event replay enables debugging and reprocessing',
      'Schema evolution requires explicit versioning',
      'Requires careful idempotency design in consumers'
    ],
    alternatives: ['Direct synchronous calls', 'Database polling', 'gRPC streaming']
  },
  {
    id: 'ADR-005',
    title: 'Transactional Outbox Pattern',
    status: 'accepted',
    context: 'When creating an Observation, we must both persist it to the database and publish an event. Without coordination, a crash between these operations leads to lost events or phantom observations.',
    decision: 'Use the Transactional Outbox pattern. Events are written to an outbox_events table in the same database transaction as the domain entity. A separate worker (outbox relay) polls for unprocessed outbox entries and publishes them to the message bus.',
    consequences: [
      'Atomic persistence of entity + event notification',
      'No distributed transaction coordination needed',
      'Worker handles retries, backoff, and ordering',
      'Outbox table grows until relayed (needs cleanup)',
      'Slight latency between entity creation and event availability'
    ],
    alternatives: ['Two-phase commit', 'Change Data Capture (Debezium)', 'Event sourcing']
  },
  {
    id: 'ADR-006',
    title: 'pgvector for Initial Vector Store',
    status: 'accepted',
    context: 'Future phases require embedding storage and similarity search for Planetary Memory. Starting with a separate vector database adds operational complexity before the need is proven.',
    decision: 'Use pgvector extension within the same PostgreSQL instance. This enables co-located spatial + vector queries and simplifies operations. Can be migrated to dedicated vector DB (Qdrant, Weaviate) if scale demands it.',
    consequences: [
      'Single database for spatial + vector operations',
      'Enables hybrid queries (spatial + semantic)',
      'Simpler operations in early phases',
      'pgvector performance may be insufficient at very large scale',
      'Migration path exists if needed'
    ],
    alternatives: ['Dedicated vector DB from day 1', 'FAISS on filesystem', 'Pinecone/Weaviate managed service']
  },
  {
    id: 'ADR-007',
    title: 'STAC (SpatioTemporal Asset Catalog) Compliance',
    status: 'accepted',
    context: 'Earth observation data has standardized discovery and access patterns. STAC is the emerging standard for describing geospatial assets with rich metadata, enabling interoperability with the broader EO ecosystem.',
    decision: 'Implement STAC Item mapping from internal Observation models. Expose STAC-compatible API endpoints. Internal models remain authoritative; STAC is a projection/view.',
    consequences: [
      'Interoperability with STAC ecosystem (stac-browser, planetary-computer, etc.)',
      'Standard metadata format reduces custom integration work',
      'Internal model can evolve independently of STAC spec changes',
      'Requires maintaining mapping layer',
      'STAC spec evolution may require mapping updates'
    ],
    alternatives: ['Custom metadata format only', 'ISO 19115', 'OGC API - Records']
  },
  {
    id: 'ADR-008',
    title: 'Generative AI Cannot Command Spacecraft Directly',
    status: 'accepted',
    context: 'As the platform incorporates generative AI capabilities, there is a critical safety boundary: AI models must never have direct access to spacecraft actuators or command uplink systems. The risk of hallucinated commands or adversarial prompt injection leading to unauthorized satellite maneuvers is unacceptable.',
    decision: 'Establish a hard architectural boundary: Generative AI can analyze, propose, and recommend. All mission proposals must flow through: AI Proposal → Mission Planner → Digital Twin Simulation → Policy Engine → Human Authorization → Flight Operations → Uplink. The AI layer has NO direct network path to command systems.',
    consequences: [
      'Critical safety boundary prevents AI-induced spacecraft damage',
      'All AI proposals are subject to simulation validation',
      'Human-in-the-loop for all commanding decisions',
      'Audit trail from proposal to execution',
      'Added latency in emergency response scenarios (acceptable tradeoff)',
      'Requires clear API contracts between AI and Mission Planner'
    ],
    alternatives: ['AI with guardrails but direct access', 'Full autonomous commanding', 'Manual-only planning']
  },
  {
    id: 'ADR-009',
    title: 'Knowledge State Classification',
    status: 'accepted',
    context: 'The platform produces different types of knowledge: direct observations, model inferences, forecasts, and simulations. Mixing these silently leads to scientific errors and loss of trust. Users must always know the epistemic status of information.',
    decision: 'Define an enum KnowledgeState with values: OBSERVED, INFERRED, FORECAST, SIMULATED. All domain entities that represent knowledge must carry this classification. UI must visually distinguish states. APIs must filter and label by state.',
    consequences: [
      'Clear epistemic provenance for all platform outputs',
      'Users can filter by confidence/knowledge type',
      'Prevents silent confusion between observation and prediction',
      'Supports future uncertainty quantification',
      'Requires discipline in tagging all outputs'
    ],
    alternatives: ['Confidence scores only', 'Provenance chain without explicit state', 'Separate tables per state']
  },
  {
    id: 'ADR-010',
    title: 'Model Versioning and Provenance',
    status: 'accepted',
    context: 'ML models used for inference must be fully traceable: which version produced which output, trained on which data, with which metrics. Reproducibility requires complete lineage.',
    decision: 'Implement ModelVersion entity with: semantic version, git commit, framework, checkpoint URI, SHA-256, training dataset version, metrics, status lifecycle. All inference outputs reference their model version. Provenance records link inputs to outputs.',
    consequences: [
      'Full reproducibility of any inference result',
      'Model lifecycle management (registered → validated → promoted → deployed → retired)',
      'Training data lineage enables data quality investigation',
      'Checkpoint integrity via SHA-256',
      'Requires disciplined versioning from ML team'
    ],
    alternatives: ['MLflow only', 'Custom registry without provenance', 'Git LFS for checkpoints']
  },
  {
    id: 'ADR-011',
    title: 'Ground vs Orbit Execution Boundary',
    status: 'accepted',
    context: 'Future phases will deploy edge computing capabilities on orbital platforms. The architecture must clearly separate what runs on the spacecraft (constrained, autonomous) from what runs on the ground (unlimited compute, full context).',
    decision: 'Define clear capability boundary. ORBIT: sensor acquisition, essential calibration, compression, small edge encoder, anomaly detection, quality estimation, event generation, priority queue, communications. GROUND: full foundation models, planetary memory, vector search, Earth Event Graph, World Model, training, generative AI, global mission planning, digital twin, model registry, large storage.',
    consequences: [
      'Clear separation enables independent evolution',
      'Orbit code must be ultra-efficient and fault-tolerant',
      'Ground can leverage full cloud infrastructure',
      'Sync protocol needed between orbit and ground',
      'Models must be designed for both contexts'
    ],
    alternatives: ['Full ground processing only', 'Full orbit processing', 'Hybrid without clear boundary']
  },
  {
    id: 'ADR-012',
    title: 'API and Event Versioning Strategy',
    status: 'accepted',
    context: 'Both the REST API and the event bus carry contracts that consumers depend on. Breaking changes must be managed explicitly to prevent silent failures across the distributed system.',
    decision: 'API: URL path versioning (/api/v1/, /api/v2/). Events: schema_version field in EventEnvelope. Never remove a field from v1; add new fields optionally. Major breaking changes require new version. Deprecation period of minimum 2 minor versions before removal.',
    consequences: [
      'Consumers can upgrade at their own pace',
      'Event schema evolution is explicit and tracked',
      'Multiple API versions may run simultaneously',
      'Requires discipline in contract management',
      'Documentation must reflect all active versions'
    ],
    alternatives: ['Header-based versioning', 'No versioning (breaking changes)', 'Content negotiation']
  }
];
