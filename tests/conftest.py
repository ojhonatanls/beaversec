"""
Pytest configuration and fixtures for BeaverSec tests.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_target():
    """Return a mock target IP."""
    return "127.0.0.1"


@pytest.fixture
def mock_ports():
    """Return a list of mock ports."""
    return [22, 80, 443]


@pytest.fixture
def mock_module_result():
    """Return a mock ModuleResult."""
    from beaversec.core.base_module import ModuleResult
    
    return ModuleResult(
        module="test_module",
        target="127.0.0.1",
        success=True,
        data={"test": "data"}
    )


@pytest.fixture
def mock_config():
    """Return a mock configuration dictionary."""
    return {
        "logging": {"level": "INFO", "format": "json"},
        "rate_limit": 500.0,
        "timeout": 5.0,
        "shodan": {"api_key": "test_key"},
        "nvd": {"api_key": "test_key"},
    }