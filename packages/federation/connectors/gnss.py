"""GNSS connectors for Galileo and EGNOS."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from packages.federation.models import *
from packages.federation.registry import SpaceProviderConnector
from packages.core.logging import get_logger

logger = get_logger(__name__)


class GalileoConnector(SpaceProviderConnector):
    """Galileo navigation connector."""

    def __init__(self, provider: SpaceDataProvider) -> None:
        super().__init__(provider)
        self._health = ProviderHealthStatus.NOT_CONFIGURED

    async def get_provider_info(self) -> dict[str, Any]:
        return {"code": self._provider.code, "name": self._provider.name}

    async def list_missions(self) -> list[ExternalMission]:
        return [
            ExternalMission(
                provider_id=self._provider.id,
                mission_code="GALILEO",
                name="Galileo",
                description="European GNSS",
                lifecycle_status=MissionLifecycleStatus.OPERATIONAL,
            ),
        ]

    async def list_spacecraft(self) -> list[ExternalSpacecraft]:
        return []

    async def list_instruments(self) -> list[ExternalInstrument]:
        return []

    async def list_collections(self) -> list[ExternalCollection]:
        return []

    async def get_collection(self, collection_id: str) -> Optional[ExternalCollection]:
        return None

    async def search(
        self,
        geometry: Optional[dict[str, Any]] = None,
        datetime_range: Optional[tuple[datetime, datetime]] = None,
        collections: Optional[list[str]] = None,
        filters: Optional[dict[str, Any]] = None,
    ) -> list[ExternalObservationCandidate]:
        return []

    async def get_item(self, external_item_id: str) -> Optional[ExternalObservationCandidate]:
        return None

    async def get_asset_metadata(self, external_item_id: str, asset_key: str) -> Optional[dict[str, Any]]:
        return None

    async def get_download_options(self, external_item_id: str) -> list[dict[str, Any]]:
        return []

    async def health_check(self) -> ProviderHealthStatus:
        return ProviderHealthStatus.NOT_CONFIGURED

    async def get_capabilities(self) -> list[ProviderCapability]:
        return [
            ProviderCapability.GNSS,
            ProviderCapability.GNSS_CORRECTIONS,
            ProviderCapability.NAVIGATION_AUTHENTICATION,
        ]


class EGNOSConnector(SpaceProviderConnector):
    """EGNOS augmentation connector."""

    def __init__(self, provider: SpaceDataProvider) -> None:
        super().__init__(provider)
        self._health = ProviderHealthStatus.NOT_CONFIGURED

    async def get_provider_info(self) -> dict[str, Any]:
        return {"code": self._provider.code, "name": self._provider.name}

    async def list_missions(self) -> list[ExternalMission]:
        return [
            ExternalMission(
                provider_id=self._provider.id,
                mission_code="EGNOS",
                name="EGNOS",
                description="European Geostationary Navigation Overlay Service",
                lifecycle_status=MissionLifecycleStatus.OPERATIONAL,
            ),
        ]

    async def list_spacecraft(self) -> list[ExternalSpacecraft]:
        return []

    async def list_instruments(self) -> list[ExternalInstrument]:
        return []

    async def list_collections(self) -> list[ExternalCollection]:
        return []

    async def get_collection(self, collection_id: str) -> Optional[ExternalCollection]:
        return None

    async def search(
        self,
        geometry: Optional[dict[str, Any]] = None,
        datetime_range: Optional[tuple[datetime, datetime]] = None,
        collections: Optional[list[str]] = None,
        filters: Optional[dict[str, Any]] = None,
    ) -> list[ExternalObservationCandidate]:
        return []

    async def get_item(self, external_item_id: str) -> Optional[ExternalObservationCandidate]:
        return None

    async def get_asset_metadata(self, external_item_id: str, asset_key: str) -> Optional[dict[str, Any]]:
        return None

    async def get_download_options(self, external_item_id: str) -> list[dict[str, Any]]:
        return []

    async def health_check(self) -> ProviderHealthStatus:
        return ProviderHealthStatus.NOT_CONFIGURED

    async def get_capabilities(self) -> list[ProviderCapability]:
        return [ProviderCapability.GNSS, ProviderCapability.GNSS_CORRECTIONS]
