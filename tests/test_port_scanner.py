"""
Tests for the port_scanner module.
"""
import pytest
from unittest.mock import patch, AsyncMock

from beaversec.modules.port_scanner import PortScannerModule


@pytest.mark.asyncio
async def test_port_scanner_success():
    """Test port_scanner with valid target and ports."""
    module = PortScannerModule()
    result = await module.run(target="127.0.0.1", ports=[22, 80, 443])
    
    assert result.module == "port_scanner"
    assert result.target == "127.0.0.1"
    assert result.success is True
    assert "open_ports" in result.data
    assert len(result.data["open_ports"]) == 3
    assert result.data["total_scanned"] == 3


@pytest.mark.asyncio
async def test_port_scanner_with_common_ports():
    """Test port_scanner with common ports (22, 80, 443 should be open)."""
    module = PortScannerModule()
    result = await module.run(target="127.0.0.1", ports=[22, 80, 443])
    
    open_ports = result.data["open_ports"]
    port_numbers = [p["port"] for p in open_ports]
    
    assert 22 in port_numbers
    assert 80 in port_numbers
    assert 443 in port_numbers


@pytest.mark.asyncio
async def test_port_scanner_empty_ports():
    """Test port_scanner with empty ports list."""
    module = PortScannerModule()
    result = await module.run(target="127.0.0.1", ports=[])
    
    assert result.data["open_ports"] == []
    assert result.data["total_scanned"] == 0