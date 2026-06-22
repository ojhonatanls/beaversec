"""
beaversec/modules/ping_sweep.py

Correções principais:
- Torna ping compatível com Windows e Unix (opções diferentes).
- Timeout e count tratados corretamente.
- Regex de RTT mais tolerante.
- Retorna dicionário consistente.
"""
import subprocess
import re
import platform
from typing import Dict, Any

def run(target: str, **kwargs) -> Dict[str, Any]:
    """
    Realiza ping sweep no alvo.
    Args:
        target: IP ou domínio para ping
        **kwargs: timeout (int em segundos), count (int)
    Returns:
        Dict com resultados
    """
    timeout = int(kwargs.get("timeout", 3))
    count = int(kwargs.get("count", 1))

    system = platform.system()
    if system == "Windows":
        # -n count, -w timeout in milliseconds
        cmd = ["ping", "-n", str(count), "-w", str(timeout * 1000), target]
    else:
        # Unix-like: -c count, -W timeout (seconds) on many distros; note: -W behavior varies
        cmd = ["ping", "-c", str(count), "-W", str(timeout), target]

    print(f"📡 Pingando {target}...")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
        alive = (result.returncode == 0)

        # Extrai RTT (procura por time=... ou tempo=... e números com decimais)
        rtt = None
        if result.stdout:
            match = re.search(r"(?:time[=<]\s*|tempo=)\s*([0-9]+(?:\.[0-9]+)?)", result.stdout)
            if match:
                try:
                    rtt = float(match.group(1))
                except Exception:
                    rtt = None

        return {
            "host": target,
            "alive": alive,
            "rtt": rtt,
            "output": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }

    except subprocess.TimeoutExpired:
        return {"host": target, "alive": False, "error": "timeout"}
    except Exception as e:
        return {"host": target, "alive": False, "error": str(e)}
