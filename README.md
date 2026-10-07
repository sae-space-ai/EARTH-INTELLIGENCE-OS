# Earth Intelligence OS

Planetary-scale intelligence platform for Earth observation, change detection, and autonomous mission planning.

## Current Status: Phase 0 — Foundation

Building the engineering foundation: modular monorepo, domain models, event-driven architecture, geospatial database, object storage, and API layer.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Control Room (React)                      │
├─────────────────────────────────────────────────────────────┤
│  FastAPI  │  Worker  │  Event Bus (Redpanda)  │  Storage   │
├─────────────────────────────────────────────────────────────┤
│  PostgreSQL + PostGIS + pgvector  │  MinIO (S3)             │
└─────────────────────────────────────────────────────────────┘
```

**Key Decisions:**
- Modular monorepo (Python backend + React frontend)
- Event-driven with transactional outbox
- PostgreSQL + PostGIS + pgvector for geospatial core
- S3-compatible object storage with immutable raw data
- Kafka-compatible event bus (Redpanda)
- Knowledge state classification: OBSERVED | INFERRED | FORECAST | SIMULATED
- Hard AI/command boundary (AI cannot directly command spacecraft)

## Repository Structure

```
earth-intelligence-os/
├── apps/
│   ├── api/              # FastAPI application
│   └── worker/           # Background worker (outbox relay)
├── packages/
│   ├── core/             # Config, logging, tracing
│   ├── contracts/        # Domain models, events, catalog
│   ├── geospatial/       # STAC mapping
│   ├── storage/          # S3 client
│   ├── events/           # Publisher, consumer, outbox
│   ├── ml/               # Model interfaces (future)
│   └── security/         # Audit logging
├── migrations/           # Alembic migrations
├── infrastructure/       # K8s, Postgres init
├── tests/                # Unit + integration tests
├── docs/                 # ADRs, security, roadmap
├── src/                  # Control Room frontend (React)
├── docker-compose.yml
├── pyproject.toml
└── Makefile
```

## Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Node.js 18+ (for Control Room frontend)

### Setup

```bash
# Install Python dependencies
make install

# Copy environment configuration
cp .env.example .env

# Start infrastructure
make compose-up

# Run migrations
make migrate

# Start API
make api

# In another terminal, start worker
make worker
```

### Frontend (Control Room)

```bash
npm install
npm run dev
```

Visit http://localhost:3000 for the Control Room dashboard.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Liveness check |
| GET | /ready | Readiness check |
| GET | /version | Version info |
| GET | /api/v1/satellites | List satellites |
| POST | /api/v1/satellites | Create satellite |
| GET | /api/v1/satellites/{id} | Get satellite |
| GET | /api/v1/sensors | List sensors |
| POST | /api/v1/sensors | Create sensor |
| GET | /api/v1/sensors/{id} | Get sensor |
| GET | /api/v1/observations | List observations |
| POST | /api/v1/observations | Create observation |
| GET | /api/v1/observations/{id} | Get observation |
| GET | /api/v1/events | List Earth Events |
| GET | /api/v1/events/{id} | Get Earth Event |
| POST | /api/v1/missions/requests | Create mission request |
| GET | /api/v1/missions/requests/{id} | Get mission request |

## Event Architecture

All domain events flow through a **transactional outbox** pattern:

1. API creates domain entity + outbox event in same transaction
2. Worker polls pending outbox events
3. Worker publishes to Redpanda/Kafka
4. Worker marks event as delivered

**Event Topics:** observation.received.v1, earth-event.created.v1, mission.requested.v1, etc.

See `packages/contracts/catalog.py` for full event catalog.

## Storage Policy

**RAW DATA IS EVIDENCE.**

- Raw assets are immutable after creation
- SHA-256 checksums mandatory
- No silent overwrites
- All transformations create new assets with provenance

**Processing Chain:** RAW → CALIBRATED → GEOREFERENCED → ALIGNED → DERIVED

## Security

See `docs/security/threat-model.md` for complete threat model.

**Critical Boundary:** Generative AI CANNOT directly command spacecraft. All mission proposals must flow through: AI → Mission Planner → Digital Twin → Policy Engine → Human Authorization → Flight Operations → Uplink → Spacecraft.

## Testing

```bash
# Run all tests
make test

# Run unit tests only
make test-unit

# Run integration tests
make test-integration

# Full validation
make check  # Runs: ruff check, ruff format --check, mypy, pytest
```

## Development

```bash
# Format code
make format

# Lint
make lint

# Type check
make typecheck

# Full validation
make check
```

## Roadmap

See `docs/phases/ROADMAP.md` for complete 14-phase roadmap.

**Next:** Phase 1 — Digital Twin Core (virtual satellites, orbital propagation, sensor footprints)

## License

Proprietary — All rights reserved.
