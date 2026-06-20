# 🦫 BeaverSec

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)
![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen)

**B.E.A.V.E.R.** - *Binary Enumeration & Advanced Vulnerability Exploitation Recon*

Canivete suíço modular para cibersegurança, construído em Python com foco em aprendizado prático, evolução contínua e colaboração open-source.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Começando](#-começando)
- [Como Usar](#-como-usar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Criando um Novo Módulo](#-criando-um-novo-módulo)
- [Roadmap](#-roadmap)
- [Como Contribuir](#-como-contribuir)
- [Licença](#-licença)
- [Contato](#-contato)

---

## 🎯 Sobre o Projeto

**BeaverSec** é uma ferramenta modular de cibersegurança criada para ser o "canivete suíço" do analista de segurança. Inspirado na filosofia Unix de "faça uma coisa e faça bem", cada módulo é uma ferramenta independente que pode ser executada separadamente.

### 🎓 Motivação

Projeto acadêmico desenvolvido no **1º semestre de TSI (Tecnologia em Sistemas para Internet) na UTFPR - Toledo**. O objetivo é aprender na prática os fundamentos de:
- Programação em Python
- Arquitetura de software
- Redes e protocolos
- Cibersegurança
- Desenvolvimento open-source

---

## ⚡ Funcionalidades

### Módulos Disponíveis

| Módulo | Descrição | Exemplo |
|--------|-----------|---------|
| `ping_sweep` | Descoberta de hosts ativos via ICMP | `python main.py ping_sweep 192.168.1.0/24` |
| `port_scanner` | Varredura de portas TCP comuns | `python main.py port_scanner scanme.nmap.org` |

### Características Técnicas

- ✅ **Modular**: Adicione novas ferramentas sem alterar o núcleo
- ✅ **Multi-threaded**: Varreduras rápidas com paralelismo
- ✅ **Cross-platform**: Funciona no Linux, Windows e macOS
- ✅ **Logging integrado**: Registro de atividades e erros
- ✅ **CLI amigável**: Interface de linha de comando com ajuda integrada
- ✅ **Verbose mode**: Modo detalhado para depuração

---

## 🚀 Começando

### Pré-requisitos

- Python 3.8 ou superior
- Git (opcional, para clonar)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/ojhonatanls/beaversec.git

# Entre na pasta
cd beaversec

# (Opcional) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt