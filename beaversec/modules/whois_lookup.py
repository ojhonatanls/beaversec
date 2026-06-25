"""
WHOIS lookup module for BeaverSec.
"""
from __future__ import annotations

from whois import whois
from typing import Any, Dict

from beaversec.core.base_module import BaseModule, ModuleResult
from beaversec.core.registry import MODULE_ARGS, ArgDef
from beaversec.core.logging import get_logger

logger = get_logger("beaversec.modules.whois_lookup")

# Registrar argumentos do módulo
MODULE_ARGS.register(
    "whois_lookup",
    ArgDef(
        name="target",
        type=str,
        required=True,
        help="Domínio ou IP para consulta WHOIS"
    )
)


class WhoisLookup(BaseModule):
    """Módulo para consulta WHOIS."""
    
    name = "whois_lookup"
    description = "WHOIS lookup for domains and IPs"
    
    async def run(self, target: str, **kwargs) -> ModuleResult:
        """Executa consulta WHOIS."""
        logger.info(f"Realizando consulta WHOIS para {target}")
        
        try:
            # Executa a consulta
            result = whois(target)
            
            # Converte o resultado para dicionário (apenas campos úteis)
            data = {
                "domain": target,
                "registrar": str(result.registrar) if result.registrar else None,
                "creation_date": str(result.creation_date) if result.creation_date else None,
                "expiration_date": str(result.expiration_date) if result.expiration_date else None,
                "name_servers": result.name_servers if result.name_servers else [],
                "status": result.status if result.status else [],
            }
            
            return ModuleResult(
                module=self.name,
                target=target,
                success=True,
                data=data
            )
        except Exception as e:
            logger.error(f"Erro na consulta WHOIS para {target}: {e}")
            return ModuleResult(
                module=self.name,
                target=target,
                success=False,
                data={"error": str(e)},
                error=str(e)
            )
