"""Space capability resolver for European Space Federation."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from packages.federation.models import (
    ExternalCollection,
    ExternalObservationCandidate,
    ProviderCapability,
)
from packages.federation.registry import ConnectorRegistry, ProviderRegistry
from packages.core.logging import get_logger

logger = get_logger(__name__)


class SpaceCapability(str, Enum):
    """High-level space capabilities that can be resolved to providers."""
    GROUND_DEFORMATION = "GROUND_DEFORMATION"
    LAND_MULTISPECTRAL = "LAND_MULTISPECTRAL"
    VEGETATION = "VEGETATION"
    OCEAN = "OCEAN"
    ATMOSPHERE = "ATMOSPHERE"
    WEATHER = "WEATHER"
    CLIMATE = "CLIMATE"
    POSITIONING = "POSITIONING"
    HIGH_ACCURACY_POSITIONING = "HIGH_ACCURACY_POSITIONING"
    NAVIGATION_AUTHENTICATION = "NAVIGATION_AUTHENTICATION"
    SPACE_WEATHER = "SPACE_WEATHER"
    SPACE_SITUATIONAL_AWARENESS = "SPACE_SITUATIONAL_AWARENESS"
    EMERGENCY_RESPONSE = "EMERGENCY_RESPONSE"


# Capability to provider/collection mappings
CAPABILITY_MAPPINGS: dict[SpaceCapability, list[dict[str, Any]]] = {
    SpaceCapability.GROUND_DEFORMATION: [
        {"provider": "COPERNICUS_CDSE", "mission": "SENTINEL-1", "sensor_type": "SAR"},
    ],
    SpaceCapability.LAND_MULTISPECTRAL: [
        {"provider": "COPERNICUS_CDSE", "mission": "SENTINEL-2", "sensor_type": "MULTISPECTRAL"},
    ],
    SpaceCapability.VEGETATION: [
        {"provider": "COPERNICUS_CDSE", "mission": "SENTINEL-2", "sensor_type": "MULTISPECTRAL"},
        {"provider": "COPERNICUS_CDSE", "mission": "SENTINEL-3", "sensor_type": "OCEAN_COLOR"},
    ],
    SpaceCapability.OCEAN: [
        {"provider": "COPERNICUS_CDSE", "mission": "SENTINEL-3", "sensor_type": "OCEAN_COLOR"},
        {"provider": "COPERNICUS_CDSE", "mission": "SENTINEL-6", "sensor_type": "RADAR_ALTIMETER"},
        {"provider": "COPERNICUS_SERVICES", "service": "CMEMS"},
        {"provider": "EUMETSAT", "sensor_type": "MICROWAVE_RADIOMETER"},
    ],
    SpaceCapability.ATMOSPHERE: [
        {"provider": "COPERNICUS_CDSE", "mission": "SENTINEL-5P", "sensor_type": "ATMOSPHERIC_SPECTROMETER"},
        {"provider": "COPERNICUS_SERVICES", "service": "CAMS"},
    ],
    SpaceCapability.WEATHER: [
        {"provider": "EUMETSAT", "mission": "METEOSAT", "sensor_type": "OPTICAL"},
        {"provider": "EUMETSAT", "mission": "MTG", "sensor_type": "OPTICAL"},
        {"provider": "EUMETSAT", "mission": "METOP", "sensor_type": "ATMOSPHERIC_SPECTROMETER"},
    ],
    SpaceCapability.CLIMATE: [
        {"provider": "COPERNICUS_SERVICES", "service": "C3S"},
        {"provider": "DESTINATION_EARTH", "capability": "DIGITAL_TWIN"},
    ],
    SpaceCapability.POSITIONING: [
        {"provider": "GALILEO", "service": "GALILEO_OPEN"},
        {"provider": "EGNOS", "service": "EGNOS_OPEN"},
    ],
    SpaceCapability.HIGH_ACCURACY_POSITIONING: [
        {"provider": "GALILEO", "service": "GALILEO_HAS"},
    ],
    SpaceCapability.NAVIGATION_AUTHENTICATION: [
        {"provider": "GALILEO", "service": "GALILEO_OSNMA"},
    ],
    SpaceCapability.SPACE_WEATHER: [
        {"provider": "ESA_SPACE_WEATHER"},
    ],
    SpaceCapability.SPACE_SITUATIONAL_AWARENESS: [
        {"provider": "EU_SST"},
        {"provider": "ESA_SPACE_SAFETY"},
    ],
    SpaceCapability.EMERGENCY_RESPONSE: [
        {"provider": "COPERNICUS_SERVICES", "service": "CEMS"},
    ],
}


class SpaceCapabilityResolver:
    """Resolves high-level capabilities to providers and data sources."""

    def __init__(
        self,
        provider_registry: ProviderRegistry,
        connector_registry: ConnectorRegistry,
    ) -> None:
        self._provider_registry = provider_registry
        self._connector_registry = connector_registry

    async def find_sources(
        self,
        capability: SpaceCapability,
        aoi: Optional[dict[str, Any]] = None,
        time_range: Optional[tuple[datetime, datetime]] = None,
        constraints: Optional[dict[str, Any]] = None,
    ) -> list[ExternalObservationCandidate]:
        """Find data sources for a given capability.

        Args:
            capability: The capability to resolve.
            aoi: Area of interest (GeoJSON geometry).
            time_range: Time range tuple (start, end).
            constraints: Additional constraints (e.g., max_cloud_cover).

        Returns:
            List of observation candidates from matching providers.
        """
        mappings = CAPABILITY_MAPPINGS.get(capability, [])
        if not mappings:
            logger.warning("No mappings for capability", extra={"capability": capability.value})
            return []

        results: list[ExternalObservationCandidate] = []

        for mapping in mappings:
            provider_code = mapping.get("provider")
            connector = self._connector_registry.get(provider_code)

            if not connector:
                logger.debug(
                    "No connector for provider",
                    extra={"provider_code": provider_code, "capability": capability.value},
                )
                continue

            try:
                # Build search filters from mapping
                filters: dict[str, Any] = {}
                if "mission" in mapping:
                    filters["mission"] = mapping["mission"]
                if "sensor_type" in mapping:
                    filters["sensor_type"] = mapping["sensor_type"]
                if "service" in mapping:
                    filters["service"] = mapping["service"]
                if "capability" in mapping:
                    filters["capability"] = mapping["capability"]

                # Merge with user constraints
                if constraints:
                    filters.update(constraints)

                # Search provider
                candidates = await connector.search(
                    geometry=aoi,
                    datetime_range=time_range,
                    filters=filters,
                )

                results.extend(candidates)
                logger.info(
                    "Found candidates from provider",
                    extra={
                        "provider_code": provider_code,
                        "capability": capability.value,
                        "count": len(candidates),
                    },
                )

            except Exception:
                logger.exception(
                    "Error searching provider",
                    extra={"provider_code": provider_code, "capability": capability.value},
                )

        return results

    def get_capability_mappings(self, capability: SpaceCapability) -> list[dict[str, Any]]:
        """Get provider mappings for a capability."""
        return CAPABILITY_MAPPINGS.get(capability, [])

    def get_all_capabilities(self) -> list[SpaceCapability]:
        """Get all supported capabilities."""
        return list(SpaceCapability)
