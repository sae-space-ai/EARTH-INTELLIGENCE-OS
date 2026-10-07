"""Federation API routes."""

from __future__ import annotations

from typing import Any, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from packages.federation.init import create_provider_registry, create_connector_registry
from packages.federation.models import SpaceDataProvider
from packages.federation.resolver import SpaceCapabilityResolver, SpaceCapability
from packages.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()

# Initialize registries
_provider_registry = create_provider_registry()
_connector_registry = create_connector_registry(_provider_registry)
_resolver = SpaceCapabilityResolver(_provider_registry, _connector_registry)


class ProviderResponse(BaseModel):
    """Provider response model."""
    code: str
    name: str
    organization_type: Optional[str]
    country_or_region: Optional[str]
    base_url: Optional[str]
    status: str
    capabilities: list[str]


class MissionResponse(BaseModel):
    """Mission response model."""
    id: UUID
    mission_code: str
    name: str
    lifecycle_status: str
    provider_code: str


class SearchRequest(BaseModel):
    """Federated search request."""
    geometry: Optional[dict[str, Any]] = None
    bbox: Optional[list[float]] = None
    datetime_range: Optional[dict[str, str]] = None
    provider: Optional[str] = None
    mission: Optional[str] = None
    sensor_type: Optional[str] = None
    collection: Optional[str] = None
    max_cloud_cover: Optional[float] = None
    limit: int = Query(10, ge=1, le=100)


class SearchResult(BaseModel):
    """Search result."""
    provider: str
    external_item_id: str
    datetime: str
    geometry: dict[str, Any]
    sensor_type: Optional[str]
    cloud_cover: Optional[float]


@router.get("/space/providers", response_model=list[ProviderResponse])
async def list_providers() -> list[ProviderResponse]:
    """List all registered space providers."""
    providers = _provider_registry.list_all()
    return [
        ProviderResponse(
            code=p.code,
            name=p.name,
            organization_type=p.organization_type,
            country_or_region=p.country_or_region,
            base_url=p.base_url,
            status=p.status,
            capabilities=[c.value for c in p.capabilities],
        )
        for p in providers
    ]


@router.get("/space/providers/{provider_code}", response_model=ProviderResponse)
async def get_provider(provider_code: str) -> ProviderResponse:
    """Get provider by code."""
    provider = _provider_registry.get(provider_code)
    if not provider:
        raise HTTPException(status_code=404, detail=f"Provider {provider_code} not found")

    return ProviderResponse(
        code=provider.code,
        name=provider.name,
        organization_type=provider.organization_type,
        country_or_region=provider.country_or_region,
        base_url=provider.base_url,
        status=provider.status,
        capabilities=[c.value for c in provider.capabilities],
    )


@router.get("/space/missions", response_model=list[MissionResponse])
async def list_missions(provider: Optional[str] = None) -> list[MissionResponse]:
    """List missions from all or specific provider."""
    missions = []

    if provider:
        connector = _connector_registry.get(provider)
        if connector:
            provider_missions = await connector.list_missions()
            missions.extend([(provider, m) for m in provider_missions])
    else:
        for connector in _connector_registry.list_all():
            provider_missions = await connector.list_missions()
            missions.extend([(connector.provider.code, m) for m in provider_missions])

    return [
        MissionResponse(
            id=m.id,
            mission_code=m.mission_code,
            name=m.name,
            lifecycle_status=m.lifecycle_status.value,
            provider_code=provider_code,
        )
        for provider_code, m in missions
    ]


@router.get("/space/provider-health")
async def provider_health() -> dict[str, str]:
    """Get health status for all providers."""
    return {code: status.value for code, status in _provider_registry.get_all_health().items()}


@router.post("/space/search", response_model=list[SearchResult])
async def federated_search(request: SearchRequest) -> list[SearchResult]:
    """Perform federated search across providers."""
    from datetime import datetime

    results = []

    # Determine which connectors to search
    connectors = []
    if request.provider:
        connector = _connector_registry.get(request.provider)
        if connector:
            connectors.append(connector)
    else:
        connectors = _connector_registry.get_available()

    # Parse datetime range
    datetime_range = None
    if request.datetime_range:
        start = datetime.fromisoformat(request.datetime_range.get("start", ""))
        end = datetime.fromisoformat(request.datetime_range.get("end", ""))
        datetime_range = (start, end)

    # Build filters
    filters: dict[str, Any] = {}
    if request.mission:
        filters["mission"] = request.mission
    if request.sensor_type:
        filters["sensor_type"] = request.sensor_type
    if request.max_cloud_cover is not None:
        filters["max_cloud_cover"] = request.max_cloud_cover

    # Search each connector
    for connector in connectors:
        try:
            candidates = await connector.search(
                geometry=request.geometry,
                datetime_range=datetime_range,
                collections=[request.collection] if request.collection else None,
                filters=filters,
            )

            for candidate in candidates[:request.limit]:
                results.append(
                    SearchResult(
                        provider=candidate.provider,
                        external_item_id=candidate.external_item_id,
                        datetime=candidate.datetime.isoformat(),
                        geometry=candidate.geometry,
                        sensor_type=candidate.sensor_type,
                        cloud_cover=candidate.cloud_cover,
                    )
                )

        except Exception:
            logger.exception("Search failed for provider", extra={"provider": connector.provider.code})

    return results[:request.limit]


@router.get("/space/capabilities")
async def list_capabilities() -> list[str]:
    """List all supported capabilities."""
    return [c.value for c in _resolver.get_all_capabilities()]


@router.post("/space/resolve-capability")
async def resolve_capability(
    capability: str,
    aoi: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Resolve a capability to providers and mappings."""
    try:
        cap = SpaceCapability(capability)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Unknown capability: {capability}")

    mappings = _resolver.get_capability_mappings(cap)
    return {
        "capability": capability,
        "mappings": mappings,
        "provider_count": len(set(m.get("provider") for m in mappings)),
    }
