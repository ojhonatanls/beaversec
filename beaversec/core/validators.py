"""Input validators for BeaverSec."""

import re
from typing import Any, Dict, List, Optional, Union
from ipaddress import ip_address, IPv4Address, IPv6Address

from beaversec.core.exceptions import ValidationError


class InputValidator:
    """
    Centralized input validation for all BeaverSec components.

    Provides methods for validating various data types and formats.
    """

    @staticmethod
    def validate_ip(ip: str) -> bool:
        """
        Validate IP address format.

        Args:
            ip: IP address string

        Returns:
            bool: True if valid

        Raises:
            ValidationError: If IP is invalid
        """
        try:
            ip_address(ip)
            return True
        except ValueError:
            raise ValidationError(f"Invalid IP address: {ip}")

    @staticmethod
    def validate_domain(domain: str) -> bool:
        """
        Validate domain name format.

        Args:
            domain: Domain name string

        Returns:
            bool: True if valid

        Raises:
            ValidationError: If domain is invalid
        """
        if not domain or len(domain) > 253:
            raise ValidationError(f"Invalid domain length: {domain}")

        domain_pattern = re.compile(
            r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        )

        if not domain_pattern.match(domain):
            raise ValidationError(f"Invalid domain format: {domain}")

        return True

    @staticmethod
    def validate_port(port: int) -> bool:
        """
        Validate port number.

        Args:
            port: Port number

        Returns:
            bool: True if valid

        Raises:
            ValidationError: If port is invalid
        """
        if not isinstance(port, int) or port < 1 or port > 65535:
            raise ValidationError(f"Invalid port number: {port}")

        return True

    @staticmethod
    def validate_ports(ports: Union[str, List[str], List[int]]) -> List[int]:
        """
        Validate and parse port specifications.

        Args:
            ports: Port specification (string, list, or comma-separated)

        Returns:
            List[int]: List of valid port numbers

        Raises:
            ValidationError: If ports are invalid
        """
        if isinstance(ports, str):
            if "," in ports:
                ports = [p.strip() for p in ports.split(",")]
            else:
                ports = [ports.strip()]

        valid_ports = []

        for port in ports:
            try:
                port_num = int(port)
                InputValidator.validate_port(port_num)
                valid_ports.append(port_num)
            except ValueError:
                raise ValidationError(f"Invalid port value: {port}")

        if len(valid_ports) == 0:
            raise ValidationError("No valid ports provided")

        if len(valid_ports) > 100:
            raise ValidationError("Too many ports specified (max 100)")

        return valid_ports

    @staticmethod
    def validate_output_format(format_str: str) -> bool:
        """
        Validate output format.

        Args:
            format_str: Format string

        Returns:
            bool: True if valid

        Raises:
            ValidationError: If format is invalid
        """
        valid_formats = {"json", "html", "csv", "yaml", "xml"}

        if format_str.lower() not in valid_formats:
            raise ValidationError(f"Invalid output format: {format_str}")

        return True

    @staticmethod
    def validate_parameter_value(key: str, value: Any) -> bool:
        """
        Validate a parameter value based on its key.

        Args:
            key: Parameter key
            value: Parameter value

        Returns:
            bool: True if valid

        Raises:
            ValidationError: If parameter is invalid
        """
        if value is None:
            raise ValidationError(f"Parameter '{key}' cannot be None")

        if key == "target":
            return InputValidator._validate_target(value)

        if key in ["port", "ports"]:
            return InputValidator.validate_port(int(value))

        return True

    @staticmethod
    def _validate_target(target: str) -> bool:
        """Validate target (IP or domain)."""
        if not target:
            raise ValidationError("Target cannot be empty")

        # Try IP validation
        try:
            return InputValidator.validate_ip(target)
        except ValidationError:
            pass

        # Try domain validation
        try:
            return InputValidator.validate_domain(target)
        except ValidationError:
            pass

        raise ValidationError(f"Invalid target format: {target}")

    @staticmethod
    def validate_params(params: Dict[str, Any], required: List[str]) -> Dict[str, Any]:
        """
        Validate a dictionary of parameters.

        Args:
            params: Parameters dictionary
            required: List of required parameter keys

        Returns:
            Dict[str, Any]: Validated parameters

        Raises:
            ValidationError: If parameters are invalid
        """
        validated = {}

        # Check required parameters
        for key in required:
            if key not in params or params[key] is None:
                raise ValidationError(f"Required parameter missing: {key}")
            validated[key] = params[key]

        # Validate optional parameters
        for key, value in params.items():
            if key not in validated:
                try:
                    InputValidator.validate_parameter_value(key, value)
                    validated[key] = value
                except ValidationError:
                    raise ValidationError(f"Invalid parameter: {key}={value}")

        return validated