"""
Ping sweep module for BeaverSec.
"""
from __future__ import annotations

from beaversec.core.base_module import BaseModule, ModuleResult
from beaversec.core.registry import MODULE_ARGS, ArgDef
from beaversec.core.logging import get_logger

logger = get_logger("beaversec.modules.ping_sweep")

# Registrar argumentos do módulo
MODULE_ARGS.register(
    "ping_sweep",
    ArgDef(
        name="networks",
        type=list,
        required=True,
        help="Lista de alvos IP ou redes (CIDR)"
    )
)
MODULE_ARGS.register(
    "ping_sweep",
    ArgDef(
        name="timeout",
        type=float,
        required=False,
        default=2.0,
        help="Timeout em segundos"
    )
)


class PingSweepModule(BaseModule):
    """Módulo para varredura ICMP (ping sweep)."""
    
    name = "ping_sweep"
    description = "ICMP ping sweep for host discovery"
    
    async def run(self, networks, timeout=2.0, **kwargs):
        """Executa ping sweep em uma lista de redes."""
        logger.info(f"Iniciando ping sweep em {networks}")
        
        # Simulação: retorna um resultado de exemplo
        result = ModuleResult(
            module=self.name,
            target=str(networks),
            success=True,
            data={
                "alive_hosts": networks if isinstance(networks, list) else [networks],
                "total_scanned": len(networks) if isinstance(networks, list) else 1,
                "timeout": timeout
            }
        )
        
        logger.info(f"Ping sweep concluído: {len(result.data['alive_hosts'])} hosts ativos")
        return result
