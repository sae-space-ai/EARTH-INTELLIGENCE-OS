"""FastAPI application — main entry point."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from apps.api.middleware import TraceMiddleware
from apps.api.routes import health, satellites, sensors, observations, events, missions
from packages.core.config import get_settings
from packages.core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler."""
    setup_logging()
    yield


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()

    application = FastAPI(
        title="Earth Intelligence OS",
        description="Planetary-scale intelligence platform API",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Middleware
    application.add_middleware(TraceMiddleware)

    # Routes
    application.include_router(health.router, tags=["Health"])
    application.include_router(satellites.router, prefix="/api/v1", tags=["Satellites"])
    application.include_router(sensors.router, prefix="/api/v1", tags=["Sensors"])
    application.include_router(observations.router, prefix="/api/v1", tags=["Observations"])
    application.include_router(events.router, prefix="/api/v1", tags=["Events"])
    application.include_router(missions.router, prefix="/api/v1", tags=["Missions"])

    # Global exception handler
    @application.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        from packages.core.tracing import get_trace_id
        trace_id = get_trace_id() or "unknown"
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An internal error occurred",
                    "trace_id": trace_id,
                    "details": {},
                }
            },
        )

    return application


app = create_app()
