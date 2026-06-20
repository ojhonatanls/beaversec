# Changelog - BeaverSec

Todas as mudanças notáveis neste projeto serão documentadas aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

---

## [0.1.0] - 2026-06-20

### Adicionado
- Estrutura modular do projeto
- Sistema de logs com níveis (INFO, DEBUG, ERROR)
- Módulo `ping_sweep`: Descoberta de hosts ativos via ICMP
  - Suporte a IP único e rede CIDR (/24)
  - Multithreading para varreduras rápidas
- Módulo `port_scanner`: Scanner de portas TCP
  - 23 portas comuns mapeadas
  - Multithreading com até 50 threads simultâneas
- Módulo `meu_modulo`: Módulo de exemplo para demonstração
- Documentação inicial:
  - `README.md` com exemplos e guia rápido
  - `CONTRIBUTING.md` com guia para colaboradores
  - `CHANGELOG.md` com histórico de versões
  - `LICENSE` (MIT)

### Tecnologias
- Python 3.8+
- Bibliotecas padrão (ipaddress, subprocess, concurrent.futures, logging, argparse)

---

## [Próximas Versões]

### Planejado
- Módulo `subdomain_finder`: Coleta de subdomínios
- Módulo `dns_enum`: Enumeração DNS
- Módulo `http_headers`: Análise de cabeçalhos HTTP
- Sistema de relatórios em JSON/CSV
- Barra de progresso com tqdm
- Cores no terminal com colorama
- Testes unitários com pytest
- CI/CD com GitHub Actions
- Integração com APIs (Shodan, VirusTotal)
- Sistema de plugins
- Pacote no PyPI (`pip install beaversec`)