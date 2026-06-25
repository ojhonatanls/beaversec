"""Network utilities for BeaverSec."""

import socket
import ipaddress
from typing import List, Optional, Tuple

from beaversec.core.exceptions import NetworkError
from beaversec.utils.audit_logger import AuditLogger


class NetworkUtils:
    """
    Network utility functions for host and port operations.

    Provides safe network operations with error handling.
    """

    @staticmethod
    def resolve_host(hostname: str) -> List[str]:
        """
        Resolve hostname to IP addresses.

        Args:
            hostname: Hostname to resolve

        Returns:
            List[str]: List of IP addresses

        Raises:
            NetworkError: If resolution fails
        """
        try:
            addrinfo = socket.getaddrinfo(hostname, None, 0, 0, socket.IPPROTO_TCP)
            ips = list(set([addr[4][0] for addr in addrinfo]))
            return ips
        except socket.gaierror as e:
            raise NetworkError(f"Failed to resolve hostname {hostname}: {e}")

    @staticmethod
    def is_port_open(host: str, port: int, timeout: float = 2.0) -> bool:
        """
        Check if a port is open on a host.

        Args:
            host: Target host
            port: Port number
            timeout: Connection timeout in seconds

        Returns:
            bool: True if port is open, False otherwise
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False

    @staticmethod
    def get_local_ip() -> Optional[str]:
        """
        Get local machine IP address.

        Returns:
            Optional[str]: Local IP address or None if unable to determine
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            ip = sock.getsockname()[0]
            sock.close()
            return ip
        except Exception:
            return None

    @staticmethod
    def is_valid_network(network: str) -> bool:
        """
        Validate a network CIDR notation.

        Args:
            network: Network in CIDR notation

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            ipaddress.ip_network(network, strict=False)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_network_hosts(network: str) -> List[str]:
        """
        Get all hosts in a network.

        Args:
            network: Network in CIDR notation

        Returns:
            List[str]: List of IP addresses in the network

        Raises:
            NetworkError: If network is invalid
        """
        try:
            net = ipaddress.ip_network(network, strict=False)
            return [str(ip) for ip in net.hosts()]
        except ValueError as e:
            raise NetworkError(f"Invalid network {network}: {e}")

    @staticmethod
    def validate_ip(ip: str) -> bool:
        """
        Validate an IP address.

        Args:
            ip: IP address string

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False