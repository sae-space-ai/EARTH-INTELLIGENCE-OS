"""Mission request endpoints."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from packages.contracts.domain import MissionRequest

router = APIRouter()

_missions: dict[UUID, MissionRequest] = {}


class MissionRequestCreate(BaseModel):
    """Request body for creating a mission request."""
    aoi: dict = Field(description="GeoJSON geometry for area of interest")
    priority: int = Field(ge=1, le=10)
    requested_by: str = Field(min_length=1, max_length=255)


class MissionRequestResponse(BaseModel):
    """Mission request response model."""
    id: UUID
    aoi: dict
    priority: int
    requested_by: str
    status: str
    created_at: str


@router.post("/missions/requests", response_model=MissionRequestResponse, status_code=201)
async def create_mission_request(body: MissionRequestCreate) -> MissionRequestResponse:
    """Submit a new mission request."""
    mission = MissionRequest(
        aoi=body.aoi,
        priority=body.priority,
        requested_by=body.requested_by,
    )
    _missions[mission.id] = mission

    return MissionRequestResponse(
        id=mission.id,
        aoi=mission.aoi,
        priority=mission.priority,
        requested_by=mission.requested_by,
        status=mission.status,
        created_at=mission.created_at.isoformat(),
    )


@router.get("/missions/requests/{mission_id}", response_model=MissionRequestResponse)
async def get_mission_request(mission_id: UUID) -> MissionRequestResponse:
    """Get mission request by ID."""
    mission = _missions.get(mission_id)
    if not mission:
        raise HTTPException(
            status_code=404,
            detail={"code": "MISSION_NOT_FOUND", "message": f"Mission {mission_id} not found"},
        )

    return MissionRequestResponse(
        id=mission.id,
        aoi=mission.aoi,
        priority=mission.priority,
        requested_by=mission.requested_by,
        status=mission.status,
        created_at=mission.created_at.isoformat(),
    )
