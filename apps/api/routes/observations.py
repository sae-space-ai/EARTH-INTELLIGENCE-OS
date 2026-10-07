"""Observation CRUD endpoints with transactional outbox integration."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, Header, HTTPException, Query
from pydantic import BaseModel, Field

from packages.contracts.domain import KnowledgeState, Observation
from packages.contracts.event import EventEnvelope
from packages.contracts.catalog import OBSERVATION_RECEIVED
from packages.events.outbox import OutboxEvent

router = APIRouter()

_observations: dict[UUID, Observation] = {}
_outbox: list[OutboxEvent] = []
_idempotency_keys: dict[str, UUID] = {}


class ObservationCreate(BaseModel):
    """Request body for creating an observation."""
    satellite_id: UUID
    sensor_id: UUID
    acquired_at: datetime
    footprint: dict = Field(description="GeoJSON geometry")
    bbox: list[float] = Field(min_length=4, max_length=4)
    processing_level: str = Field(max_length=50)
    quality_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    raw_asset_id: UUID


class ObservationResponse(BaseModel):
    """Observation response model."""
    id: UUID
    satellite_id: UUID
    sensor_id: UUID
    acquired_at: str
    footprint: dict
    bbox: list[float]
    processing_level: str
    quality_score: Optional[float]
    raw_asset_id: UUID
    knowledge_state: str
    created_at: str


class PaginatedResponse(BaseModel):
    """Paginated list response."""
    items: list[ObservationResponse]
    total: int
    page: int
    per_page: int


@router.get("/observations", response_model=PaginatedResponse)
async def list_observations(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
) -> PaginatedResponse:
    """List observations with pagination."""
    all_items = list(_observations.values())
    total = len(all_items)
    start = (page - 1) * per_page
    end = start + per_page
    page_items = all_items[start:end]

    return PaginatedResponse(
        items=[
            ObservationResponse(
                id=o.id,
                satellite_id=o.satellite_id,
                sensor_id=o.sensor_id,
                acquired_at=o.acquired_at.isoformat(),
                footprint=o.footprint,
                bbox=o.bbox,
                processing_level=o.processing_level,
                quality_score=o.quality_score,
                raw_asset_id=o.raw_asset_id,
                knowledge_state=o.knowledge_state.value,
                created_at=o.created_at.isoformat(),
            )
            for o in page_items
        ],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.post("/observations", response_model=ObservationResponse, status_code=201)
async def create_observation(
    body: ObservationCreate,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
) -> ObservationResponse:
    """Create observation with transactional outbox.

    Implements idempotency via Idempotency-Key header.
    Creates outbox event in same logical transaction.
    """
    # Idempotency check
    if idempotency_key:
        if idempotency_key in _idempotency_keys:
            existing_id = _idempotency_keys[idempotency_key]
            existing = _observations[existing_id]
            return ObservationResponse(
                id=existing.id,
                satellite_id=existing.satellite_id,
                sensor_id=existing.sensor_id,
                acquired_at=existing.acquired_at.isoformat(),
                footprint=existing.footprint,
                bbox=existing.bbox,
                processing_level=existing.processing_level,
                quality_score=existing.quality_score,
                raw_asset_id=existing.raw_asset_id,
                knowledge_state=existing.knowledge_state.value,
                created_at=existing.created_at.isoformat(),
            )

    observation = Observation(
        satellite_id=body.satellite_id,
        sensor_id=body.sensor_id,
        acquired_at=body.acquired_at,
        footprint=body.footprint,
        bbox=body.bbox,
        processing_level=body.processing_level,
        quality_score=body.quality_score,
        raw_asset_id=body.raw_asset_id,
    )

    # Store observation
    _observations[observation.id] = observation

    # Create outbox event (transactional outbox pattern)
    trace_id = uuid4()
    correlation_id = uuid4()
    outbox_event = OutboxEvent(
        event_type=OBSERVATION_RECEIVED.full_name,
        schema_version=OBSERVATION_RECEIVED.version,
        payload={
            "observation_id": str(observation.id),
            "satellite_id": str(observation.satellite_id),
            "sensor_id": str(observation.sensor_id),
        },
        trace_id=trace_id,
        correlation_id=correlation_id,
    )
    _outbox.append(outbox_event)

    # Store idempotency key
    if idempotency_key:
        _idempotency_keys[idempotency_key] = observation.id

    return ObservationResponse(
        id=observation.id,
        satellite_id=observation.satellite_id,
        sensor_id=observation.sensor_id,
        acquired_at=observation.acquired_at.isoformat(),
        footprint=observation.footprint,
        bbox=observation.bbox,
        processing_level=observation.processing_level,
        quality_score=observation.quality_score,
        raw_asset_id=observation.raw_asset_id,
        knowledge_state=observation.knowledge_state.value,
        created_at=observation.created_at.isoformat(),
    )


@router.get("/observations/{observation_id}", response_model=ObservationResponse)
async def get_observation(observation_id: UUID) -> ObservationResponse:
    """Get observation by ID."""
    observation = _observations.get(observation_id)
    if not observation:
        raise HTTPException(
            status_code=404,
            detail={"code": "OBSERVATION_NOT_FOUND", "message": f"Observation {observation_id} not found"},
        )

    return ObservationResponse(
        id=observation.id,
        satellite_id=observation.satellite_id,
        sensor_id=observation.sensor_id,
        acquired_at=observation.acquired_at.isoformat(),
        footprint=observation.footprint,
        bbox=observation.bbox,
        processing_level=observation.processing_level,
        quality_score=observation.quality_score,
        raw_asset_id=observation.raw_asset_id,
        knowledge_state=observation.knowledge_state.value,
        created_at=observation.created_at.isoformat(),
    )
