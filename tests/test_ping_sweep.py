"""
Tests for the ping_sweep module.
"""
import pytest
from unittest.mock import patch, AsyncMock

from beaversec.modules.ping_sweep import PingSweepModule


@pytest.mark.asyncio
async def test_ping_sweep_success():
    """Test ping_sweep with a valid target."""
    module = PingSweepModule()
    result = await module.run(target="192.168.1.1", timeout=2.0)
    
    assert result.module == "ping_sweep"
    assert result.target == "192.168.1.1"
    assert result.success is True
    assert "alive_hosts" in result.data
    assert len(result.data["alive_hosts"]) == 1
    assert result.data["alive_hosts"][0] == "192.168.1.1"


@pytest.mark.asyncio
async def test_ping_sweep_timeout():
    """Test ping_sweep with timeout parameter."""
    module = PingSweepModule()
    result = await module.run(target="192.168.1.1", timeout=5.0)
    
    assert result.data["timeout"] == 5.0


@pytest.mark.asyncio
async def test_ping_sweep_invalid_target():
    """Test ping_sweep with an invalid target (should still return result)."""
    module = PingSweepModule()
    result = await module.run(target="invalid-target")
    
    # A implementação atual retorna o target mesmo se inválido
    assert result.target == "invalid-target"
    assert result.success is True