"""Typed application settings using pydantic-settings."""

from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # General
    environment: str = Field(default="development", description="Runtime environment")
    log_level: str = Field(default="INFO", description="Logging level")

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/earth_intelligence",
        description="Async PostgreSQL connection URL",
    )

    # Object Storage
    object_storage_endpoint: str = Field(
        default="http://localhost:9000",
        description="S3-compatible endpoint URL",
    )
    object_storage_bucket: str = Field(
        default="earth-observations",
        description="Default storage bucket",
    )
    object_storage_access_key: str = Field(
        default="minioadmin",
        description="S3 access key",
    )
    object_storage_secret_key: str = Field(
        default="minioadmin",
        description="S3 secret key",
    )

    # Event Bus
    event_bus_brokers: str = Field(
        default="localhost:9092",
        description="Comma-separated Kafka/Redpanda broker addresses",
    )

    # API
    api_host: str = Field(default="0.0.0.0", description="API bind host")
    api_port: int = Field(default=8000, ge=1, le=65535, description="API bind port")

    # Observability
    otel_exporter_otlp_endpoint: Optional[str] = Field(
        default=None,
        description="OpenTelemetry OTLP exporter endpoint",
    )

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Ensure log level is valid."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        upper = v.upper()
        if upper not in valid_levels:
            raise ValueError(f"Invalid log level: {v}. Must be one of {valid_levels}")
        return upper

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Ensure environment is valid."""
        valid_envs = {"development", "staging", "production", "test"}
        lower = v.lower()
        if lower not in valid_envs:
            raise ValueError(f"Invalid environment: {v}. Must be one of {valid_envs}")
        return lower

    def get_broker_list(self) -> list[str]:
        """Parse broker string into list."""
        return [b.strip() for b in self.event_bus_brokers.split(",") if b.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings singleton."""
    return Settings()
