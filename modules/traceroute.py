"""
modules/traceroute.py

Correções principais:
- Verifica se o comando existe (shutil.which) antes de executar.
- Compatibilidade Windows / Unix.
- Exibe saída em tempo real sem bloquear em leituras inseguras.
- Melhor tratamento de erros.
"""
import subprocess
import platform
import shutil

def run(target, **kwargs):
    """
    Executa traceroute para o alvo (usa comando do sistema).
    Exemplo: python main.py traceroute google.com
    """
    system = platform.system()
    try:
        if system == "Windows":
            cmd_name = "tracert"
            cmd = [cmd_name, "-d", "-h", "30", target]
        else:
            cmd_name = "traceroute"
            cmd = [cmd_name, "-n", "-m", "30", target]

        # Verifica existência do comando
        if shutil.which(cmd_name) is None:
            if system == "Windows":
                print("[-] Comando 'tracert' não encontrado no sistema Windows.")
            else:
                print("[-] Comando 'traceroute' não encontrado no sistema.")
                print("    Instale com: apt-get install traceroute (Debian/Ubuntu) ou use o gerenciador da sua distro.")
            return None

        print(f"[+] Running traceroute to {target}...")
        print("    (Aguarde, pode levar alguns segundos)")

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Leitura em tempo real da saída padrão
        for line in process.stdout:
            if line:
                print(f"    {line.rstrip()}")

        process.wait()
        if process.returncode != 0:
            stderr = process.stderr.read()
            print(f"[-] Traceroute falhou com código {process.returncode}")
            if stderr:
                print(f"    Error: {stderr.strip()}")

        return True

    except Exception as e:
        print(f"[-] Erro inesperado: {e}")
        return False
