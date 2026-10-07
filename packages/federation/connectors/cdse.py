"""Copernicus Data Space Ecosystem (CDSE) connector."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

import httpx

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
from packages.federation.registry import SpaceProviderConnector
from packages.core.config import get_settings
from packages.core.logging import get_logger

logger = get_logger(__name__)


class CDSEConnector(SpaceProviderConnector):
    """Connector for Copernicus Data Space Ecosystem.

    Implements STAC-based search and OData API access.
    Supports Sentinel-1, Sentinel-2, Sentinel-3, Sentinel-5P, Sentinel-6.
    """

    def __init__(self, provider: SpaceDataProvider) -> None:
        super().__init__(provider)
        settings = get_settings()
        self._base_url = provider.base_url or "https://catalogue.dataspace.copernicus.eu"
        self._stac_url = f"{self._base_url}/stac"
        self._client_id = getattr(settings, "cdse_client_id", None)
        self._client_secret = getattr(settings, "cdse_client_secret", None)
        self._access_token: Optional[str] = None
        self._http_client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._http_client is None or self._http_client.is_closed:
            self._http_client = httpx.AsyncClient(
                timeout=30.0,
                follow_redirects=True,
            )
        return self._http_client

    async def _authenticate(self) -> bool:
        """Authenticate with CDSE if credentials available."""
        if not self._client_id or not self._client_secret:
            logger.debug("CDSE credentials not configured, using anonymous access")
            return False

        try:
            client = await self._get_client()
            response = await client.post(
                "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                },
                timeout=10.0,
            )
            if response.status_code == 200:
                self._access_token = response.json()["access_token"]
                return True
            else:
                logger.warning("CDSE authentication failed", extra={"status": response.status_code})
                return False
        except Exception:
            logger.exception("CDSE authentication error")
            return False

    async def get_provider_info(self) -> dict[str, Any]:
        """Get CDSE provider information."""
        return {
            "code": self._provider.code,
            "name": self._provider.name,
            "base_url": self._base_url,
            "capabilities": [c.value for c in self._provider.capabilities],
            "stac_url": self._stac_url,
        }

    async def list_missions(self) -> list[ExternalMission]:
        """List Copernicus Sentinel missions."""
        missions = [
            ExternalMission(
                provider_id=self._provider.id,
                mission_code="SENTINEL-1",
                name="Sentinel-1",
                description="SAR constellation for all-weather, day/night imaging",
                programme="Copernicus",
                operator="ESA",
                lifecycle_status="OPERATIONAL",
                launch_date=datetime(2014, 4, 3),
                capabilities=["SAR", "INTERFEROMETRY", "GROUND_DEFORMATION"],
            ),
            ExternalMission(
                provider_id=self._provider.id,
                mission_code="SENTINEL-2",
                name="Sentinel-2",
                description="Multispectral imaging for land monitoring",
                programme="Copernicus",
                operator="ESA",
                lifecycle_status="OPERATIONAL",
                launch_date=datetime(2015, 6, 23),
                capabilities=["MULTISPECTRAL", "LAND", "VEGETATION"],
            ),
            ExternalMission(
                provider_id=self._provider.id,
                mission_code="SENTINEL-3",
                name="Sentinel-3",
                description="Ocean and land monitoring",
                programme="Copernicus",
                operator="ESA",
                lifecycle_status="OPERATIONAL",
                launch_date=datetime(2016, 2, 16),
                capabilities=["OCEAN_COLOR", "LAND", "ATMOSPHERE"],
            ),
            ExternalMission(
                provider_id=self._provider.id,
                mission_code="SENTINEL-5P",
                name="Sentinel-5 Precursor",
                description="Atmospheric composition monitoring",
                programme="Copernicus",
                operator="ESA",
                lifecycle_status="OPERATIONAL",
                launch_date=datetime(2017, 10, 13),
                capabilities=["ATMOSPHERIC_COMPOSITION", "AIR_QUALITY"],
            ),
            ExternalMission(
                provider_id=self._provider.id,
                mission_code="SENTINEL-6",
                name="Sentinel-6 Michael Freilich",
                description="Sea level monitoring",
                programme="Copernicus",
                operator="ESA/EUMETSAT",
                lifecycle_status="OPERATIONAL",
                launch_date=datetime(2020, 11, 21),
                capabilities=["ALTIMETRY", "SEA_LEVEL"],
            ),
        ]
        return missions

    async def list_spacecraft(self) -> list[ExternalSpacecraft]:
        """List Sentinel spacecraft."""
        return [
            ExternalSpacecraft(
                provider_id=self._provider.id,
                name="Sentinel-1A",
                lifecycle_status="ENDED",
                launch_date=datetime(2014, 4, 3),
            ),
            ExternalSpacecraft(
                provider_id=self._provider.id,
                name="Sentinel-1B",
                lifecycle_status="ENDED",
                launch_date=datetime(2016, 4, 25),
            ),
            ExternalSpacecraft(
                provider_id=self._provider.id,
                name="Sentinel-2A",
                lifecycle_status="OPERATIONAL",
                launch_date=datetime(2015, 6, 23),
            ),
            ExternalSpacecraft(
                provider_id=self._provider.id,
                name="Sentinel-2B",
                lifecycle_status="OPERATIONAL",
                launch_date=datetime(2017, 3, 7),
            ),
        ]

    async def list_instruments(self) -> list[ExternalInstrument]:
        """List Sentinel instruments."""
        return [
            ExternalInstrument(
                provider_id=self._provider.id,
                name="C-SAR",
                sensor_type="SAR",
                spatial_resolution="5m x 20m",
                swath="250km",
                frequency="C-band (5.405 GHz)",
                polarizations=["HH", "VV", "HV", "VH"],
            ),
            ExternalInstrument(
                provider_id=self._provider.id,
                name="MSI",
                sensor_type="MULTISPECTRAL",
                spatial_resolution="10m / 20m / 60m",
                swath="290km",
                spectral_bands={"bands": 13, "range": "443-2190nm"},
            ),
        ]

    async def list_collections(self) -> list[ExternalCollection]:
        """List CDSE collections via STAC."""
        try:
            client = await self._get_client()
            response = await client.get(f"{self._stac_url}/collections", timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                collections = []
                for coll in data.get("collections", []):
                    collections.append(
                        ExternalCollection(
                            provider_id=self._provider.id,
                            external_collection_id=coll["id"],
                            title=coll.get("title", coll["id"]),
                            description=coll.get("description"),
                            temporal_extent=coll.get("extent", {}).get("temporal"),
                            spatial_extent=coll.get("extent", {}).get("spatial"),
                            canonical_url=coll.get("links", [{}])[0].get("href") if coll.get("links") else None,
                        )
                    )
                return collections
            else:
                logger.warning("Failed to list CDSE collections", extra={"status": response.status_code})
                return []
        except Exception:
            logger.exception("Error listing CDSE collections")
            return []

    async def get_collection(self, collection_id: str) -> Optional[ExternalCollection]:
        """Get a specific collection."""
        try:
            client = await self._get_client()
            response = await client.get(f"{self._stac_url}/collections/{collection_id}", timeout=10.0)
            if response.status_code == 200:
                coll = response.json()
                return ExternalCollection(
                    provider_id=self._provider.id,
                    external_collection_id=coll["id"],
                    title=coll.get("title", coll["id"]),
                    description=coll.get("description"),
                    temporal_extent=coll.get("extent", {}).get("temporal"),
                    spatial_extent=coll.get("extent", {}).get("spatial"),
                )
            return None
        except Exception:
            logger.exception("Error getting CDSE collection", extra={"collection_id": collection_id})
            return None

    async def search(
        self,
        geometry: Optional[dict[str, Any]] = None,
        datetime_range: Optional[tuple[datetime, datetime]] = None,
        collections: Optional[list[str]] = None,
        filters: Optional[dict[str, Any]] = None,
    ) -> list[ExternalObservationCandidate]:
        """Search CDSE via STAC API."""
        try:
            client = await self._get_client()

            # Build STAC search request
            search_params: dict[str, Any] = {
                "limit": 10,  # Bounded search
            }

            if geometry:
                search_params["intersects"] = geometry

            if datetime_range:
                start, end = datetime_range
                search_params["datetime"] = f"{start.isoformat()}/{end.isoformat()}"

            if collections:
                search_params["collections"] = collections

            # Apply filters
            if filters:
                if "mission" in filters:
                    # Map mission to collection
                    mission_map = {
                        "SENTINEL-1": "sentinel-1-grd",
                        "SENTINEL-2": "sentinel-2-l2a",
                        "SENTINEL-3": "sentinel-3-olci",
                        "SENTINEL-5P": "sentinel-5p-l2",
                    }
                    collection = mission_map.get(filters["mission"])
                    if collection:
                        search_params["collections"] = [collection]

            response = await client.post(
                f"{self._stac_url}/search",
                json=search_params,
                timeout=15.0,
            )

            if response.status_code == 200:
                data = response.json()
                candidates = []
                for feature in data.get("features", []):
                    props = feature.get("properties", {})
                    candidates.append(
                        ExternalObservationCandidate(
                            provider=self._provider.code,
                            mission=props.get("mission"),
                            spacecraft=props.get("platform"),
                            instrument=props.get("instrument"),
                            collection=feature.get("collection"),
                            external_item_id=feature["id"],
                            datetime=datetime.fromisoformat(props["datetime"].replace("Z", "+00:00")),
                            geometry=feature.get("geometry", {}),
                            bbox=feature.get("bbox"),
                            sensor_type=props.get("instrument_type"),
                            processing_level=props.get("processing:level"),
                            cloud_cover=props.get("eo:cloud_cover"),
                            assets=feature.get("assets", {}),
                            provider_metadata=props,
                        )
                    )
                return candidates
            else:
                logger.warning("CDSE search failed", extra={"status": response.status_code})
                return []

        except Exception:
            logger.exception("Error searching CDSE")
            return []

    async def get_item(self, external_item_id: str) -> Optional[ExternalObservationCandidate]:
        """Get a specific item."""
        try:
            client = await self._get_client()
            response = await client.get(f"{self._stac_url}/collections/*/items/{external_item_id}", timeout=10.0)
            if response.status_code == 200:
                feature = response.json()
                props = feature.get("properties", {})
                return ExternalObservationCandidate(
                    provider=self._provider.code,
                    external_item_id=feature["id"],
                    datetime=datetime.fromisoformat(props["datetime"].replace("Z", "+00:00")),
                    geometry=feature.get("geometry", {}),
                    bbox=feature.get("bbox"),
                    assets=feature.get("assets", {}),
                )
            return None
        except Exception:
            logger.exception("Error getting CDSE item", extra={"item_id": external_item_id})
            return None

    async def get_asset_metadata(
        self, external_item_id: str, asset_key: str
    ) -> Optional[dict[str, Any]]:
        """Get asset metadata."""
        item = await self.get_item(external_item_id)
        if item and asset_key in item.assets:
            return item.assets[asset_key]
        return None

    async def get_download_options(
        self, external_item_id: str
    ) -> list[dict[str, Any]]:
        """Get download options for an item."""
        item = await self.get_item(external_item_id)
        if not item:
            return []

        options = []
        for key, asset in item.assets.items():
            if "href" in asset:
                options.append({
                    "asset_key": key,
                    "url": asset["href"],
                    "type": asset.get("type"),
                    "size": asset.get("size"),
                })
        return options

    async def health_check(self) -> ProviderHealthStatus:
        """Check CDSE health."""
        try:
            client = await self._get_client()
            response = await client.get(f"{self._stac_url}/", timeout=5.0)
            if response.status_code == 200:
                self._health = ProviderHealthStatus.AVAILABLE
                return ProviderHealthStatus.AVAILABLE
            else:
                self._health = ProviderHealthStatus.DEGRADED
                return ProviderHealthStatus.DEGRADED
        except Exception:
            self._health = ProviderHealthStatus.UNAVAILABLE
            return ProviderHealthStatus.UNAVAILABLE

    async def get_capabilities(self) -> list[ProviderCapability]:
        """Get CDSE capabilities."""
        return [
            ProviderCapability.STAC,
            ProviderCapability.ODATA,
            ProviderCapability.CATALOG_SEARCH,
            ProviderCapability.DOWNLOAD,
            ProviderCapability.S3,
            ProviderCapability.OPENEO,
        ]

    async def close(self) -> None:
        """Close HTTP client."""
        if self._http_client and not self._http_client.is_closed:
            await self._http_client.aclose()
