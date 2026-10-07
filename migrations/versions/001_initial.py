"""Initial migration — create all Phase 0 tables."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial schema."""
    # Enable extensions
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # Satellites
    op.create_table(
        "satellites",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("platform_type", sa.String(100), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, default="ACTIVE"),
        sa.Column("metadata", postgresql.JSONB, default={}),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Sensors
    op.create_table(
        "sensors",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("satellite_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("satellites.id"), nullable=False),
        sa.Column("sensor_type", sa.String(50), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, default="ACTIVE"),
        sa.Column("metadata", postgresql.JSONB, default={}),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_sensors_satellite_id", "sensors", ["satellite_id"])

    # Observation Assets
    op.create_table(
        "observation_assets",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("bucket", sa.String(255), nullable=False),
        sa.Column("key", sa.String(1024), nullable=False),
        sa.Column("size", sa.BigInteger, nullable=False),
        sa.Column("content_type", sa.String(255), nullable=False),
        sa.Column("sha256", sa.String(64), nullable=False),
        sa.Column("processing_level", sa.String(50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_observation_assets_sha256", "observation_assets", ["sha256"])

    # Observations
    op.create_table(
        "observations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("satellite_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("satellites.id"), nullable=False),
        sa.Column("sensor_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("sensors.id"), nullable=False),
        sa.Column("acquired_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("footprint", postgresql.JSONB, nullable=False),
        sa.Column("bbox", postgresql.ARRAY(sa.Float), nullable=False),
        sa.Column("processing_level", sa.String(50), nullable=False),
        sa.Column("quality_score", sa.Float),
        sa.Column("raw_asset_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("observation_assets.id")),
        sa.Column("processed_asset_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("observation_assets.id")),
        sa.Column("model_version_id", postgresql.UUID(as_uuid=True)),
        sa.Column("knowledge_state", sa.String(20), nullable=False, default="OBSERVED"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_observations_satellite_id", "observations", ["satellite_id"])
    op.create_index("ix_observations_sensor_id", "observations", ["sensor_id"])
    op.create_index("ix_observations_acquired_at", "observations", ["acquired_at"])

    # Earth Events
    op.create_table(
        "earth_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("event_type", sa.String(100), nullable=False),
        sa.Column("geometry", postgresql.JSONB, nullable=False),
        sa.Column("first_seen", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_seen", sa.DateTime(timezone=True), nullable=False),
        sa.Column("confidence", sa.Float, nullable=False),
        sa.Column("priority", sa.Integer, nullable=False),
        sa.Column("knowledge_state", sa.String(20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_earth_events_event_type", "earth_events", ["event_type"])

    # Mission Requests
    op.create_table(
        "mission_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("aoi", postgresql.JSONB, nullable=False),
        sa.Column("priority", sa.Integer, nullable=False),
        sa.Column("requested_by", sa.String(255), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, default="REQUESTED"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Model Versions
    op.create_table(
        "model_versions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("model_name", sa.String(255), nullable=False),
        sa.Column("semantic_version", sa.String(50), nullable=False),
        sa.Column("git_commit", sa.String(40), nullable=False),
        sa.Column("framework", sa.String(100), nullable=False),
        sa.Column("checkpoint_uri", sa.String(1024), nullable=False),
        sa.Column("checkpoint_sha256", sa.String(64), nullable=False),
        sa.Column("training_dataset_version_id", postgresql.UUID(as_uuid=True)),
        sa.Column("metrics", postgresql.JSONB, default={}),
        sa.Column("status", sa.String(20), nullable=False, default="REGISTERED"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Dataset Versions
    op.create_table(
        "dataset_versions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("version", sa.String(50), nullable=False),
        sa.Column("uri", sa.String(1024), nullable=False),
        sa.Column("sha256", sa.String(64), nullable=False),
        sa.Column("metadata", postgresql.JSONB, default={}),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Provenance Records
    op.create_table(
        "provenance_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("input_asset_ids", postgresql.ARRAY(postgresql.UUID(as_uuid=True)), nullable=False),
        sa.Column("output_asset_ids", postgresql.ARRAY(postgresql.UUID(as_uuid=True)), nullable=False),
        sa.Column("operation", sa.String(255), nullable=False),
        sa.Column("software_version", sa.String(100), nullable=False),
        sa.Column("model_version_id", postgresql.UUID(as_uuid=True)),
        sa.Column("parameters_hash", sa.String(128), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("trace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Audit Records
    op.create_table(
        "audit_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("actor_type", sa.String(50), nullable=False),
        sa.Column("actor_id", sa.String(255), nullable=False),
        sa.Column("action", sa.String(255), nullable=False),
        sa.Column("resource_type", sa.String(100), nullable=False),
        sa.Column("resource_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("trace_id", postgresql.UUID(as_uuid=True)),
        sa.Column("metadata", postgresql.JSONB, default={}),
    )
    op.create_index("ix_audit_records_actor_id", "audit_records", ["actor_id"])
    op.create_index("ix_audit_records_action", "audit_records", ["action"])

    # Outbox Events (Transactional Outbox)
    op.create_table(
        "outbox_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("event_type", sa.String(255), nullable=False),
        sa.Column("schema_version", sa.String(20), nullable=False, default="v1"),
        sa.Column("payload", postgresql.JSONB, nullable=False),
        sa.Column("trace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("correlation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, default="PENDING"),
        sa.Column("retry_count", sa.Integer, nullable=False, default=0),
        sa.Column("error_message", sa.Text),
        sa.Column("next_retry_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("delivered_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_outbox_events_status", "outbox_events", ["status"])
    op.create_index("ix_outbox_events_next_retry_at", "outbox_events", ["next_retry_at"])


def downgrade() -> None:
    """Drop all tables."""
    op.drop_table("outbox_events")
    op.drop_table("audit_records")
    op.drop_table("provenance_records")
    op.drop_table("dataset_versions")
    op.drop_table("model_versions")
    op.drop_table("mission_requests")
    op.drop_table("earth_events")
    op.drop_table("observations")
    op.drop_table("observation_assets")
    op.drop_table("sensors")
    op.drop_table("satellites")
