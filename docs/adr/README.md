# Architecture Decision Records

## ADR-001: Modular Monorepo
**Status:** Accepted
**Context:** Multiple bounded contexts need to evolve independently while sharing contracts.
**Decision:** Modular monorepo with packages/, services/, apps/ structure.
**Consequences:** Single deployment initially, clear boundaries for future extraction.
**Alternatives:** Full microservices, pure monolith, multi-repo.

## ADR-002: PostgreSQL/PostGIS Geospatial Core
**Status:** Accepted
**Context:** Robust geospatial operations, spatial indexing, and vector embeddings needed.
**Decision:** PostgreSQL + PostGIS + pgvector. SRID 4326 for all geographic data.
**Consequences:** Mature engine, rich spatial indexing, co-located vector search.
**Alternatives:** MongoDB geospatial, dedicated spatial DB.

## ADR-003: S3 Storage + Immutable Raw Data
**Status:** Accepted
**Context:** Satellite observations are scientific evidence that must not be silently overwritten.
**Decision:** S3-compatible storage. Raw assets immutable. SHA-256 checksums. Provenance tracking.
**Consequences:** Data integrity guaranteed, content-addressable dedup possible.
**Alternatives:** Local filesystem, HDFS.

## ADR-004: Event-Driven Architecture
**Status:** Accepted
**Context:** Observation pipeline has multiple stages requiring loose coupling.
**Decision:** Kafka-compatible event bus (Redpanda). Versioned event schemas.
**Consequences:** Independent scaling, new consumers without producer changes.
**Alternatives:** Direct sync calls, database polling.

## ADR-005: Transactional Outbox
**Status:** Accepted
**Context:** Must atomically persist entity + publish event without distributed transactions.
**Decision:** Write events to outbox_events table in same transaction. Worker relays to bus.
**Consequences:** Guaranteed delivery, no 2PC needed, slight latency.
**Alternatives:** Two-phase commit, CDC (Debezium).

## ADR-006: pgvector Initial Vector Store
**Status:** Accepted
**Context:** Future embedding storage needed. Separate vector DB adds complexity early.
**Decision:** pgvector in same PostgreSQL. Enables hybrid spatial+vector queries.
**Consequences:** Simpler ops, may need migration at scale.
**Alternatives:** Dedicated vector DB, FAISS.

## ADR-007: STAC Interoperability
**Status:** Accepted
**Context:** EO data has standardized discovery patterns via STAC.
**Decision:** Map Observation → STAC Item. Internal model authoritative; STAC is projection.
**Consequences:** Ecosystem interoperability, mapping layer maintenance.
**Alternatives:** Custom format, ISO 19115.

## ADR-008: Generative AI Cannot Command Spacecraft
**Status:** Accepted
**Context:** AI hallucination or prompt injection must never reach spacecraft actuators.
**Decision:** Hard boundary. AI proposes → Mission Planner → Digital Twin → Policy → Human Auth → Flight Ops → Uplink.
**Consequences:** Safety guaranteed, added latency acceptable.
**Alternatives:** AI with guardrails but direct access, full autonomy.

## ADR-009: Scientific Knowledge States
**Status:** Accepted
**Context:** Must distinguish observations from inferences, forecasts, simulations.
**Decision:** Enum KnowledgeState: OBSERVED, INFERRED, FORECAST, SIMULATED. All entities tagged.
**Consequences:** Clear epistemic provenance, prevents silent confusion.
**Alternatives:** Confidence scores only, separate tables.

## ADR-010: Model Versioning and Provenance
**Status:** Accepted
**Context:** ML model outputs must be fully reproducible.
**Decision:** ModelVersion with git commit, checkpoint SHA-256, training data version, metrics, lifecycle.
**Consequences:** Full reproducibility, disciplined versioning required.
**Alternatives:** MLflow only, no provenance.

## ADR-011: Ground/Orbit Execution Boundary
**Status:** Accepted
**Context:** Future orbital edge computing needs clear separation from ground.
**Decision:** ORBIT: acquisition, calibration, compression, edge encoder, anomaly detection. GROUND: full models, memory, training, planning.
**Consequences:** Independent evolution, clear capability allocation.
**Alternatives:** Full ground only, full orbit, unclear boundary.

## ADR-012: API/Event Contract Versioning
**Status:** Accepted
**Context:** API and event consumers depend on stable contracts.
**Decision:** URL path versioning for API. schema_version in events. Never remove v1 fields.
**Consequences:** Consumer upgrade flexibility, explicit evolution.
**Alternatives:** Header versioning, no versioning.
