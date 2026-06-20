# 🦫 BeaverSec

**B.E.A.V.E.R.** - *Binary Enumeration & Advanced Vulnerability Exploitation Recon*

Canivete suíço modular para cibersegurança, construído em Python com foco em aprendizado prático, evolução contínua e colaboração open-source.

---

## ⚡ Funcionalidades

### Módulos Disponíveis

| Módulo | Descrição | Exemplo |
|--------|-----------|---------|
| `ping_sweep` | Descoberta de hosts ativos via ICMP | `python3 main.py ping_sweep 192.168.1.0/24` |
| `port_scanner` | Varredura de portas TCP comuns | `python3 main.py port_scanner scanme.nmap.org` |

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

📖 Como Usar
Comandos Básicos
bash

# Listar módulos disponíveis
python3 main.py -l

# Executar um módulo
python3 main.py ping_sweep 8.8.8.8

# Modo detalhado
python3 main.py ping_sweep 192.168.1.0/24 -v

# Ajuda
python3 main.py -h

Scripts Rápidos
bash

# Configurar alias e instalação global
./setup.sh

# Varredura rápida
./scan.sh 8.8.8.8

# Varredura automática
python3 auto_scan.py

# Instalar dependências (se necessário)
./install.sh

# Atualizar do GitHub
./update.sh

Instalação Global (Opcional)
bash

# Instala o comando 'beaver' globalmente
sudo ln -s $(pwd)/main.py /usr/local/bin/beaver

# Agora pode usar de qualquer lugar:
beaver -l
beaver ping_sweep 8.8.8.8

📁 Estrutura do Projeto
text

beaversec/
├── beaversec/                 # Pacote principal
│   ├── core/                  # Núcleo do sistema
│   │   └── handler.py         # Gerenciador de módulos
│   ├── modules/               # Módulos (ferramentas)
│   │   ├── ping_sweep.py      # Varredura ICMP
│   │   └── port_scanner.py    # Varredura de portas
│   └── utils/                 # Utilitários
│       └── logger.py          # Sistema de logging
├── main.py                    # Ponto de entrada
├── README.md                  # Documentação
└── requirements.txt           # Dependências

🛠️ Criando um Novo Módulo

    Crie um arquivo em beaversec/modules/:

python

# beaversec/modules/meu_modulo.py
def run(target: str, verbose: bool = False) -> None:
    """Função obrigatória para o módulo"""
    print(f"Executando meu módulo contra {target}")
    if verbose:
        print("Modo detalhado ativado")

    Execute seu módulo:

bash

python3 main.py meu_modulo 8.8.8.8 -v

📖 Documentação

Para um guia detalhado com todos os comandos, exemplos e scripts:

    📄 Bíblia do BeaverSec (PDF) - Guia completo para impressão

    📝 Bíblia do BeaverSec (MD) - Versão Markdown interativa

🤝 Contribuindo

Contribuições são bem-vindas!

    Faça um fork do projeto

    Crie uma branch: git checkout -b feature/nova-funcionalidade

    Commit suas mudanças: git commit -m "Adiciona nova funcionalidade"

    Push: git push origin feature/nova-funcionalidade

    Abra um Pull Request

Reporte bugs ou sugira melhorias nas Issues.
📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
🎓 Projeto Acadêmico

Desenvolvido no 1º semestre de TSI (Tecnologia em Sistemas para Internet) na UTFPR - Toledo.

🦫 BeaverSec - Binary Enumeration & Advanced Vulnerability Exploitation Recon

"Conhecimento compartilhado é conhecimento multiplicado."