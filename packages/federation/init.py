"""Federation initialization — registers all European space providers."""

from __future__ import annotations

from packages.federation.models import (
    AccessPolicy,
    ProviderCapability,
    SpaceDataProvider,
)
from packages.federation.registry import ConnectorRegistry, ProviderRegistry
from packages.federation.connectors.cdse import CDSEConnector
from packages.federation.connectors.esa import ESAConnector
from packages.federation.connectors.eumetsat import EUMETSATConnector
from packages.federation.connectors.destine import DestinEConnector
from packages.federation.connectors.gnss import GalileoConnector, EGNOSConnector
from packages.federation.connectors.space_weather import SpaceWeatherConnector, SSAConnector
from packages.core.logging import get_logger

logger = get_logger(__name__)


def create_default_providers() -> list[SpaceDataProvider]:
    """Create default European space providers."""
    return [
        SpaceDataProvider(
            code="COPERNICUS_CDSE",
            name="Copernicus Data Space Ecosystem",
            organization_type="EU_PROGRAMME",
            country_or_region="EU",
            base_url="https://catalogue.dataspace.copernicus.eu",
            documentation_url="https://documentation.dataspace.copernicus.eu",
            capabilities=[
                ProviderCapability.STAC,
                ProviderCapability.ODATA,
                ProviderCapability.CATALOG_SEARCH,
                ProviderCapability.DOWNLOAD,
                ProviderCapability.S3,
                ProviderCapability.OPENEO,
            ],
            access_policy={"policy": AccessPolicy.FREE_REGISTRATION_REQUIRED.value},
        ),
        SpaceDataProvider(
            code="COPERNICUS_SERVICES",
            name="Copernicus Information Services",
            organization_type="EU_PROGRAMME",
            country_or_region="EU",
            base_url="https://copernicus.eu",
            capabilities=[
                ProviderCapability.REST,
                ProviderCapability.CATALOG_SEARCH,
                ProviderCapability.EMERGENCY_PRODUCTS,
            ],
            access_policy={"policy": AccessPolicy.OPEN_ANONYMOUS.value},
        ),
        SpaceDataProvider(
            code="ESA_EARTH_OBSERVATION",
            name="ESA Earth Observation",
            organization_type="INTERGOVERNMENTAL",
            country_or_region="Europe",
            base_url="https://earth.esa.int",
            capabilities=[ProviderCapability.CATALOG_SEARCH],
            access_policy={"policy": AccessPolicy.FREE_REGISTRATION_REQUIRED.value},
        ),
        SpaceDataProvider(
            code="EUMETSAT",
            name="EUMETSAT",
            organization_type="INTERGOVERNMENTAL",
            country_or_region="Europe",
            base_url="https://www.eumetsat.int",
            capabilities=[
                ProviderCapability.CATALOG_SEARCH,
                ProviderCapability.DOWNLOAD,
                ProviderCapability.REST,
            ],
            access_policy={"policy": AccessPolicy.FREE_REGISTRATION_REQUIRED.value},
        ),
        SpaceDataProvider(
            code="DESTINATION_EARTH",
            name="Destination Earth",
            organization_type="EU_PROGRAMME",
            country_or_region="EU",
            base_url="https://destination-earth.eu",
            capabilities=[
                ProviderCapability.DIGITAL_TWIN,
                ProviderCapability.FORECAST,
                ProviderCapability.STAC,
            ],
            access_policy={"policy": AccessPolicy.FREE_REGISTRATION_REQUIRED.value},
        ),
        SpaceDataProvider(
            code="GALILEO",
            name="Galileo",
            organization_type="EU_PROGRAMME",
            country_or_region="EU",
            base_url="https://www.euspa.europa.eu",
            capabilities=[
                ProviderCapability.GNSS,
                ProviderCapability.GNSS_CORRECTIONS,
                ProviderCapability.NAVIGATION_AUTHENTICATION,
            ],
            access_policy={
                "open_service": AccessPolicy.OPEN_ANONYMOUS.value,
                "prs": AccessPolicy.RESTRICTED.value,
            },
        ),
        SpaceDataProvider(
            code="EGNOS",
            name="EGNOS",
            organization_type="EU_PROGRAMME",
            country_or_region="EU",
            capabilities=[
                ProviderCapability.GNSS,
                ProviderCapability.GNSS_CORRECTIONS,
            ],
            access_policy={"policy": AccessPolicy.OPEN_ANONYMOUS.value},
        ),
        SpaceDataProvider(
            code="ESA_SPACE_WEATHER",
            name="ESA Space Weather",
            organization_type="INTERGOVERNMENTAL",
            country_or_region="Europe",
            base_url="https://swe.esa.int",
            capabilities=[ProviderCapability.SPACE_WEATHER, ProviderCapability.HAPI],
            access_policy={"policy": AccessPolicy.OPEN_ANONYMOUS.value},
        ),
        SpaceDataProvider(
            code="EU_SST",
            name="EU Space Surveillance and Tracking",
            organization_type="EU_PROGRAMME",
            country_or_region="EU",
            capabilities=[ProviderCapability.SPACE_SITUATIONAL_AWARENESS],
            access_policy={"policy": AccessPolicy.RESTRICTED.value},
        ),
        SpaceDataProvider(
            code="ESA_SPACE_SAFETY",
            name="ESA Space Safety",
            organization_type="INTERGOVERNMENTAL",
            country_or_region="Europe",
            base_url="https://safety.esa.int",
            capabilities=[ProviderCapability.SPACE_SITUATIONAL_AWARENESS],
            access_policy={"policy": AccessPolicy.OPEN_ANONYMOUS.value},
        ),
    ]


def create_provider_registry() -> ProviderRegistry:
    """Create and populate the provider registry."""
    registry = ProviderRegistry()
    for provider in create_default_providers():
        registry.register(provider)
    logger.info("Provider registry initialized", extra={"count": len(registry.list_all())})
    return registry


def create_connector_registry(provider_registry: ProviderRegistry) -> ConnectorRegistry:
    """Create and populate the connector registry."""
    connector_registry = ConnectorRegistry()

    connector_map = {
        "COPERNICUS_CDSE": CDSEConnector,
        "ESA_EARTH_OBSERVATION": ESAConnector,
        "EUMETSAT": EUMETSATConnector,
        "DESTINATION_EARTH": DestinEConnector,
        "GALILEO": GalileoConnector,
        "EGNOS": EGNOSConnector,
        "ESA_SPACE_WEATHER": SpaceWeatherConnector,
        "EU_SST": SSAConnector,
        "ESA_SPACE_SAFETY": SSAConnector,
    }

    for provider in provider_registry.list_all():
        connector_cls = connector_map.get(provider.code)
        if connector_cls:
            connector = connector_cls(provider)
            connector_registry.register(connector)

    logger.info("Connector registry initialized", extra={"count": len(connector_registry.list_all())})
    return connector_registry
