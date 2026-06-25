"""
Port scanner module for BeaverSec.
"""
from __future__ import annotations

from beaversec.core.base_module import BaseModule, ModuleResult
from beaversec.core.registry import MODULE_ARGS, ArgDef
from beaversec.core.logging import get_logger

logger = get_logger("beaversec.modules.port_scanner")

# Registrar argumentos do módulo
MODULE_ARGS.register(
    "port_scanner",
    ArgDef(
        name="targets",
        type=list,
        required=True,
        help="Lista de alvos IP ou hostnames"
    )
)
MODULE_ARGS.register(
    "port_scanner",
    ArgDef(
        name="ports",
        type=list,
        required=True,
        help="Lista de portas para scanear"
    )
)
MODULE_ARGS.register(
    "port_scanner",
    ArgDef(
        name="timeout",
        type=float,
        required=False,
        default=2.0,
        help="Timeout em segundos"
    )
)


class PortScannerModule(BaseModule):
    """Módulo para scan de portas TCP."""
    
    name = "port_scanner"
    description = "TCP port scanner"
    
    async def run(self, targets, ports, timeout=2.0, **kwargs):
        """Executa scan de portas TCP em múltiplos alvos."""
        logger.info(f"Iniciando port scan em {targets}: {len(ports)} portas")
        
        # Simulação: retorna um resultado de exemplo
        results = {}
        for target in targets:
            open_ports = []
            for port in ports[:5]:
                if port in [22, 80, 443]:
                    open_ports.append({"port": port, "open": True, "service": "tcp"})
            results[target] = {"open_ports": open_ports, "total_scanned": len(ports)}
        
        result = ModuleResult(
            module=self.name,
            target=str(targets),
            success=True,
            data=results
        )
        
        logger.info(f"Port scan concluído para {len(targets)} alvos")
        return result
