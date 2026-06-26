markdown

# BeaverSec - Segurança Ofensiva Modular (v4.0)

## Visão Geral

BeaverSec é um framework de segurança ofensiva modular projetado para reconhecimento, enumeração e análise de vulnerabilidades. A v4.0 representa uma reformulação completa com foco em segurança, performance e arquitetura robusta.

### Principais Características

- **Arquitetura Modular**: Sistema baseado em plugins com descoberta automática de módulos
- **Segurança em Primeiro Lugar**: Sanitização de entradas, logging auditável e validação rigorosa
- **Alta Performance**: Processamento assíncrono, rate limiting e connection pooling
- **Multiplataforma**: Suporte nativo para Windows, Linux e macOS
- **Zero Dependências Externas**: Utiliza apenas bibliotecas padrão do Python
- **Logging Estruturado**: Auditoria completa com logs em JSON e formato padrão

---

## Módulos Disponíveis (16)

| Módulo | Descrição |
|--------|-----------|
| `ping_sweep` | Varredura ICMP e ARP para descoberta de hosts |
| `port_scanner` | Escaneamento TCP com detecção de serviços |
| `syn_scan` | SYN stealth scan para varredura sigilosa |
| `udp_scan` | Escaneamento UDP para serviços baseados em UDP |
| `dns_enum` | Enumeração de registros DNS (A, AAAA, MX, NS, TXT, etc.) |
| `dns_zone_transfer` | Teste de transferência de zona DNS |
| `subdomain_brute` | Força bruta de subdomínios com wordlist |
| `ssl_scan` | Análise de certificados SSL/TLS |
| `ssl_cipher_scan` | Enumeração de cifras SSL/TLS suportadas |
| `http_headers` | Análise de cabeçalhos HTTP de segurança |
| `whois_lookup` | Consulta WHOIS para domínios e IPs |
| `shodan_enum` | Enriquecimento de dados via Shodan API |
| `vuln_scanner` | Scanner de vulnerabilidades via NVD API |
| `service_detection` | Detecção de serviços via banner grabbing |
| `os_detection` | Fingerprinting de sistema operacional |
| `snmp_enum` | Enumeração SNMP com comunidades padrão |

---

## Início Rápido

### 1. Instalação

**Linux/macOS:**
```bash
./scripts/install.sh