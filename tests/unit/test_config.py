"""Unit tests for core configuration."""

import pytest
from packages.core.config import Settings


def test_settings_default_values():
    """Test settings load with defaults."""
    settings = Settings()
    assert settings.environment == "development"
    assert settings.log_level == "INFO"
    assert settings.api_port == 8000


def test_settings_invalid_log_level():
    """Test invalid log level raises error."""
    with pytest.raises(ValueError, match="Invalid log level"):
        Settings(log_level="INVALID")


def test_settings_invalid_environment():
    """Test invalid environment raises error."""
    with pytest.raises(ValueError, match="Invalid environment"):
        Settings(environment="invalid")


def test_settings_valid_log_levels():
    """Test all valid log levels."""
    for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        settings = Settings(log_level=level)
        assert settings.log_level == level


def test_settings_broker_list():
    """Test broker list parsing."""
    settings = Settings(event_bus_brokers="host1:9092,host2:9092")
    brokers = settings.get_broker_list()
    assert len(brokers) == 2
    assert brokers[0] == "host1:9092"
    assert brokers[1] == "host2:9092"
