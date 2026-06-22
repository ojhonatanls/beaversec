"""
Rastreamento de rota (traceroute) com fallback.
"""
import logging
import shlex
import subprocess
from ipaddress import ip_address

from beaversec.core.base_module import BaseModule, ModuleResult

logger = logging.getLogger(__name__)


class Traceroute(BaseModule):
    """Rastreia a rota até o alvo usando traceroute do sistema."""

    name = "traceroute"
    description = "Rastreamento de rota até o alvo"

    def run(self, target: str, **kwargs) -> ModuleResult:
        self._log_start(target)
        validated = self.validate_input(target, **kwargs)

        # Valida se é IP ou hostname (básico)
        try:
            ip_address(target)
        except ValueError:
            # Pode ser hostname, válido
            pass

        # Usa subprocess com sanitização
        cmd = ["traceroute", "-n", "-w", str(int(validated.timeout)), target]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=validated.timeout * 2 + 5,
                check=False,
            )
            if result.returncode != 0:
                return ModuleResult(
                    module=self.name,
                    target=target,
                    success=False,
                    errors=[f"traceroute falhou: {result.stderr.strip()}"],
                )

            # Parse básico da saída
            lines = result.stdout.splitlines()
            hops = []
            for line in lines:
                if not line.strip() or "traceroute" in line:
                    continue
                parts = line.split()
                if parts and parts[0].isdigit():
                    hop_num = int(parts[0])
                    if len(parts) > 1:
                        ip_addr = parts[1] if parts[1] != "*" else None
                        if ip_addr and ip_addr != "*":
                            hops.append({"hop": hop_num, "ip": ip_addr})
                        else:
                            hops.append({"hop": hop_num, "ip": None})

            return ModuleResult(
                module=self.name,
                target=target,
                success=True,
                data={"hops": hops, "count": len(hops), "raw": result.stdout},
            )

        except subprocess.TimeoutExpired:
            return ModuleResult(
                module=self.name,
                target=target,
                success=False,
                errors=["Timeout no traceroute"],
            )
        except Exception as e:
            return ModuleResult(
                module=self.name,
                target=target,
                success=False,
                errors=[str(e)],
            )
