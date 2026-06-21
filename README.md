<p align="center">
  <img src="assets/BeaverSec2.png" alt="BeaverSec Banner" width="100%">
</p>

# 🦫 BeaverSec - Canivete suíço para cibersegurança

BeaverSec é uma ferramenta modular de segurança cibernética com arquitetura extensível.

## 📋 Módulos Disponíveis

- 🖥️ **ping_sweep** - Verifica hosts ativos via ICMP
- 🔌 **port_scanner** - Escaneia portas TCP abertas
- 🌐 **dns_enum** - Enumera registros DNS
- 🔒 **ssl_scan** - Analisa certificados SSL/TLS
- 📋 **http_headers** - Analisa headers HTTP de segurança
- 🔍 **subdomain_brute** - Descobre subdomínios por brute force
- 🗺️ **traceroute** - Rastreia a rota até o alvo

##  Instalação

```bash
git clone https://github.com/ojhonatanls/BeaverSec.git
cd BeaverSec
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
