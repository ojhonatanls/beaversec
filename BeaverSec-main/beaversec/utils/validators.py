"""
Validação e sanitização de entradas.
"""
import re
from ipaddress import ip_address, ip_network

IP_REGEX = re.compile(
    r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
)
DOMAIN_REGEX = re.compile(
    r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.([A-Za-z]{2,}|[A-Za-z]{2,}\.[A-Za-z]{2,})$"
)


def is_valid_ip(ip: str) -> bool:
    try:
        ip_address(ip)
        return True
    except ValueError:
        return False


def is_valid_domain(domain: str) -> bool:
    return bool(DOMAIN_REGEX.match(domain))


def sanitize_target(target: str) -> str:
    """Remove caracteres perigosos de um alvo."""
    # Remove espaços e caracteres de controle
    target = target.strip()
    # Permite apenas letras, números, pontos, hífens, dois pontos, barras
    if not re.match(r"^[a-zA-Z0-9.:/-]+$", target):
        raise ValueError("Alvo contém caracteres inválidos")
    return target
