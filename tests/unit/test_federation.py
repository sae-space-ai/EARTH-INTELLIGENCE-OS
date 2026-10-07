"""Unit tests for European Space Federation layer."""

import pytest
from datetime import datetime
from uuid import uuid4

from packages.federation.models import (
    AccessPolicy,
    ProviderCapability,
    ProviderHealthStatus,
    MissionLifecycleStatus,
    SpaceEnvironmentCategory,
    SpaceDataProvider,
    ExternalMission,
    ExternalSpacecraft,
    ExternalInstrument,
    ExternalCollection,
    ExternalSpaceService,
    ExternalObservationCandidate,
    SpaceEnvironmentObservation,
    CatalogSyncRun,
)
from packages.federation.registry import ProviderRegistry, ConnectorRegistry
from packages.federation.resolver import SpaceCapabilityResolver, SpaceCapability


def test_access_policy_values():
    """Test AccessPolicy enum values."""
    assert AccessPolicy.OPEN_ANONYMOUS.value == "OPEN_ANONYMOUS"
    assert AccessPolicy.RESTRICTED.value == "RESTRICTED"
    assert AccessPolicy.COMMERCIAL.value == "COMMERCIAL"


def test_provider_capability_values():
    """Test ProviderCapability enum values."""
    assert ProviderCapability.STAC.value == "STAC"
    assert ProviderCapability.DOWNLOAD.value == "DOWNLOAD"
    assert ProviderCapability.SPACE_WEATHER.value == "SPACE_WEATHER"


def test_space_data_provider_creation():
    """Test SpaceDataProvider model creation."""
    provider = SpaceDataProvider(
        code="TEST_PROVIDER",
        name="Test Provider",
        organization_type="TEST",
        capabilities=[ProviderCapability.STAC],
    )
    assert provider.code == "TEST_PROVIDER"
    assert provider.status == "ACTIVE"
    assert ProviderCapability.STAC in provider.capabilities


def test_external_mission_creation():
    """Test ExternalMission model creation."""
    mission = ExternalMission(
        provider_id=uuid4(),
        mission_code="TEST-MISSION",
        name="Test Mission",
        lifecycle_status=MissionLifecycleStatus.OPERATIONAL,
    )
    assert mission.mission_code == "TEST-MISSION"
    assert mission.lifecycle_status == MissionLifecycleStatus.OPERATIONAL


def test_external_spacecraft_creation():
    """Test ExternalSpacecraft model creation."""
    spacecraft = ExternalSpacecraft(
        provider_id=uuid4(),
        name="Test Spacecraft",
        lifecycle_status="OPERATIONAL",
    )
    assert spacecraft.name == "Test Spacecraft"


def test_external_instrument_creation():
    """Test ExternalInstrument model creation."""
    instrument = ExternalInstrument(
        provider_id=uuid4(),
        name="Test Instrument",
        sensor_type="SAR",
    )
    assert instrument.sensor_type == "SAR"


def test_external_collection_creation():
    """Test ExternalCollection model creation."""
    collection = ExternalCollection(
        provider_id=uuid4(),
        external_collection_id="test-collection",
        title="Test Collection",
    )
    assert collection.external_collection_id == "test-collection"


def test_external_service_creation():
    """Test ExternalSpaceService model creation."""
    service = ExternalSpaceService(
        provider_id=uuid4(),
        name="Test Service",
        service_type="STAC",
    )
    assert service.service_type == "STAC"


def test_external_observation_candidate_creation():
    """Test ExternalObservationCandidate model creation."""
    candidate = ExternalObservationCandidate(
        provider="TEST",
        external_item_id="item-123",
        datetime=datetime.utcnow(),
        geometry={"type": "Point", "coordinates": [0, 0]},
    )
    assert candidate.provider == "TEST"
    assert candidate.external_item_id == "item-123"


def test_space_environment_observation_creation():
    """Test SpaceEnvironmentObservation model creation."""
    obs = SpaceEnvironmentObservation(
        provider_id=uuid4(),
        observed_at=datetime.utcnow(),
        knowledge_state="OBSERVED",
        category=SpaceEnvironmentCategory.SOLAR_ACTIVITY,
        variable="F10.7",
        value=150.0,
        unit="sfu",
    )
    assert obs.category == SpaceEnvironmentCategory.SOLAR_ACTIVITY


def test_catalog_sync_run_creation():
    """Test CatalogSyncRun model creation."""
    sync = CatalogSyncRun(
        provider_id=uuid4(),
        started_at=datetime.utcnow(),
        status="RUNNING",
    )
    assert sync.status == "RUNNING"
    assert sync.collections_discovered == 0


def test_provider_registry():
    """Test ProviderRegistry operations."""
    registry = ProviderRegistry()
    provider = SpaceDataProvider(code="TEST", name="Test")
    registry.register(provider)

    assert registry.get("TEST") == provider
    assert len(registry.list_all()) == 1


def test_provider_registry_health():
    """Test provider health tracking."""
    registry = ProviderRegistry()
    provider = SpaceDataProvider(code="TEST", name="Test")
    registry.register(provider)

    registry.update_health("TEST", ProviderHealthStatus.AVAILABLE)
    assert registry.get_health("TEST") == ProviderHealthStatus.AVAILABLE


def test_connector_registry():
    """Test ConnectorRegistry operations."""
    registry = ConnectorRegistry()
    assert len(registry.list_all()) == 0


def test_capability_resolver_mappings():
    """Test capability resolver mappings."""
    provider_registry = ProviderRegistry()
    connector_registry = ConnectorRegistry()
    resolver = SpaceCapabilityResolver(provider_registry, connector_registry)

    mappings = resolver.get_capability_mappings(SpaceCapability.LAND_MULTISPECTRAL)
    assert len(mappings) > 0
    assert any(m.get("mission") == "SENTINEL-2" for m in mappings)


def test_capability_resolver_ocean():
    """Test ocean capability resolution."""
    provider_registry = ProviderRegistry()
    connector_registry = ConnectorRegistry()
    resolver = SpaceCapabilityResolver(provider_registry, connector_registry)

    mappings = resolver.get_capability_mappings(SpaceCapability.OCEAN)
    assert len(mappings) > 0
    providers = {m.get("provider") for m in mappings}
    assert "COPERNICUS_CDSE" in providers or "EUMETSAT" in providers


def test_capability_resolver_weather():
    """Test weather capability resolution."""
    provider_registry = ProviderRegistry()
    connector_registry = ConnectorRegistry()
    resolver = SpaceCapabilityResolver(provider_registry, connector_registry)

    mappings = resolver.get_capability_mappings(SpaceCapability.WEATHER)
    assert len(mappings) > 0
    assert any(m.get("provider") == "EUMETSAT" for m in mappings)


def test_capability_resolver_positioning():
    """Test positioning capability resolution."""
    provider_registry = ProviderRegistry()
    connector_registry = ConnectorRegistry()
    resolver = SpaceCapabilityResolver(provider_registry, connector_registry)

    mappings = resolver.get_capability_mappings(SpaceCapability.POSITIONING)
    assert len(mappings) > 0
    assert any(m.get("provider") == "GALILEO" for m in mappings)


def test_capability_resolver_space_weather():
    """Test space weather capability resolution."""
    provider_registry = ProviderRegistry()
    connector_registry = ConnectorRegistry()
    resolver = SpaceCapabilityResolver(provider_registry, connector_registry)

    mappings = resolver.get_capability_mappings(SpaceCapability.SPACE_WEATHER)
    assert len(mappings) > 0
    assert any(m.get("provider") == "ESA_SPACE_WEATHER" for m in mappings)


def test_all_capabilities_listed():
    """Test all capabilities are accessible."""
    provider_registry = ProviderRegistry()
    connector_registry = ConnectorRegistry()
    resolver = SpaceCapabilityResolver(provider_registry, connector_registry)

    capabilities = resolver.get_all_capabilities()
    assert SpaceCapability.GROUND_DEFORMATION in capabilities
    assert SpaceCapability.SPACE_WEATHER in capabilities
    assert len(capabilities) >= 10


def test_federation_init_creates_providers():
    """Test federation initialization creates all providers."""
    from packages.federation.init import create_default_providers

    providers = create_default_providers()
    codes = {p.code for p in providers}

    assert "COPERNICUS_CDSE" in codes
    assert "ESA_EARTH_OBSERVATION" in codes
    assert "EUMETSAT" in codes
    assert "DESTINATION_EARTH" in codes
    assert "GALILEO" in codes
    assert "EGNOS" in codes
    assert "ESA_SPACE_WEATHER" in codes
    assert "EU_SST" in codes
    assert "ESA_SPACE_SAFETY" in codes
    assert len(providers) >= 10
