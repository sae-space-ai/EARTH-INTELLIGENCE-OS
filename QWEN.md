# EARTH INTELLIGENCE OS — Project Memory

## PROJECT
Earth Intelligence OS — Planetary-scale intelligence platform.

## CORE PRINCIPLES

1. Raw scientific data is immutable evidence.
2. Scientific knowledge states must remain distinct: OBSERVED | INFERRED | FORECAST | SIMULATED.
3. Generative AI may analyze, propose and recommend.
4. Generative AI must NEVER directly command spacecraft actuators.
   Future control chain: AI Proposal → Mission Planner → Digital Twin → Policy Engine → Authorization → Flight Operations → Uplink → Spacecraft.
5. Every scientific result must support provenance.
6. Every model must be versioned.
7. Important operations must preserve trace_id and correlation_id.
8. Code is not considered complete until tests/validation run.
9. No fake implementations.
10. No hidden secrets.
11. Do not break existing validated components.

## ARCHITECTURE
- Modular monorepo (Python backend + React frontend Control Room prototype).
- Event-driven, API-first, cloud-native ground segment.
- Prepared for edge computing orbital (Phase 1+).
- PostgreSQL + PostGIS + pgvector for geospatial core.
- S3-compatible object storage (MinIO local, S3/GCS production).
- Kafka-compatible event bus (Redpanda local).
- Transactional outbox for guaranteed event delivery.

## CODE STYLE
- Python: PEP 8, type hints, docstrings on public interfaces.
- Small functions, clear responsibilities.
- No god classes, no global mutable state, no hardcoded secrets.
- No catch-all exceptions without logging.

## VALIDATION
```
make check   # Runs: ruff check, ruff format --check, mypy, pytest
```

## SECRETS POLICY
- Never commit real credentials.
- Use .env.example for templates.
- Pre-commit hooks check for secrets.

## DEPENDENCY POLICY
- Verify necessity before adding.
- Pin versions in pyproject.toml.
- Prefer stdlib where reasonable.

## VERSIONING
- Semantic versioning for API and events.
- Schema versioning for all event contracts.
- Git SHA tracked in model versions.

## RAW DATA RULE
- RAW assets are immutable evidence.
- No silent overwrites.
- SHA-256 checksums mandatory.
- All transformations create new assets with provenance.

## KNOWLEDGE STATES
- OBSERVED: Direct sensor measurement.
- INFERRED: Model analysis of observations.
- FORECAST: Predictive model output.
- SIMULATED: Digital Twin / World Model output.
- Never mix silently. Always label.

## AI BOUNDARY
- AI can analyze, propose, recommend.
- AI CANNOT send commands to spacecraft.
- Hard network/policy boundary enforced.

## DEFINITION OF DONE
- Code exists and imports resolve.
- Configuration loads correctly.
- Tests pass.
- Lint/type-check pass.
- Documentation matches implementation.
- No TODO/FIXME in required paths.
