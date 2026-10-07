"""Unit tests for storage client."""

from packages.storage.client import StorageClient


def test_sha256_computation():
    """Test SHA-256 checksum computation."""
    data = b"hello world"
    sha256 = StorageClient.compute_sha256(data)
    assert len(sha256) == 64
    assert sha256 == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"


def test_sha256_empty():
    """Test SHA-256 of empty data."""
    sha256 = StorageClient.compute_sha256(b"")
    assert len(sha256) == 64
    assert sha256 == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def test_is_raw_key():
    """Test raw key detection."""
    assert StorageClient._is_raw_key("raw/obs1.tif") is True
    assert StorageClient._is_raw_key("data/raw/obs1.tif") is True
    assert StorageClient._is_raw_key("processed/obs1.tif") is False
    assert StorageClient._is_raw_key("derived/output.tif") is False
