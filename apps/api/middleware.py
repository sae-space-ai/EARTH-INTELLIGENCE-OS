"""Trace middleware — injects trace/correlation IDs."""

from __future__ import annotations

import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from packages.core.tracing import is_valid_uuid, set_trace_id, set_correlation_id, get_trace_id


class TraceMiddleware(BaseHTTPMiddleware):
    """Middleware that manages trace and correlation IDs.

    - Reads X-Trace-ID from request headers (validates UUID format).
    - Generates new UUID if missing or invalid.
    - Sets trace context for logging.
    - Returns trace ID in response headers.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with trace context."""
        # Extract or generate trace ID
        trace_id = request.headers.get("X-Trace-ID", "")
        if not trace_id or not is_valid_uuid(trace_id):
            trace_id = str(uuid.uuid4())

        # Extract or generate correlation ID
        correlation_id = request.headers.get("X-Correlation-ID", "")
        if not correlation_id or not is_valid_uuid(correlation_id):
            correlation_id = str(uuid.uuid4())

        # Set context
        set_trace_id(trace_id)
        set_correlation_id(correlation_id)

        # Process request
        response = await call_next(request)

        # Add trace headers to response
        response.headers["X-Trace-ID"] = trace_id
        response.headers["X-Correlation-ID"] = correlation_id

        return response
