"""Input sanitization for BeaverSec."""

import re
import html
from typing import Any, Dict, List, Optional, Union


class Sanitizer:
    """
    Comprehensive input sanitization for all data types.

    Provides methods to safely sanitize various data formats
    to prevent injection and XSS attacks.
    """

    @staticmethod
    def sanitize_string(value: str) -> str:
        """
        Sanitize a string value.

        Args:
            value: String to sanitize

        Returns:
            str: Sanitized string
        """
        if not value:
            return ""

        # Remove control characters
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', value)

        # HTML escape
        sanitized = html.escape(sanitized)

        # Remove dangerous patterns
        dangerous_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'<.*?/>',
            r'<.*?>',
        ]

        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)

        return sanitized

    @staticmethod
    def sanitize_path(path: str) -> str:
        """
        Sanitize a file path.

        Args:
            path: Path to sanitize

        Returns:
            str: Sanitized path
        """
        if not path:
            return ""

        # Remove path traversal
        sanitized = path.replace("..", "")

        # Replace dangerous characters
        dangerous_chars = "<>|&;`$"
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, "")

        # Normalize path
        sanitized = sanitized.replace("\\", "/").strip()

        return sanitized

    @staticmethod
    def sanitize_params(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize all parameters in a dictionary.

        Args:
            params: Parameters to sanitize

        Returns:
            Dict[str, Any]: Sanitized parameters
        """
        sanitized = {}

        for key, value in params.items():
            if isinstance(value, str):
                sanitized[key] = Sanitizer.sanitize_string(value)
            elif isinstance(value, dict):
                sanitized[key] = Sanitizer.sanitize_params(value)
            elif isinstance(value, list):
                sanitized[key] = Sanitizer.sanitize_list(value)
            else:
                sanitized[key] = value

        return sanitized

    @staticmethod
    def sanitize_list(values: List[Any]) -> List[Any]:
        """
        Sanitize all values in a list.

        Args:
            values: List to sanitize

        Returns:
            List[Any]: Sanitized list
        """
        sanitized = []

        for value in values:
            if isinstance(value, str):
                sanitized.append(Sanitizer.sanitize_string(value))
            elif isinstance(value, dict):
                sanitized.append(Sanitizer.sanitize_params(value))
            elif isinstance(value, list):
                sanitized.append(Sanitizer.sanitize_list(value))
            else:
                sanitized.append(value)

        return sanitized

    @staticmethod
    def sanitize_command(command: str) -> str:
        """
        Sanitize a command string to prevent command injection.

        Args:
            command: Command to sanitize

        Returns:
            str: Sanitized command
        """
        if not command:
            return ""

        # Remove shell metacharacters
        shell_metachars = "|;&<>$`'\""
        for char in shell_metachars:
            command = command.replace(char, "")

        # Remove command injection patterns
        injection_patterns = [
            r'\$\{.*?\}',
            r'`.*?`',
            r'\$\(.*?\)',
        ]

        for pattern in injection_patterns:
            command = re.sub(pattern, '', command)

        return command.strip()

    @staticmethod
    def sanitize_for_shell(command_args: List[str]) -> List[str]:
        """
        Sanitize command arguments for shell execution.

        Args:
            command_args: List of command arguments

        Returns:
            List[str]: Sanitized arguments
        """
        sanitized = []

        for arg in command_args:
            # Quote arguments if they contain spaces
            arg = arg.replace('"', '\\"')
            if ' ' in arg and not arg.startswith('"'):
                arg = f'"{arg}"'
            sanitized.append(arg)

        return sanitized

    @staticmethod
    def sanitize_for_json(value: Any) -> Any:
        """
        Sanitize value for JSON serialization.

        Args:
            value: Value to sanitize

        Returns:
            Any: Sanitized value
        """
        if isinstance(value, str):
            return value.encode('unicode_escape').decode('ascii')
        if isinstance(value, dict):
            return {k: Sanitizer.sanitize_for_json(v) for k, v in value.items()}
        if isinstance(value, list):
            return [Sanitizer.sanitize_for_json(v) for v in value]
        return value