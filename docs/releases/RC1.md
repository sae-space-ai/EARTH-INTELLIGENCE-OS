# Earth Intelligence OS RC1 — Release Candidate 1

**Version:** 0.1.0-rc1  
**Release Date:** 2026  
**Status:** Ready for Human Testing

---

## Overview

Earth Intelligence OS RC1 is the first human-testable release of the planetary intelligence platform. This release delivers a functional Control Room with live data integration, real satellite tracking, and comprehensive entity management.

---

## Key Features

### 3D Control Room
- **CesiumJS-powered globe** with terrain and imagery
- **Real-time entity visualization** for aircraft, vessels, satellites, earthquakes, and fires
- **Interactive selection and tracking** with trail visualization
- **Context-aware layer management** (Live Contacts, Space Missions, Environmental, European Space)
- **Source and freshness indicators** for all data layers

### Live Data Integration
- **Aircraft tracking** via OpenSky Network and adsb.lol
- **Military ADS-B** visualization (public data only)
- **Vessel tracking** via AISStream (requires API key)
- **Satellite tracking** with real SGP4 orbital propagation
- **Earthquake monitoring** via USGS
- **Active fire detection** via NASA FIRMS (requires API key)

### European Space Federation
- **Copernicus CDSE** integration for Sentinel data
- **ESA Earth Observation** mission registry
- **EUMETSAT** meteorological data
- **Destination Earth** digital twin
- **Galileo/EGNOS** navigation services
- **ESA Space Weather** monitoring
- **EU SST** space situational awareness

### Advanced Capabilities
- **Real SGP4 propagation** using the sgp4 library
- **Satellite pass prediction** with topocentric visibility calculations
- **Orbit visualization** with ground tracks
- **European satellite linkage** connecting spacecraft to missions and instruments
- **Entity tracking** with bounded trails
- **Cockpit mode** for aircraft tracking
- **Demo mode** with deterministic fixtures for testing

### Infrastructure
- **FastAPI backend** with comprehensive REST API
- **PostgreSQL + PostGIS + pgvector** for geospatial data
- **MinIO** for object storage
- **Redpanda** for event streaming
- **Transactional outbox** for reliable event delivery
- **Docker Compose** for one-command deployment

---

## Installation

### Prerequisites
- Docker Desktop (or Docker Engine + Docker Compose)
- 8GB RAM minimum
- 10GB disk space

### Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd earth-intelligence-os

# Copy environment configuration
cp .env.example .env

# Optional: Add provider API keys to .env
# OPENSKY_USERNAME=your_username
# OPENSKY_PASSWORD=your_password
# AISSTREAM_API_KEY=your_key
# FIRMS_MAP_KEY=your_key

# Start all services
docker compose up --build

# Access the Control Room
open http://localhost:3000
```

### Demo Mode

If you don't have provider API keys, enable demo mode:

```bash
# Via API
curl -X POST http://localhost:8000/api/v1/live/demo/enable

# Or via UI
# Click "Enable Demo Mode" in the Control Room
```

Demo mode provides deterministic fixtures for:
- 3 aircraft
- 1 military aircraft
- 2 vessels
- 4 satellites (including ISS with real TLE)
- 3 earthquakes
- 5 fire detections

---

## API Endpoints

### Live Data
- `GET /api/v1/live/aircraft` — Live aircraft positions
- `GET /api/v1/live/military-aircraft` — Military ADS-B data
- `GET /api/v1/live/vessels` — Vessel positions
- `GET /api/v1/live/satellites` — Satellite positions (SGP4 propagated)
- `GET /api/v1/live/earthquakes` — Recent earthquakes
- `GET /api/v1/live/fires` — Active fire detections
- `GET /api/v1/live/provider-health` — Provider status

### Satellite Operations
- `POST /api/v1/live/satellites/pass` — Predict satellite pass over location

### Entity Management
- `POST /api/v1/live/track/{entity_id}` — Track entity
- `DELETE /api/v1/live/track/{entity_id}` — Untrack entity
- `POST /api/v1/live/select/{entity_id}` — Select entity
- `GET /api/v1/live/trail/{entity_id}` — Get entity trail

### Demo Mode
- `POST /api/v1/live/demo/enable` — Enable demo mode
- `POST /api/v1/live/demo/disable` — Disable demo mode
- `GET /api/v1/live/demo/status` — Check demo mode status

### European Space Federation
- `GET /api/v1/space/providers` — List providers
- `GET /api/v1/space/missions` — List missions
- `GET /api/v1/space/collections` — List data collections
- `POST /api/v1/space/search` — Search for data
- `POST /api/v1/space/catalog-sync/{provider_code}` — Sync catalog

### Health & Status
- `GET /health` — Service health
- `GET /ready` — Readiness check
- `GET /version` — Version information

---

## Testing

### Manual Testing Checklist

1. **Start the application**
   ```bash
   docker compose up --build
   ```

2. **Open Control Room**
   - Navigate to http://localhost:3000
   - Verify 3D globe loads

3. **Enable demo mode** (if no API keys)
   ```bash
   curl -X POST http://localhost:8000/api/v1/live/demo/enable
   ```

4. **Test live data layers**
   - Enable "Live Aircraft" layer
   - Verify aircraft appear on globe
   - Click aircraft to see details
   - Track aircraft to see trail

5. **Test satellite tracking**
   - Enable "Satellites" layer
   - Verify satellites appear with propagated positions
   - Click satellite to see orbital elements
   - Test pass prediction for ISS (NORAD 25544)

6. **Test European Space Federation**
   - Navigate to European Space context
   - Search for Sentinel-2 collections
   - Verify provider status

7. **Test entity selection**
   - Select different entity types
   - Verify details panel shows correct information
   - Test tracking/untracking

8. **Test demo/live mode switching**
   - Switch between demo and live modes
   - Verify data source changes

### Automated Tests

```bash
# Run all tests
make test

# Run specific test suites
make test-unit
make test-integration

# Run linting
make lint

# Run type checking
make typecheck
```

---

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Core infrastructure
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/earth_intelligence
OBJECT_STORAGE_ENDPOINT=http://minio:9000
OBJECT_STORAGE_ACCESS_KEY=minioadmin
OBJECT_STORAGE_SECRET_KEY=minioadmin
EVENT_BUS_BROKERS=redpanda:9092

# Optional provider credentials
OPENSKY_USERNAME=
OPENSKY_PASSWORD=
AISSTREAM_API_KEY=
FIRMS_MAP_KEY=
CDSE_CLIENT_ID=
CDSE_CLIENT_SECRET=

# LLM provider (optional)
OPENAI_API_KEY=
```

### Provider Status

| Provider | Status | Credentials Required | Live Tested |
|----------|--------|---------------------|-------------|
| OpenSky Network | ✅ Implemented | Optional (anonymous available) | ⚠️ Not tested |
| adsb.lol | ✅ Implemented | No | ⚠️ Not tested |
| AISStream | ✅ Implemented | Yes | ⚠️ Not tested |
| CelesTrak | ✅ Implemented | No | ⚠️ Not tested |
| USGS Earthquakes | ✅ Implemented | No | ⚠️ Not tested |
| NASA FIRMS | ✅ Implemented | Yes | ⚠️ Not tested |
| Copernicus CDSE | ✅ Implemented | Optional | ⚠️ Not tested |
| ESA | ✅ Registered | N/A | N/A |
| EUMETSAT | ✅ Registered | N/A | N/A |
| Destination Earth | ✅ Registered | N/A | N/A |

---

## Known Limitations

### RC1 Limitations

1. **No runtime verification** — Code is complete but not tested against live providers in this environment
2. **Simplified vessel tracking** — AISStream requires WebSocket implementation for real-time data
3. **No weather layers** — Wind, radar, clouds not yet implemented
4. **No camera layers** — CCTV and ALPR not yet implemented
5. **No Ask Earth/MCP** — Tool catalog defined but not exposed
6. **Demo mode only** — Live provider testing requires API keys and network access

### Provider-Specific Limitations

- **OpenSky**: Anonymous access is rate-limited; authenticated access recommended
- **AISStream**: Requires API key; WebSocket implementation needed for real-time
- **NASA FIRMS**: Requires MAP_KEY; 24-hour data window
- **Copernicus CDSE**: STAC search implemented; data download not yet implemented

---

## Architecture

### Backend Stack
- **Python 3.11+** with FastAPI
- **Pydantic v2** for data validation
- **SQLAlchemy 2.x** with async support
- **PostgreSQL 16** with PostGIS and pgvector
- **Alembic** for database migrations
- **MinIO** for S3-compatible object storage
- **Redpanda** for event streaming

### Frontend Stack
- **React 18** with TypeScript
- **Vite** for build tooling
- **CesiumJS** for 3D globe
- **Tailwind CSS** for styling
- **Framer Motion** for animations

### Orbital Mechanics
- **sgp4 library** for real satellite propagation
- **TLE parsing** with validation
- **Topocentric calculations** for pass prediction
- **Coordinate transformations** (TEME → ECEF → Geodetic)

---

## Security

### Implemented Controls
- ✅ No arbitrary URL proxying
- ✅ Provider credentials stored server-side only
- ✅ Bounding box validation
- ✅ Result limit enforcement
- ✅ Timeout and retry handling
- ✅ No secrets in frontend bundle
- ✅ No face/person recognition
- ✅ No private surveillance APIs

### Privacy Boundaries
- Military ADS-B shows only public broadcast data
- No classified mission inference
- No weapon targeting capabilities
- No named-person tracking

---

## Roadmap

### Phase 0D.2 — Weather + Earth Observation (Next)
- Wind visualization (NOAA GFS, ECMWF IFS)
- Rain radar (NOAA nowCOAST)
- Satellite clouds (GOES)
- Lightning density
- Cyclone tracking
- Recent satellite imagery search

### Phase 0D.3 — Cameras + Infrastructure
- Public CCTV integration
- ALPR infrastructure mapping
- Datacenter visualization
- Dam monitoring
- Submarine cable mapping (license permitting)

### Phase 1 — Digital Twin Core
- Virtual satellite constellation
- Orbital simulation
- Synthetic pass generation
- Earth replay engine

---

## Support

### Documentation
- [Architecture Decision Records](docs/adr/README.md)
- [Space Federation Guide](docs/space-federation/README.md)
- [Security Threat Model](docs/security/threat-model.md)
- [Upstream Parity Manifest](docs/upstream/GODS-EYE-VIEW-PARITY.md)

### Runbooks
- [Phase 0 Validation](docs/runbooks/phase0-validation.md)
- [Try RC1 Guide](docs/runbooks/TRY-RC1.md)

---

## License

Proprietary — All rights reserved.

Third-party data sources are subject to their own licenses. See [THIRD-PARTY-LICENSES.md](docs/upstream/THIRD-PARTY-LICENSES.md) for details.

---

## Credits

Earth Intelligence OS is inspired by the capability architecture of [God's Eye View](https://github.com/bilawalsidhu/gods-eye-view) by Bilawal Sidhu and Sameh Khamis at Halfpixel.

---

**Release Candidate 1 — Ready for Human Testing**
