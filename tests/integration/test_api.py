"""Integration tests for FastAPI endpoints."""

import pytest
from httpx import AsyncClient, ASGITransport
from uuid import uuid4

from apps.api.main import app


@pytest.fixture
async def client():
    """Create test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    """Test /health returns healthy."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_ready_endpoint(client: AsyncClient):
    """Test /ready returns ready status."""
    response = await client.get("/ready")
    assert response.status_code in (200, 503)
    data = response.json()
    assert "status" in data
    assert "checks" in data


@pytest.mark.asyncio
async def test_version_endpoint(client: AsyncClient):
    """Test /version returns version info."""
    response = await client.get("/version")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert data["version"] == "0.1.0"
    assert "environment" in data


@pytest.mark.asyncio
async def test_trace_middleware(client: AsyncClient):
    """Test trace ID middleware."""
    response = await client.get("/health")
    assert "x-trace-id" in response.headers
    assert "x-correlation-id" in response.headers


@pytest.mark.asyncio
async def test_trace_middleware_with_valid_id(client: AsyncClient):
    """Test trace middleware accepts valid UUID."""
    trace_id = str(uuid4())
    response = await client.get("/health", headers={"X-Trace-ID": trace_id})
    assert response.headers["x-trace-id"] == trace_id


@pytest.mark.asyncio
async def test_satellite_crud(client: AsyncClient):
    """Test satellite create/get/list."""
    # Create
    response = await client.post("/api/v1/satellites", json={
        "name": "TestSat-1",
        "platform_type": "CUBESAT",
    })
    assert response.status_code == 201
    data = response.json()
    sat_id = data["id"]
    assert data["name"] == "TestSat-1"

    # Get
    response = await client.get(f"/api/v1/satellites/{sat_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "TestSat-1"

    # List
    response = await client.get("/api/v1/satellites")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert "items" in data
    assert "page" in data


@pytest.mark.asyncio
async def test_sensor_crud(client: AsyncClient):
    """Test sensor create/get/list."""
    sat_id = str(uuid4())

    # Create
    response = await client.post("/api/v1/sensors", json={
        "satellite_id": sat_id,
        "sensor_type": "SAR",
        "name": "SAR-X",
    })
    assert response.status_code == 201
    data = response.json()
    sensor_id = data["id"]

    # Get
    response = await client.get(f"/api/v1/sensors/{sensor_id}")
    assert response.status_code == 200
    assert response.json()["sensor_type"] == "SAR"


@pytest.mark.asyncio
async def test_observation_crud(client: AsyncClient):
    """Test observation create/get/list."""
    # Create
    response = await client.post("/api/v1/observations", json={
        "satellite_id": str(uuid4()),
        "sensor_id": str(uuid4()),
        "acquired_at": "2024-01-15T12:00:00",
        "footprint": {"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]},
        "bbox": [0.0, 0.0, 1.0, 1.0],
        "processing_level": "L1B",
        "raw_asset_id": str(uuid4()),
    })
    assert response.status_code == 201
    data = response.json()
    obs_id = data["id"]
    assert data["knowledge_state"] == "OBSERVED"

    # Get
    response = await client.get(f"/api/v1/observations/{obs_id}")
    assert response.status_code == 200

    # List
    response = await client.get("/api/v1/observations")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_observation_idempotency(client: AsyncClient):
    """Test idempotency key prevents duplicate observations."""
    idem_key = str(uuid4())
    payload = {
        "satellite_id": str(uuid4()),
        "sensor_id": str(uuid4()),
        "acquired_at": "2024-01-15T12:00:00",
        "footprint": {"type": "Point", "coordinates": [0, 0]},
        "bbox": [0.0, 0.0, 0.0, 0.0],
        "processing_level": "L1",
        "raw_asset_id": str(uuid4()),
    }

    # First request
    response1 = await client.post(
        "/api/v1/observations",
        json=payload,
        headers={"Idempotency-Key": idem_key},
    )
    assert response1.status_code == 201
    id1 = response1.json()["id"]

    # Second request with same key
    response2 = await client.post(
        "/api/v1/observations",
        json=payload,
        headers={"Idempotency-Key": idem_key},
    )
    assert response2.status_code == 201
    id2 = response2.json()["id"]

    # Same observation returned
    assert id1 == id2


@pytest.mark.asyncio
async def test_pagination(client: AsyncClient):
    """Test pagination parameters."""
    response = await client.get("/api/v1/satellites?page=1&per_page=5")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["per_page"] == 5


@pytest.mark.asyncio
async def test_mission_request(client: AsyncClient):
    """Test mission request creation."""
    response = await client.post("/api/v1/missions/requests", json={
        "aoi": {"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]},
        "priority": 3,
        "requested_by": "test-user",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "REQUESTED"
    assert data["priority"] == 3
