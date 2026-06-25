"""Command line argument parser configuration."""

import argparse
from typing import argparse


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the command line argument parser.

    Returns:
        argparse.ArgumentParser: Configured parser instance
    """
    parser = argparse.ArgumentParser(
        prog="beaversec",
        description="BeaverSec - Modular Offensive Security Framework",
        epilog="For more information, visit: https://github.com/ojhonatanls/BeaverSec",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List command
    list_parser = subparsers.add_parser("list", help="List available modules")
    list_parser.set_defaults(func=cli_commands.list_modules)

    # Run command
    run_parser = subparsers.add_parser("run", help="Run a specific module")
    run_parser.add_argument("module_name", help="Name of the module to run")
    run_parser.add_argument("target", help="Target IP or domain")
    run_parser.add_argument("-p", "--port", help="Ports to scan (comma-separated)")
    run_parser.add_argument("-o", "--output", help="Output file path")
    run_parser.add_argument("--format", default="json", choices=["json", "html", "csv"],
                           help="Output format")
    run_parser.set_defaults(func=cli_commands.run_module)

    return parser


# Lazy import to avoid circular dependencies
import beaversec.cli.commands as cli_commands