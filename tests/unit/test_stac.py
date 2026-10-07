"""Unit tests for STAC mapping."""

from datetime import datetime
from uuid import uuid4

from packages.contracts.domain import Observation, KnowledgeState
from packages.geospatial.stac import observation_to_stac_item


def test_observation_to_stac_item():
    """Test Observation → STAC Item mapping."""
    obs = Observation(
        satellite_id=uuid4(),
        sensor_id=uuid4(),
        acquired_at=datetime(2024, 1, 15, 12, 0, 0),
        footprint={"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]},
        bbox=[0.0, 0.0, 1.0, 1.0],
        processing_level="L1B",
        quality_score=0.95,
        raw_asset_id=uuid4(),
    )

    item = observation_to_stac_item(
        observation=obs,
        platform_name="TestSat-1",
        instrument_name="SAR-X",
        raw_asset_href="s3://bucket/raw/obs1.tif",
    )

    assert item["type"] == "Feature"
    assert item["stac_version"] == "1.0.0"
    assert item["id"] == str(obs.id)
    assert item["geometry"] == obs.footprint
    assert item["bbox"] == obs.bbox
    assert item["properties"]["datetime"] == "2024-01-15T12:00:00"
    assert item["properties"]["platform"] == "TestSat-1"
    assert item["properties"]["instruments"] == ["SAR-X"]
    assert item["properties"]["processing:level"] == "L1B"
    assert item["properties"]["earth-intelligence:quality_score"] == 0.95
    assert item["properties"]["earth-intelligence:knowledge_state"] == "OBSERVED"
    assert "raw" in item["assets"]
    assert item["assets"]["raw"]["href"] == "s3://bucket/raw/obs1.tif"


def test_stac_item_with_processed_asset():
    """Test STAC item includes processed asset when available."""
    obs = Observation(
        satellite_id=uuid4(),
        sensor_id=uuid4(),
        acquired_at=datetime.utcnow(),
        footprint={"type": "Point", "coordinates": [0, 0]},
        bbox=[0, 0, 0, 0],
        processing_level="L2",
        raw_asset_id=uuid4(),
        processed_asset_id=uuid4(),
    )

    item = observation_to_stac_item(
        observation=obs,
        platform_name="Sat",
        instrument_name="Sensor",
        raw_asset_href="s3://raw/data.tif",
        processed_asset_href="s3://processed/data.tif",
    )

    assert "processed" in item["assets"]
    assert item["assets"]["processed"]["href"] == "s3://processed/data.tif"
