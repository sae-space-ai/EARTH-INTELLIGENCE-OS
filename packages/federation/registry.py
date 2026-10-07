"""Provider and connector registry for European Space Federation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from packages.federation.models import (
    ExternalCollection,
    ExternalMission,
    ExternalObservationCandidate,
    ExternalSpaceService,
    ExternalSpacecraft,
    ExternalInstrument,
    ProviderCapability,
    ProviderHealthStatus,
    SpaceDataProvider,
)
from packages.core.logging import get_logger

logger = get_logger(__name__)


class SpaceProviderConnector(ABC):
    """Abstract connector interface for space data providers.

    Provider-neutral abstraction that allows federation with any
    European space data provider supporting standard interfaces.
    """

    def __init__(self, provider: SpaceDataProvider) -> None:
        self._provider = provider
        self._health = ProviderHealthStatus.NOT_CONFIGURED

    @property
    def provider(self) -> SpaceDataProvider:
        """Get the associated provider."""
        return self._provider

    @property
    def health(self) -> ProviderHealthStatus:
        """Get current health status."""
        return self._health

    @abstractmethod
    async def get_provider_info(self) -> dict[str, Any]:
        """Get provider information."""

    @abstractmethod
    async def list_missions(self) -> list[ExternalMission]:
        """List available missions."""

    @abstractmethod
    async def list_spacecraft(self) -> list[ExternalSpacecraft]:
        """List available spacecraft."""

    @abstractmethod
    async def list_instruments(self) -> list[ExternalInstrument]:
        """List available instruments."""

    @abstractmethod
    async def list_collections(self) -> list[ExternalCollection]:
        """List available data collections."""

    @abstractmethod
    async def get_collection(self, collection_id: str) -> Optional[ExternalCollection]:
        """Get a specific collection by ID."""

    @abstractmethod
    async def search(
        self,
        geometry: Optional[dict[str, Any]] = None,
        datetime_range: Optional[tuple[datetime, datetime]] = None,
        collections: Optional[list[str]] = None,
        filters: Optional[dict[str, Any]] = None,
    ) -> list[ExternalObservationCandidate]:
        """Search for observation candidates."""

    @abstractmethod
    async def get_item(self, external_item_id: str) -> Optional[ExternalObservationCandidate]:
        """Get a specific item by external ID."""

    @abstractmethod
    async def get_asset_metadata(
        self, external_item_id: str, asset_key: str
    ) -> Optional[dict[str, Any]]:
        """Get metadata for a specific asset."""

    @abstractmethod
    async def get_download_options(
        self, external_item_id: str
    ) -> list[dict[str, Any]]:
        """Get available download options for an item."""

    @abstractmethod
    async def health_check(self) -> ProviderHealthStatus:
        """Check provider health."""

    @abstractmethod
    async def get_capabilities(self) -> list[ProviderCapability]:
        """Get provider capabilities."""


class ProviderRegistry:
    """Registry of space data providers."""

    def __init__(self) -> None:
        self._providers: dict[str, SpaceDataProvider] = {}
        self._health_status: dict[str, ProviderHealthStatus] = {}

    def register(self, provider: SpaceDataProvider) -> None:
        """Register a provider."""
        self._providers[provider.code] = provider
        self._health_status[provider.code] = ProviderHealthStatus.NOT_CONFIGURED
        logger.info("Provider registered", extra={"provider_code": provider.code})

    def get(self, code: str) -> Optional[SpaceDataProvider]:
        """Get provider by code."""
        return self._providers.get(code)

    def list_all(self) -> list[SpaceDataProvider]:
        """List all registered providers."""
        return list(self._providers.values())

    def update_health(self, code: str, status: ProviderHealthStatus) -> None:
        """Update provider health status."""
        if code in self._providers:
            self._health_status[code] = status
            logger.info(
                "Provider health updated",
                extra={"provider_code": code, "status": status.value},
            )

    def get_health(self, code: str) -> ProviderHealthStatus:
        """Get provider health status."""
        return self._health_status.get(code, ProviderHealthStatus.NOT_CONFIGURED)

    def get_all_health(self) -> dict[str, ProviderHealthStatus]:
        """Get health status for all providers."""
        return dict(self._health_status)


class ConnectorRegistry:
    """Registry of provider connectors."""

    def __init__(self) -> None:
        self._connectors: dict[str, SpaceProviderConnector] = {}

    def register(self, connector: SpaceProviderConnector) -> None:
        """Register a connector."""
        code = connector.provider.code
        self._connectors[code] = connector
        logger.info("Connector registered", extra={"provider_code": code})

    def get(self, code: str) -> Optional[SpaceProviderConnector]:
        """Get connector by provider code."""
        return self._connectors.get(code)

    def list_all(self) -> list[SpaceProviderConnector]:
        """List all registered connectors."""
        return list(self._connectors.values())

    def get_available(self) -> list[SpaceProviderConnector]:
        """Get connectors for available providers."""
        return [
            c for c in self._connectors.values()
            if c.health == ProviderHealthStatus.AVAILABLE
        ]
