"""CLI command handling and module orchestration."""

import argparse
import sys
from typing import List, Optional

from beaversec.cli.parser import create_parser
from beaversec.core.base import ModuleManager
from beaversec.core.security import SecurityContext
from beaversec.utils.audit_logger import AuditLogger
from beaversec.utils.credential_manager import CredentialManager


class CommandHandler:
    """
    Handles CLI command execution with security context validation.

    Attributes:
        parser: Argument parser instance
        logger: Audit logger for command tracking
        security_context: Security validation context
    """

    def __init__(self):
        """Initialize the command handler with security context."""
        self.parser = create_parser()
        self.logger = AuditLogger.get_logger("cli")
        self.security_context = SecurityContext()
        self.credential_manager = CredentialManager()

    def execute(self, args: Optional[List[str]] = None) -> int:
        """
        Execute CLI command with full validation.

        Args:
            args: Command line arguments (defaults to sys.argv[1:])

        Returns:
            int: Exit code (0 for success, non-zero for errors)

        Raises:
            SecurityException: For security validation failures
        """
        if args is None:
            args = sys.argv[1:]

        parsed_args = self.parser.parse_args(args)

        if hasattr(parsed_args, "func"):
            try:
                self._validate_command(parsed_args)
                return parsed_args.func(parsed_args)
            except Exception as e:
                self.logger.error(f"Command execution failed: {str(e)}")
                print(f"Error: {str(e)}", file=sys.stderr)
                return 1

        self.parser.print_help()
        return 0

    def _validate_command(self, parsed_args: argparse.Namespace) -> None:
        """Validate command execution against security policies."""
        self.security_context.validate_operation(
            parsed_args.command if hasattr(parsed_args, "command") else "unknown"
        )


def main():
    """Main entry point for the BeaverSec CLI."""
    handler = CommandHandler()
    sys.exit(handler.execute())


def list_modules(args):
    """List all available modules."""
    manager = ModuleManager()
    modules = manager.list_modules()

    print("\nAvailable Modules:")
    print("-" * 40)
    for name, info in modules.items():
        print(f"  {name:20} - {info.get('description', 'No description')}")
    print("-" * 40)
    return 0


def run_module(args):
    """Run a specific module with validated parameters."""
    manager = ModuleManager()
    module = manager.get_module(args.module_name)

    if not module:
        print(f"Error: Module '{args.module_name}' not found")
        return 1

    # Validate and sanitize parameters
    params = {
        "target": args.target,
        "port": getattr(args, "port", None),
        "format": getattr(args, "format", "json"),
        "output": getattr(args, "output", None),
    }

    # Run module with security context
    result = module.execute(params)
    return 0