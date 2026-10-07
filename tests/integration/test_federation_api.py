"""Integration tests for Federation API endpoints."""

import pytest
from httpx import AsyncClient, ASGITransport

from apps.api.main import app


@pytest.fixture
async def client():
    """Create test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.mark.asyncio
async def test_list_providers(client: AsyncClient):
    """Test listing all space providers."""
    response = await client.get("/api/v1/space/providers")
    assert response.status_code == 200
    providers = response.json()
    assert len(providers) >= 10

    codes = {p["code"] for p in providers}
    assert "COPERNICUS_CDSE" in codes
    assert "EUMETSAT" in codes


@pytest.mark.asyncio
async def test_get_provider(client: AsyncClient):
    """Test getting a specific provider."""
    response = await client.get("/api/v1/space/providers/COPERNICUS_CDSE")
    assert response.status_code == 200
    provider = response.json()
    assert provider["code"] == "COPERNICUS_CDSE"
    assert "STAC" in provider["capabilities"]


@pytest.mark.asyncio
async def test_get_provider_not_found(client: AsyncClient):
    """Test getting non-existent provider."""
    response = await client.get("/api/v1/space/providers/NONEXISTENT")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_missions(client: AsyncClient):
    """Test listing missions."""
    response = await client.get("/api/v1/space/missions")
    assert response.status_code == 200
    missions = response.json()
    assert len(missions) > 0


@pytest.mark.asyncio
async def test_list_missions_by_provider(client: AsyncClient):
    """Test listing missions for specific provider."""
    response = await client.get("/api/v1/space/missions?provider=COPERNICUS_CDSE")
    assert response.status_code == 200
    missions = response.json()
    assert all(m["provider_code"] == "COPERNICUS_CDSE" for m in missions)


@pytest.mark.asyncio
async def test_provider_health(client: AsyncClient):
    """Test provider health endpoint."""
    response = await client.get("/api/v1/space/provider-health")
    assert response.status_code == 200
    health = response.json()
    assert "COPERNICUS_CDSE" in health


@pytest.mark.asyncio
async def test_federated_search(client: AsyncClient):
    """Test federated search endpoint."""
    response = await client.post(
        "/api/v1/space/search",
        json={
            "bbox": [0, 0, 10, 10],
            "limit": 5,
        },
    )
    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)


@pytest.mark.asyncio
async def test_list_capabilities(client: AsyncClient):
    """Test listing capabilities."""
    response = await client.get("/api/v1/space/capabilities")
    assert response.status_code == 200
    capabilities = response.json()
    assert "GROUND_DEFORMATION" in capabilities
    assert "OCEAN" in capabilities


@pytest.mark.asyncio
async def test_resolve_capability(client: AsyncClient):
    """Test capability resolution."""
    response = await client.post(
        "/api/v1/space/resolve-capability?capability=LAND_MULTISPECTRAL",
    )
    assert response.status_code == 200
    result = response.json()
    assert result["capability"] == "LAND_MULTISPECTRAL"
    assert len(result["mappings"]) > 0


@pytest.mark.asyncio
async def test_resolve_unknown_capability(client: AsyncClient):
    """Test resolving unknown capability."""
    response = await client.post(
        "/api/v1/space/resolve-capability?capability=UNKNOWN_CAP",
    )
    assert response.status_code == 400
