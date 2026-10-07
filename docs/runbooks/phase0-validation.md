# Phase 0 Validation Runbook

## Local Validation

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Node.js 18+

### Steps

```bash
# 1. Install Python dependencies
make install

# 2. Copy environment configuration
cp .env.example .env

# 3. Run code quality checks
make check
# Runs: ruff check, ruff format --check, mypy, pytest

# 4. Start infrastructure
make compose-up

# 5. Wait for services to be healthy
docker compose ps

# 6. Verify PostgreSQL with PostGIS + pgvector
docker compose exec postgres psql -U postgres -d earth_intelligence -c "SELECT PostGIS_Version();"
docker compose exec postgres psql -U postgres -d earth_intelligence -c "SELECT extversion FROM pg_extension WHERE extname = 'vector';"

# 7. Run database migrations
make migrate

# 8. Start API
make api &

# 9. Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8000/ready
curl http://localhost:8000/version

# 10. Test CRUD operations
curl -X POST http://localhost:8000/api/v1/satellites \
  -H "Content-Type: application/json" \
  -d '{"name": "TestSat-1", "platform_type": "CUBESAT"}'

# 11. Start worker
make worker

# 12. Build frontend
npm run build

# 13. Cleanup
make compose-down
```

## GitHub Actions Validation

### Workflow Jobs

1. **quality**: Ruff lint, format check, mypy
2. **unit-tests**: pytest tests/unit
3. **frontend**: npm build
4. **docker-build**: Build API, Worker, PostgreSQL images
5. **integration**: Full integration with PostGIS, MinIO, Redpanda

### Integration Test Includes
- PostGIS extension verification
- Alembic migration
- API startup
- CRUD operations
- Federation API
- STAC mapping
- Storage checksums

### Triggering
- Push to main/develop
- Pull requests to main/develop

## Validation Status Categories

| Category | Description |
|----------|-------------|
| IMPLEMENTED | Code exists and is structurally correct |
| STATICALLY REVIEWED | Code inspected, no runtime execution |
| LOCALLY EXECUTED | Run on local machine with all deps |
| CI EXECUTED | Passed in GitHub Actions |
| NETWORK TESTED | Tested against live external APIs |
| AUTH BLOCKED | Requires credentials not available |
| ENVIRONMENT BLOCKED | Sandbox lacks required tools |

## Known Limitations

- Qwen sandbox lacks Python/Docker runtime
- External provider tests require network + credentials
- Full E2E validation requires complete infrastructure stack

## Troubleshooting

### PostgreSQL fails to start
- Check Docker logs: `docker compose logs postgres`
- Verify port 5432 is free
- Check init.sql syntax

### Migrations fail
- Ensure database is healthy
- Check DATABASE_URL in .env
- Run `alembic current` to see state

### API fails to start
- Check dependencies are installed
- Verify DATABASE_URL is accessible
- Check logs for import errors

### Tests fail
- Run `pytest -v` for details
- Check test database is clean
- Verify environment variables
