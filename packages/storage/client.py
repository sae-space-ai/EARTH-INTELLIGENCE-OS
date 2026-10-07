"""S3-compatible storage client with checksum verification."""

from __future__ import annotations

import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from uuid import UUID, uuid4

import boto3
from botocore.config import Config as BotoConfig
from pydantic import BaseModel, Field

from packages.core.config import get_settings
from packages.core.logging import get_logger

logger = get_logger(__name__)


class AssetMetadata(BaseModel):
    """Metadata for a stored asset."""

    id: UUID = Field(default_factory=uuid4)
    bucket: str
    key: str
    size: int = Field(ge=0)
    content_type: str
    sha256: str = Field(min_length=64, max_length=64)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class StorageClient:
    """S3-compatible object storage client.

    Provides upload, download, existence check, and metadata retrieval
    with SHA-256 checksum verification.
    """

    def __init__(
        self,
        endpoint_url: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
    ) -> None:
        """Initialize storage client with configuration."""
        settings = get_settings()
        self._endpoint = endpoint_url or settings.object_storage_endpoint
        self._access_key = access_key or settings.object_storage_access_key
        self._secret_key = secret_key or settings.object_storage_secret_key
        self._default_bucket = settings.object_storage_bucket

        self._client = boto3.client(
            "s3",
            endpoint_url=self._endpoint,
            aws_access_key_id=self._access_key,
            aws_secret_access_key=self._secret_key,
            config=BotoConfig(signature_version="s3v4"),
        )

    @staticmethod
    def compute_sha256(data: bytes) -> str:
        """Compute SHA-256 checksum of data."""
        return hashlib.sha256(data).hexdigest()

    def put_bytes(
        self,
        data: bytes,
        key: str,
        bucket: Optional[str] = None,
        content_type: str = "application/octet-stream",
    ) -> AssetMetadata:
        """Upload bytes to object storage.

        Args:
            data: Raw bytes to store.
            key: Object key/path.
            bucket: Target bucket (defaults to configured bucket).
            content_type: MIME type of the content.

        Returns:
            AssetMetadata with checksum and size.

        Raises:
            ValueError: If raw key already exists with different checksum.
        """
        bucket = bucket or self._default_bucket
        sha256 = self.compute_sha256(data)

        # Immutability check for raw data
        if self._is_raw_key(key):
            if self.exists(key, bucket):
                existing = self.get_metadata(key, bucket)
                if existing.sha256 != sha256:
                    raise ValueError(
                        f"Raw asset immutability violation: key={key} exists with "
                        f"different checksum. Expected {existing.sha256}, got {sha256}"
                    )
                logger.info("Raw asset already exists with matching checksum", extra={"key": key})
                return existing

        self._client.put_object(
            Bucket=bucket,
            Key=key,
            Body=data,
            ContentType=content_type,
            Metadata={"sha256": sha256},
        )

        metadata = AssetMetadata(
            bucket=bucket,
            key=key,
            size=len(data),
            content_type=content_type,
            sha256=sha256,
        )

        logger.info(
            "Asset uploaded",
            extra={"bucket": bucket, "key": key, "size": len(data), "sha256": sha256},
        )
        return metadata

    def upload_file(
        self,
        file_path: str | Path,
        key: str,
        bucket: Optional[str] = None,
        content_type: str = "application/octet-stream",
    ) -> AssetMetadata:
        """Upload a file to object storage.

        Args:
            file_path: Local file path.
            key: Object key/path.
            bucket: Target bucket.
            content_type: MIME type.

        Returns:
            AssetMetadata.
        """
        path = Path(file_path)
        data = path.read_bytes()
        return self.put_bytes(data, key, bucket, content_type)

    def get_bytes(self, key: str, bucket: Optional[str] = None) -> bytes:
        """Download object as bytes.

        Args:
            key: Object key.
            bucket: Source bucket.

        Returns:
            Raw bytes.
        """
        bucket = bucket or self._default_bucket
        response = self._client.get_object(Bucket=bucket, Key=key)
        data = response["Body"].read()

        # Verify checksum
        stored_sha256 = response.get("Metadata", {}).get("sha256")
        if stored_sha256:
            computed = self.compute_sha256(data)
            if computed != stored_sha256:
                raise ValueError(
                    f"Checksum mismatch for {key}: expected {stored_sha256}, got {computed}"
                )

        return data

    def download_file(
        self, key: str, destination: str | Path, bucket: Optional[str] = None
    ) -> Path:
        """Download object to local file.

        Args:
            key: Object key.
            destination: Local file path.
            bucket: Source bucket.

        Returns:
            Path to downloaded file.
        """
        data = self.get_bytes(key, bucket)
        dest_path = Path(destination)
        dest_path.write_bytes(data)
        return dest_path

    def exists(self, key: str, bucket: Optional[str] = None) -> bool:
        """Check if object exists.

        Args:
            key: Object key.
            bucket: Target bucket.

        Returns:
            True if object exists.
        """
        bucket = bucket or self._default_bucket
        try:
            self._client.head_object(Bucket=bucket, Key=key)
            return True
        except self._client.exceptions.ClientError:
            return False

    def get_metadata(self, key: str, bucket: Optional[str] = None) -> AssetMetadata:
        """Get object metadata.

        Args:
            key: Object key.
            bucket: Target bucket.

        Returns:
            AssetMetadata.

        Raises:
            KeyError: If object does not exist.
        """
        bucket = bucket or self._default_bucket
        try:
            response = self._client.head_object(Bucket=bucket, Key=key)
            return AssetMetadata(
                bucket=bucket,
                key=key,
                size=response["ContentLength"],
                content_type=response.get("ContentType", "application/octet-stream"),
                sha256=response.get("Metadata", {}).get("sha256", ""),
            )
        except self._client.exceptions.ClientError as e:
            raise KeyError(f"Object not found: {bucket}/{key}") from e

    @staticmethod
    def _is_raw_key(key: str) -> bool:
        """Check if key represents raw/immutable data."""
        return key.startswith("raw/") or "/raw/" in key
