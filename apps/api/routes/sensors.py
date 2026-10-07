"""Sensor CRUD endpoints."""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from packages.contracts.domain import Sensor, SensorType

router = APIRouter()

_sensors: dict[UUID, Sensor] = {}


class SensorCreate(BaseModel):
    """Request body for creating a sensor."""
    satellite_id: UUID
    sensor_type: SensorType
    name: str = Field(min_length=1, max_length=255)
    status: str = Field(default="ACTIVE", max_length=50)


class SensorResponse(BaseModel):
    """Sensor response model."""
    id: UUID
    satellite_id: UUID
    sensor_type: SensorType
    name: str
    status: str
    created_at: str


class PaginatedResponse(BaseModel):
    """Paginated list response."""
    items: list[SensorResponse]
    total: int
    page: int
    per_page: int


@router.get("/sensors", response_model=PaginatedResponse)
async def list_sensors(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
) -> PaginatedResponse:
    """List sensors with pagination."""
    all_items = list(_sensors.values())
    total = len(all_items)
    start = (page - 1) * per_page
    end = start + per_page
    page_items = all_items[start:end]

    return PaginatedResponse(
        items=[
            SensorResponse(
                id=s.id,
                satellite_id=s.satellite_id,
                sensor_type=s.sensor_type,
                name=s.name,
                status=s.status,
                created_at=s.created_at.isoformat(),
            )
            for s in page_items
        ],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.post("/sensors", response_model=SensorResponse, status_code=201)
async def create_sensor(body: SensorCreate) -> SensorResponse:
    """Register a new sensor."""
    sensor = Sensor(
        satellite_id=body.satellite_id,
        sensor_type=body.sensor_type,
        name=body.name,
        status=body.status,
    )
    _sensors[sensor.id] = sensor

    return SensorResponse(
        id=sensor.id,
        satellite_id=sensor.satellite_id,
        sensor_type=sensor.sensor_type,
        name=sensor.name,
        status=sensor.status,
        created_at=sensor.created_at.isoformat(),
    )


@router.get("/sensors/{sensor_id}", response_model=SensorResponse)
async def get_sensor(sensor_id: UUID) -> SensorResponse:
    """Get sensor by ID."""
    sensor = _sensors.get(sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail={"code": "SENSOR_NOT_FOUND", "message": f"Sensor {sensor_id} not found"})

    return SensorResponse(
        id=sensor.id,
        satellite_id=sensor.satellite_id,
        sensor_type=sensor.sensor_type,
        name=sensor.name,
        status=sensor.status,
        created_at=sensor.created_at.isoformat(),
    )
