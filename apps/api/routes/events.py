"""Earth Event endpoints."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from packages.contracts.domain import EarthEvent, KnowledgeState

router = APIRouter()

_events: dict[UUID, EarthEvent] = {}


class EventResponse(BaseModel):
    """Earth Event response model."""
    id: UUID
    event_type: str
    geometry: dict
    first_seen: str
    last_seen: str
    confidence: float
    priority: int
    knowledge_state: str
    created_at: str
    updated_at: str


class PaginatedResponse(BaseModel):
    """Paginated list response."""
    items: list[EventResponse]
    total: int
    page: int
    per_page: int


@router.get("/events", response_model=PaginatedResponse)
async def list_events(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
) -> PaginatedResponse:
    """List Earth Events with pagination."""
    all_items = list(_events.values())
    total = len(all_items)
    start = (page - 1) * per_page
    end = start + per_page
    page_items = all_items[start:end]

    return PaginatedResponse(
        items=[
            EventResponse(
                id=e.id,
                event_type=e.event_type,
                geometry=e.geometry,
                first_seen=e.first_seen.isoformat(),
                last_seen=e.last_seen.isoformat(),
                confidence=e.confidence,
                priority=e.priority,
                knowledge_state=e.knowledge_state.value,
                created_at=e.created_at.isoformat(),
                updated_at=e.updated_at.isoformat(),
            )
            for e in page_items
        ],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/events/{event_id}", response_model=EventResponse)
async def get_event(event_id: UUID) -> EventResponse:
    """Get Earth Event by ID."""
    event = _events.get(event_id)
    if not event:
        raise HTTPException(
            status_code=404,
            detail={"code": "EVENT_NOT_FOUND", "message": f"Event {event_id} not found"},
        )

    return EventResponse(
        id=event.id,
        event_type=event.event_type,
        geometry=event.geometry,
        first_seen=event.first_seen.isoformat(),
        last_seen=event.last_seen.isoformat(),
        confidence=event.confidence,
        priority=event.priority,
        knowledge_state=event.knowledge_state.value,
        created_at=event.created_at.isoformat(),
        updated_at=event.updated_at.isoformat(),
    )
