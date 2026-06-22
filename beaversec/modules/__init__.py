"""
Módulos do BeaverSec.
"""
from beaversec.modules.dns_enum import DNSEnum
from beaversec.modules.http_headers import HTTPHeaders
from beaversec.modules.ping_sweep import PingSweep
from beaversec.modules.port_scanner import PortScanner
from beaversec.modules.ssl_scan import SSLScan
from beaversec.modules.subdomain_brute import SubdomainBrute
from beaversec.modules.traceroute import Traceroute
from beaversec.modules.whois_lookup import WhoisLookup

MODULES = {
    "ping-sweep": "Varredura ICMP para hosts ativos",
    "port-scanner": "Escaneamento de portas TCP",
    "dns-enum": "Enumeração de registros DNS",
    "ssl-scan": "Análise de certificados SSL/TLS",
    "http-headers": "Análise de cabeçalhos HTTP de segurança",
    "subdomain-brute": "Força bruta para subdomínios",
    "traceroute": "Rastreamento de rota até o alvo",
    "whois": "Consulta WHOIS de domínios",
}

__all__ = [
    "DNSEnum",
    "HTTPHeaders",
    "PingSweep",
    "PortScanner",
    "SSLScan",
    "SubdomainBrute",
    "Traceroute",
    "WhoisLookup",
    "MODULES",
]
