"""
Tests for the BeaverSec CLI.
"""
import pytest
from click.testing import CliRunner

from beaversec.cli import cli


def test_cli_help():
    """Test the CLI help command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    
    assert result.exit_code == 0
    assert "BeaverSec" in result.output
    assert "--config" in result.output
    assert "--debug" in result.output


def test_cli_list():
    """Test the CLI list command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["list"])
    
    assert result.exit_code == 0
    assert "=== Available Modules ===" in result.output
    assert "ping_sweep" in result.output
    assert "port_scanner" in result.output


def test_cli_check():
    """Test the CLI check command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["check"])
    
    assert result.exit_code == 0
    assert "Checking BeaverSec configuration" in result.output


def test_cli_run_ping_sweep():
    """Test the CLI run command with ping_sweep."""
    runner = CliRunner()
    result = runner.invoke(cli, ["run", "ping_sweep", "192.168.1.1"])
    
    assert result.exit_code == 0
    assert "Running ping_sweep against 192.168.1.1" in result.output
    assert "ping_sweep completed successfully" in result.output


def test_cli_run_port_scanner():
    """Test the CLI run command with port_scanner."""
    runner = CliRunner()
    result = runner.invoke(cli, ["run", "port_scanner", "127.0.0.1", "-p", "22,80,443"])
    
    assert result.exit_code == 0
    assert "Running port_scanner against 127.0.0.1" in result.output
    assert "port_scanner completed successfully" in result.output


def test_cli_run_invalid_module():
    """Test the CLI run command with an invalid module."""
    runner = CliRunner()
    result = runner.invoke(cli, ["run", "invalid_module", "127.0.0.1"])
    
    assert result.exit_code == 1
    assert "Module 'invalid_module' not found" in result.output


def test_cli_run_no_target():
    """Test the CLI run command without a target."""
    runner = CliRunner()
    result = runner.invoke(cli, ["run", "ping_sweep"])
    
    assert result.exit_code == 2  # Click error for missing argument