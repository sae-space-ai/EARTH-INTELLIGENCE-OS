"""Health check endpoints."""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    """Liveness check — process is running."""
    return {"status": "healthy"}


@router.get("/ready")
async def ready() -> JSONResponse:
    """Readiness check — dependencies available.

    Checks database connectivity. Returns 503 if not ready.
    """
    # In Phase 0, we check if database URL is configured
    # Full dependency check would attempt actual connection
    from packages.core.config import get_settings
    settings = get_settings()

    checks: dict[str, bool] = {}

    # Database check
    checks["database"] = bool(settings.database_url)

    # Object storage check
    checks["storage"] = bool(settings.object_storage_endpoint)

    # Event bus check
    checks["event_bus"] = bool(settings.event_bus_brokers)

    all_ready = all(checks.values())

    if all_ready:
        return JSONResponse(content={"status": "ready", "checks": checks})
    else:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "checks": checks},
        )


@router.get("/version")
async def version() -> dict[str, str]:
    """Version information."""
    from packages.core.config import get_settings
    settings = get_settings()

    return {
        "version": "0.1.0",
        "environment": settings.environment,
        "api_version": "v1",
    }
