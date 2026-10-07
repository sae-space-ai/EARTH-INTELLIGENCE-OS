"""Satellite CRUD endpoints."""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from packages.contracts.domain import Satellite

router = APIRouter()

# In-memory store for Phase 0 (replace with DB repository in production)
_satellites: dict[UUID, Satellite] = {}


class SatelliteCreate(BaseModel):
    """Request body for creating a satellite."""
    name: str = Field(min_length=1, max_length=255)
    platform_type: str = Field(min_length=1, max_length=100)
    status: str = Field(default="ACTIVE", max_length=50)


class SatelliteResponse(BaseModel):
    """Satellite response model."""
    id: UUID
    name: str
    platform_type: str
    status: str
    created_at: str


class PaginatedResponse(BaseModel):
    """Paginated list response."""
    items: list[SatelliteResponse]
    total: int
    page: int
    per_page: int


@router.get("/satellites", response_model=PaginatedResponse)
async def list_satellites(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
) -> PaginatedResponse:
    """List satellites with pagination."""
    all_items = list(_satellites.values())
    total = len(all_items)
    start = (page - 1) * per_page
    end = start + per_page
    page_items = all_items[start:end]

    return PaginatedResponse(
        items=[
            SatelliteResponse(
                id=s.id,
                name=s.name,
                platform_type=s.platform_type,
                status=s.status,
                created_at=s.created_at.isoformat(),
            )
            for s in page_items
        ],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.post("/satellites", response_model=SatelliteResponse, status_code=201)
async def create_satellite(body: SatelliteCreate) -> SatelliteResponse:
    """Register a new satellite."""
    satellite = Satellite(
        name=body.name,
        platform_type=body.platform_type,
        status=body.status,
    )
    _satellites[satellite.id] = satellite

    return SatelliteResponse(
        id=satellite.id,
        name=satellite.name,
        platform_type=satellite.platform_type,
        status=satellite.status,
        created_at=satellite.created_at.isoformat(),
    )


@router.get("/satellites/{satellite_id}", response_model=SatelliteResponse)
async def get_satellite(satellite_id: UUID) -> SatelliteResponse:
    """Get satellite by ID."""
    satellite = _satellites.get(satellite_id)
    if not satellite:
        raise HTTPException(status_code=404, detail={"code": "SATELLITE_NOT_FOUND", "message": f"Satellite {satellite_id} not found"})

    return SatelliteResponse(
        id=satellite.id,
        name=satellite.name,
        platform_type=satellite.platform_type,
        status=satellite.status,
        created_at=satellite.created_at.isoformat(),
    )
