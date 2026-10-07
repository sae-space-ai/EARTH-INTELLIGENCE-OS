export interface Domain {
  id: string;
  name: string;
  icon: string;
  color: string;
  description: string;
  entities: string[];
  responsibilities: string[];
}

export const domains: Domain[] = [
  {
    id: 'OBSERVATION',
    name: 'Observation',
    icon: '🛰️',
    color: '#00d4ff',
    description: 'Manages sensor observations, assets, footprints, and metadata from satellite constellations.',
    entities: ['Satellite', 'Sensor', 'Observation', 'ObservationAsset', 'AreaOfInterest'],
    responsibilities: ['Ingest raw sensor data', 'Manage observation lifecycle', 'Track spatial footprints', 'Quality scoring', 'STAC compliance']
  },
  {
    id: 'CONSTELLATION',
    name: 'Constellation',
    icon: '🌐',
    color: '#00ff88',
    description: 'Satellite fleet management, orbital state, coverage planning, and constellation health.',
    entities: ['Satellite', 'OrbitalState', 'CoverageMap'],
    responsibilities: ['Track satellite health', 'Propagate orbital elements', 'Compute coverage', 'Plan observation windows', 'Manage constellation state']
  },
  {
    id: 'PLANETARY_MEMORY',
    name: 'Planetary Memory',
    icon: '🧠',
    color: '#a855f7',
    description: 'Historical embedding store, Earth State representation, and temporal knowledge base.',
    entities: ['EarthState', 'Embedding', 'TemporalIndex'],
    responsibilities: ['Store historical embeddings', 'Maintain Earth State vector', 'Enable temporal queries', 'Support similarity search', 'Foundation for World Model']
  },
  {
    id: 'EARTH_EVENTS',
    name: 'Earth Events',
    icon: '🌍',
    color: '#ff6b35',
    description: 'Detection, tracking, and classification of planetary changes and anomalies.',
    entities: ['EarthEvent', 'ChangeEvent', 'AnomalyEvent', 'Evidence'],
    responsibilities: ['Detect changes', 'Classify anomalies', 'Track event evolution', 'Build evidence chains', 'Prioritize events']
  },
  {
    id: 'INTELLIGENCE',
    name: 'Intelligence',
    icon: '⚡',
    color: '#ffd700',
    description: 'ML models, inference pipelines, confidence estimation, and forecasting.',
    entities: ['ModelVersion', 'InferenceResult', 'Forecast', 'ConfidenceScore'],
    responsibilities: ['Run inference pipelines', 'Estimate uncertainty', 'Generate forecasts', 'Manage model lifecycle', 'Benchmark performance']
  },
  {
    id: 'MISSION',
    name: 'Mission',
    icon: '🎯',
    color: '#ff3366',
    description: 'Mission requests, planning, digital twin simulation, validation, and authorization.',
    entities: ['MissionRequest', 'MissionPlan', 'SimulationResult', 'Authorization'],
    responsibilities: ['Receive mission requests', 'Generate plans', 'Simulate via Digital Twin', 'Policy validation', 'Authorization workflow']
  },
  {
    id: 'PROVENANCE',
    name: 'Provenance',
    icon: '🔗',
    color: '#06b6d4',
    description: 'Complete lineage tracking for all data transformations, model versions, and audit records.',
    entities: ['ProvenanceRecord', 'AuditRecord', 'DatasetVersion', 'LineageGraph'],
    responsibilities: ['Track data lineage', 'Record transformations', 'Version datasets', 'Audit trail', 'Reproducibility support']
  },
  {
    id: 'SECURITY',
    name: 'Security',
    icon: '🛡️',
    color: '#ef4444',
    description: 'Identity, permissions, policies, secrets management, and the AI/command boundary.',
    entities: ['Identity', 'Permission', 'Policy', 'Secret', 'CommandBoundary'],
    responsibilities: ['Authentication/Authorization', 'Policy enforcement', 'Secret management', 'AI boundary enforcement', 'Audit logging']
  }
];

export interface EventTopic {
  name: string;
  version: string;
  domain: string;
  description: string;
  payload: Record<string, string>;
}

export const eventTopics: EventTopic[] = [
  { name: 'satellite.telemetry.received', version: 'v1', domain: 'CONSTELLATION', description: 'Raw telemetry packet received from satellite', payload: { satellite_id: 'uuid', timestamp: 'ISO8601', packet_type: 'string' } },
  { name: 'satellite.state.updated', version: 'v1', domain: 'CONSTELLATION', description: 'Satellite state transition detected', payload: { satellite_id: 'uuid', previous_state: 'enum', new_state: 'enum' } },
  { name: 'observation.received', version: 'v1', domain: 'OBSERVATION', description: 'New observation ingested into the system', payload: { observation_id: 'uuid', satellite_id: 'uuid', sensor_id: 'uuid' } },
  { name: 'observation.validated', version: 'v1', domain: 'OBSERVATION', description: 'Observation passed validation checks', payload: { observation_id: 'uuid', validation_result: 'object' } },
  { name: 'observation.calibrated', version: 'v1', domain: 'OBSERVATION', description: 'Radiometric calibration applied', payload: { observation_id: 'uuid', calibration_version: 'string' } },
  { name: 'observation.georeferenced', version: 'v1', domain: 'OBSERVATION', description: 'Geographic coordinates assigned', payload: { observation_id: 'uuid', srid: 'int', geometry: 'GeoJSON' } },
  { name: 'observation.coregistered', version: 'v1', domain: 'OBSERVATION', description: 'Aligned with reference grid', payload: { observation_id: 'uuid', reference_id: 'uuid' } },
  { name: 'observation.quality-scored', version: 'v1', domain: 'OBSERVATION', description: 'Quality assessment completed', payload: { observation_id: 'uuid', quality_score: 'float', flags: 'string[]' } },
  { name: 'embedding.created', version: 'v1', domain: 'INTELLIGENCE', description: 'New embedding generated from observation', payload: { observation_id: 'uuid', model_version_id: 'uuid', dimensions: 'int' } },
  { name: 'change.detected', version: 'v1', domain: 'EARTH_EVENTS', description: 'Temporal change detected between observations', payload: { location: 'GeoJSON', magnitude: 'float', evidence_ids: 'uuid[]' } },
  { name: 'anomaly.detected', version: 'v1', domain: 'EARTH_EVENTS', description: 'Anomalous pattern detected', payload: { location: 'GeoJSON', anomaly_type: 'string', confidence: 'float' } },
  { name: 'earth-event.created', version: 'v1', domain: 'EARTH_EVENTS', description: 'New Earth Event registered', payload: { event_id: 'uuid', event_type: 'string', geometry: 'GeoJSON' } },
  { name: 'earth-event.updated', version: 'v1', domain: 'EARTH_EVENTS', description: 'Earth Event updated with new evidence', payload: { event_id: 'uuid', new_evidence_count: 'int' } },
  { name: 'earth-event.confirmed', version: 'v1', domain: 'EARTH_EVENTS', description: 'Earth Event confirmed by analysis', payload: { event_id: 'uuid', confidence: 'float' } },
  { name: 'prediction.created', version: 'v1', domain: 'INTELLIGENCE', description: 'New forecast/prediction generated', payload: { prediction_id: 'uuid', model_version_id: 'uuid', horizon: 'string' } },
  { name: 'mission.requested', version: 'v1', domain: 'MISSION', description: 'New observation mission requested', payload: { mission_id: 'uuid', aoi: 'GeoJSON', priority: 'int' } },
  { name: 'mission.plan-created', version: 'v1', domain: 'MISSION', description: 'Mission plan generated', payload: { mission_id: 'uuid', plan_id: 'uuid', satellites: 'uuid[]' } },
  { name: 'mission.simulation-passed', version: 'v1', domain: 'MISSION', description: 'Digital Twin simulation validated plan', payload: { mission_id: 'uuid', simulation_id: 'uuid' } },
  { name: 'mission.simulation-failed', version: 'v1', domain: 'MISSION', description: 'Digital Twin simulation rejected plan', payload: { mission_id: 'uuid', failure_reason: 'string' } },
  { name: 'mission.authorization-required', version: 'v1', domain: 'MISSION', description: 'Mission requires human authorization', payload: { mission_id: 'uuid', authorization_level: 'string' } },
  { name: 'mission.approved', version: 'v1', domain: 'MISSION', description: 'Mission approved for execution', payload: { mission_id: 'uuid', approved_by: 'string' } },
  { name: 'mission.rejected', version: 'v1', domain: 'MISSION', description: 'Mission rejected', payload: { mission_id: 'uuid', rejection_reason: 'string' } },
  { name: 'model.registered', version: 'v1', domain: 'INTELLIGENCE', description: 'New model version registered', payload: { model_version_id: 'uuid', model_name: 'string', version: 'string' } },
  { name: 'model.validation-passed', version: 'v1', domain: 'INTELLIGENCE', description: 'Model passed validation suite', payload: { model_version_id: 'uuid', metrics: 'object' } },
  { name: 'model.promoted', version: 'v1', domain: 'INTELLIGENCE', description: 'Model promoted to production', payload: { model_version_id: 'uuid', environment: 'string' } },
  { name: 'audit.recorded', version: 'v1', domain: 'SECURITY', description: 'Security audit event recorded', payload: { actor_id: 'string', action: 'string', resource_id: 'uuid' } },
];

export interface PipelineStage {
  name: string;
  event: string;
  status: 'active' | 'planned' | 'future';
  description: string;
}

export const observationPipeline: PipelineStage[] = [
  { name: 'Receive', event: 'observation.received.v1', status: 'active', description: 'Raw data ingested from satellite downlink' },
  { name: 'Validate', event: 'observation.validated.v1', status: 'active', description: 'Format, integrity, and completeness checks' },
  { name: 'Calibrate', event: 'observation.calibrated.v1', status: 'planned', description: 'Radiometric and geometric calibration' },
  { name: 'Georeference', event: 'observation.georeferenced.v1', status: 'planned', description: 'Assign precise geographic coordinates' },
  { name: 'Coregister', event: 'observation.coregistered.v1', status: 'planned', description: 'Align to reference grid/system' },
  { name: 'Quality Score', event: 'observation.quality-scored.v1', status: 'planned', description: 'Automated quality assessment' },
  { name: 'Embed', event: 'embedding.created.v1', status: 'future', description: 'Generate foundation model embeddings' },
  { name: 'Detect Change', event: 'change.detected.v1', status: 'future', description: 'Compare with historical observations' },
];

export interface RoadmapPhase {
  id: number;
  name: string;
  goal: string;
  inputs: string[];
  outputs: string[];
  dependencies: string[];
  acceptanceCriteria: string[];
  status: 'current' | 'next' | 'planned' | 'future';
}

export const roadmapPhases: RoadmapPhase[] = [
  { id: 0, name: 'Foundation', goal: 'Build the correct foundations: architecture, infrastructure, domain models, events, storage, and observability.', inputs: ['Requirements', 'Architecture decisions'], outputs: ['Monorepo', 'Docker Compose', 'API', 'Worker', 'Database', 'Event bus', 'Tests'], dependencies: [], acceptanceCriteria: ['All Phase 0 criteria pass', 'Tests green', 'Infrastructure runs'], status: 'current' },
  { id: 1, name: 'Digital Twin Core', goal: 'Virtual satellites, orbital state, synthetic passes, sensor footprints, AOI intersection, simulation clock.', inputs: ['Phase 0 foundation', 'Orbital mechanics models'], outputs: ['Virtual satellite fleet', 'Orbital propagator', 'Footprint calculator', 'Simulation clock'], dependencies: ['Phase 0'], acceptanceCriteria: ['Virtual satellites in orbit', 'Footprints computed', 'AOI intersections work'], status: 'next' },
  { id: 2, name: 'Planetary Data Platform', goal: 'Multi-source data ingestion, harmonization, and access layer.', inputs: ['Phase 1', 'Data format specs'], outputs: ['Ingestion pipelines', 'Harmonized data layer', 'Query API'], dependencies: ['Phase 0', 'Phase 1'], acceptanceCriteria: ['Multiple data sources ingestible', 'Unified query interface'], status: 'planned' },
  { id: 3, name: 'Multimodal Foundation Model', goal: 'Train/finetune foundation model for multi-sensor Earth observation.', inputs: ['Phase 2 data', 'GPU infrastructure', 'Training datasets'], outputs: ['Foundation model', 'Encoder interfaces', 'Benchmark suite'], dependencies: ['Phase 2'], acceptanceCriteria: ['Model trained', 'Multi-modal encoding works', 'Benchmarks established'], status: 'planned' },
  { id: 4, name: 'Planetary Memory', goal: 'Build temporal embedding store and Earth State representation.', inputs: ['Phase 3 embeddings', 'Historical data'], outputs: ['Planetary Memory store', 'Earth State vector', 'Temporal search'], dependencies: ['Phase 3'], acceptanceCriteria: ['Embeddings stored', 'Temporal queries work', 'Earth State maintained'], status: 'future' },
  { id: 5, name: 'Earth Events & Change Intelligence', goal: 'Detect, track, and classify planetary changes and anomalies.', inputs: ['Phase 4 memory', 'Change detection algorithms'], outputs: ['Event detection', 'Event tracking', 'Anomaly classification'], dependencies: ['Phase 4'], acceptanceCriteria: ['Changes detected', 'Events tracked', 'Anomalies classified'], status: 'future' },
  { id: 6, name: 'World Model', goal: 'Build internal world model for simulation and prediction.', inputs: ['Phase 5 events', 'Physics models'], outputs: ['World Model', 'Simulation engine', 'Prediction capabilities'], dependencies: ['Phase 5'], acceptanceCriteria: ['World model runs', 'Predictions generated', 'Simulations validated'], status: 'future' },
  { id: 7, name: 'Active Earth Intelligence', goal: 'Closed-loop observe→understand→act cycle with information gap identification.', inputs: ['Phase 6', 'Planning algorithms'], outputs: ['Information gap detector', 'Observation planner', 'Active learning loop'], dependencies: ['Phase 6'], acceptanceCriteria: ['Gaps identified', 'Observations planned', 'Loop closes'], status: 'future' },
  { id: 8, name: 'Constellation Intelligence', goal: 'Optimize constellation operations and coordination.', inputs: ['Phase 7', 'Constellation models'], outputs: ['Fleet optimizer', 'Coordination protocols', 'Resource allocator'], dependencies: ['Phase 7'], acceptanceCriteria: ['Fleet optimized', 'Coordination works', 'Resources allocated'], status: 'future' },
  { id: 9, name: 'Ask Earth / Generative Orchestrator', goal: 'Natural language interface to planetary intelligence with tool use.', inputs: ['Phase 8', 'LLM integration'], outputs: ['NL interface', 'Tool orchestration', 'Verified responses'], dependencies: ['Phase 8'], acceptanceCriteria: ['NL queries work', 'Tools invoked correctly', 'Responses verified'], status: 'future' },
  { id: 10, name: 'Earth Intelligence Control Room', goal: 'Full 3D operational control room for planetary monitoring.', inputs: ['Phase 9', 'Visualization framework'], outputs: ['3D Control Room', 'Real-time dashboard', 'Mission control interface'], dependencies: ['Phase 9'], acceptanceCriteria: ['3D visualization works', 'Real-time data', 'Mission control functional'], status: 'future' },
  { id: 11, name: 'Security & Mission Authority', goal: 'Full security stack, IAM, policy engine, and mission authorization.', inputs: ['Phase 10', 'Security requirements'], outputs: ['IAM system', 'Policy engine', 'Authorization workflow'], dependencies: ['Phase 10'], acceptanceCriteria: ['IAM operational', 'Policies enforced', 'Authorization works'], status: 'future' },
  { id: 12, name: 'Production Platform', goal: 'Harden for production: scaling, reliability, monitoring, disaster recovery.', inputs: ['Phase 11', 'Production requirements'], outputs: ['Production deployment', 'DR plan', 'Scaling automation'], dependencies: ['Phase 11'], acceptanceCriteria: ['Production-ready', 'DR tested', 'Auto-scaling works'], status: 'future' },
  { id: 13, name: 'End-to-End Mission Demonstrator', goal: 'Complete demonstration: detect event → plan observation → simulate → authorize → observe → learn.', inputs: ['Phase 12', 'Mission scenario'], outputs: ['Full mission cycle', 'Demonstration report', 'Validation results'], dependencies: ['Phase 12'], acceptanceCriteria: ['Full cycle demonstrated', 'All phases connected', 'Results validated'], status: 'future' },
];

export const knowledgeStates = [
  { state: 'OBSERVED', color: '#00d4ff', description: 'Direct sensor measurement. Highest epistemic certainty.', icon: '📡' },
  { state: 'INFERRED', color: '#a855f7', description: 'Derived from model analysis of observations. Includes confidence.', icon: '🔬' },
  { state: 'FORECAST', color: '#ffd700', description: 'Predicted future state based on models and trends.', icon: '🔮' },
  { state: 'SIMULATED', color: '#ff6b35', description: 'Generated by Digital Twin or World Model simulation.', icon: '🎮' },
];

export const apiEndpoints = [
  { method: 'GET', path: '/health', description: 'Service health check', auth: false },
  { method: 'GET', path: '/ready', description: 'Readiness check (dependencies available)', auth: false },
  { method: 'GET', path: '/version', description: 'Service version information', auth: false },
  { method: 'GET', path: '/api/v1/satellites', description: 'List satellites (paginated)', auth: true },
  { method: 'POST', path: '/api/v1/satellites', description: 'Register new satellite', auth: true },
  { method: 'GET', path: '/api/v1/satellites/{id}', description: 'Get satellite by ID', auth: true },
  { method: 'GET', path: '/api/v1/sensors', description: 'List sensors (paginated)', auth: true },
  { method: 'POST', path: '/api/v1/sensors', description: 'Register new sensor', auth: true },
  { method: 'GET', path: '/api/v1/observations', description: 'List observations (paginated, filterable)', auth: true },
  { method: 'POST', path: '/api/v1/observations', description: 'Create observation (triggers outbox)', auth: true },
  { method: 'GET', path: '/api/v1/observations/{id}', description: 'Get observation by ID', auth: true },
  { method: 'GET', path: '/api/v1/events', description: 'List Earth Events (paginated)', auth: true },
  { method: 'GET', path: '/api/v1/events/{id}', description: 'Get Earth Event by ID', auth: true },
  { method: 'POST', path: '/api/v1/missions/requests', description: 'Submit mission request', auth: true },
  { method: 'GET', path: '/api/v1/missions/requests/{id}', description: 'Get mission request status', auth: true },
];

export const threatModelItems = [
  { threat: 'API Compromise', risk: 'high', control: 'Rate limiting, WAF, input validation, auth tokens', status: 'planned' },
  { threat: 'Credential Theft', risk: 'high', control: 'Secret rotation, vault integration, no hardcoded secrets', status: 'planned' },
  { threat: 'Malicious Ingest', risk: 'high', control: 'Schema validation, checksum verification, quarantine', status: 'planned' },
  { threat: 'Data Poisoning', risk: 'critical', control: 'Provenance tracking, anomaly detection, data validation', status: 'future' },
  { threat: 'Model Poisoning', risk: 'critical', control: 'Checkpoint SHA-256, training data validation, model validation suite', status: 'future' },
  { threat: 'Event Bus Tampering', risk: 'high', control: 'TLS encryption, authentication, schema validation', status: 'planned' },
  { threat: 'Object Store Modification', risk: 'critical', control: 'Immutable raw data, SHA-256 verification, access control', status: 'active' },
  { threat: 'Database Compromise', risk: 'critical', control: 'Encryption at rest, access control, audit logging', status: 'planned' },
  { threat: 'Prompt Injection (future)', risk: 'high', control: 'AI boundary enforcement, no direct actuator access', status: 'designed' },
  { threat: 'Tool Misuse', risk: 'high', control: 'Tool sandboxing, output validation, human authorization', status: 'future' },
  { threat: 'Unauthorized Mission Proposal', risk: 'critical', control: 'Policy engine, simulation validation, human approval', status: 'designed' },
  { threat: 'Unauthorized Command Path', risk: 'critical', control: 'Hard AI/command boundary, no direct network path', status: 'designed' },
  { threat: 'Supply Chain Attack', risk: 'high', control: 'Dependency pinning, SBOM, vulnerability scanning', status: 'planned' },
  { threat: 'Secrets Exposure', risk: 'critical', control: 'Vault, no env vars in code, pre-commit secret detection', status: 'active' },
  { threat: 'Checkpoint Tampering', risk: 'critical', control: 'SHA-256 verification, signed checkpoints, integrity checks', status: 'future' },
];
