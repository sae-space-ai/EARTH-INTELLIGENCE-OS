"""STAC Item mapping from Observation domain model."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from packages.contracts.domain import Observation


def observation_to_stac_item(
    observation: Observation,
    platform_name: str,
    instrument_name: str,
    raw_asset_href: str,
    processed_asset_href: str | None = None,
) -> dict[str, Any]:
    """Map Observation domain model to STAC Item representation.

    Args:
        observation: Source observation entity.
        platform_name: Satellite/platform name.
        instrument_name: Sensor/instrument name.
        raw_asset_href: URL/href for raw asset.
        processed_asset_href: Optional URL for processed asset.

    Returns:
        STAC Item dictionary compliant with STAC spec 1.0.0.
    """
    item: dict[str, Any] = {
        "type": "Feature",
        "stac_version": "1.0.0",
        "id": str(observation.id),
        "geometry": observation.footprint,
        "bbox": observation.bbox,
        "properties": {
            "datetime": observation.acquired_at.isoformat(),
            "platform": platform_name,
            "instruments": [instrument_name],
            "processing:level": observation.processing_level,
            "eo:cloud_cover": None,
            "view:off_nadir": None,
            "earth-intelligence:quality_score": observation.quality_score,
            "earth-intelligence:knowledge_state": observation.knowledge_state.value,
        },
        "links": [
            {"rel": "self", "href": f"/api/v1/observations/{observation.id}/stac"},
            {"rel": "root", "href": "/stac"},
            {"rel": "parent", "href": "/stac/collections/observations"},
            {"rel": "collection", "href": "/stac/collections/observations"},
        ],
        "assets": {
            "raw": {
                "href": raw_asset_href,
                "type": "application/octet-stream",
                "roles": ["data"],
                "title": "Raw observation data",
            },
        },
        "collection": "observations",
    }

    if processed_asset_href:
        item["assets"]["processed"] = {
            "href": processed_asset_href,
            "type": "application/octet-stream",
            "roles": ["data", "processed"],
            "title": "Processed observation data",
        }

    return item
