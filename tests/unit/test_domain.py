"""Unit tests for domain models."""

import pytest
from datetime import datetime
from uuid import uuid4

from packages.contracts.domain import (
    KnowledgeState,
    SensorType,
    ModelVersionStatus,
    Satellite,
    Sensor,
    Observation,
    EarthEvent,
    ModelVersion,
    ProvenanceRecord,
)


def test_knowledge_state_values():
    """Test KnowledgeState enum values."""
    assert KnowledgeState.OBSERVED.value == "OBSERVED"
    assert KnowledgeState.INFERRED.value == "INFERRED"
    assert KnowledgeState.FORECAST.value == "FORECAST"
    assert KnowledgeState.SIMULATED.value == "SIMULATED"


def test_sensor_type_values():
    """Test SensorType enum values."""
    assert SensorType.SAR.value == "SAR"
    assert SensorType.LIDAR.value == "LIDAR"
    assert SensorType.HYPERSPECTRAL.value == "HYPERSPECTRAL"
    assert SensorType.SUBSURFACE_RADAR.value == "SUBSURFACE_RADAR"
    assert SensorType.OTHER.value == "OTHER"


def test_satellite_creation():
    """Test Satellite model creation."""
    sat = Satellite(name="TestSat", platform_type="CUBESAT")
    assert sat.name == "TestSat"
    assert sat.status == "ACTIVE"
    assert sat.id is not None


def test_sensor_creation():
    """Test Sensor model creation."""
    sat_id = uuid4()
    sensor = Sensor(satellite_id=sat_id, sensor_type=SensorType.SAR, name="SAR-1")
    assert sensor.satellite_id == sat_id
    assert sensor.sensor_type == SensorType.SAR


def test_observation_bbox_validation():
    """Test observation bbox validation."""
    obs = Observation(
        satellite_id=uuid4(),
        sensor_id=uuid4(),
        acquired_at=datetime.utcnow(),
        footprint={"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]},
        bbox=[-10.0, -5.0, 10.0, 5.0],
        processing_level="L1",
        raw_asset_id=uuid4(),
    )
    assert obs.bbox == [-10.0, -5.0, 10.0, 5.0]


def test_observation_invalid_bbox():
    """Test observation rejects invalid bbox."""
    with pytest.raises(ValueError, match="South.*must be.*North"):
        Observation(
            satellite_id=uuid4(),
            sensor_id=uuid4(),
            acquired_at=datetime.utcnow(),
            footprint={"type": "Point", "coordinates": [0, 0]},
            bbox=[0, 10, 0, 5],  # south > north
            processing_level="L1",
            raw_asset_id=uuid4(),
        )


def test_observation_footprint_validation():
    """Test observation requires valid GeoJSON footprint."""
    with pytest.raises(ValueError, match="type"):
        Observation(
            satellite_id=uuid4(),
            sensor_id=uuid4(),
            acquired_at=datetime.utcnow(),
            footprint={"coordinates": [0, 0]},  # missing type
            bbox=[0, 0, 1, 1],
            processing_level="L1",
            raw_asset_id=uuid4(),
        )


def test_earth_event_confidence_range():
    """Test EarthEvent confidence must be 0-1."""
    with pytest.raises(ValueError):
        EarthEvent(
            event_type="flood",
            geometry={"type": "Point", "coordinates": [0, 0]},
            first_seen=datetime.utcnow(),
            last_seen=datetime.utcnow(),
            confidence=1.5,  # > 1
            priority=1,
            knowledge_state=KnowledgeState.INFERRED,
        )


def test_earth_event_priority_range():
    """Test EarthEvent priority must be 1-5."""
    with pytest.raises(ValueError):
        EarthEvent(
            event_type="flood",
            geometry={"type": "Point", "coordinates": [0, 0]},
            first_seen=datetime.utcnow(),
            last_seen=datetime.utcnow(),
            confidence=0.9,
            priority=6,  # > 5
            knowledge_state=KnowledgeState.INFERRED,
        )


def test_model_version_status():
    """Test ModelVersionStatus enum."""
    assert ModelVersionStatus.REGISTERED.value == "REGISTERED"
    assert ModelVersionStatus.DEPLOYED.value == "DEPLOYED"
    assert ModelVersionStatus.RETIRED.value == "RETIRED"


def test_provenance_record_validation():
    """Test ProvenanceRecord time validation."""
    now = datetime.utcnow()
    with pytest.raises(ValueError, match="finished_at.*started_at"):
        ProvenanceRecord(
            input_asset_ids=[uuid4()],
            output_asset_ids=[uuid4()],
            operation="calibrate",
            software_version="1.0.0",
            parameters_hash="abc123",
            started_at=now,
            finished_at=now.replace(hour=now.hour - 1),  # before started
            trace_id=uuid4(),
        )
