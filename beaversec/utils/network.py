"""
Funções auxiliares de rede.
"""
import socket
from ipaddress import ip_address


def resolve_host(host: str, timeout: float = 5.0) -> str:
    """Resolve um hostname para IP."""
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        raise ValueError(f"Não foi possível resolver {host}")


def is_port_open(ip: str, port: int, timeout: float = 2.0) -> bool:
    """Verifica se uma porta TCP está aberta."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except Exception:
        return False
