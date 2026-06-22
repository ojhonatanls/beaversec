"""
Consulta WHOIS para domínios.
"""
import logging
import asyncio

import whois

from beaversec.core.base_module import BaseModule

logger = logging.getLogger(__name__)


class WhoisLookup(BaseModule):
    """Consulta WHOIS de domínios."""

    name = "whois_lookup"
    description = "Consulta WHOIS de domínios"

    async def run(self, target: str, **kwargs) -> dict:
        self._log_start(target)
        
        # Rodar whois em um executor para não bloquear o loop
        loop = asyncio.get_event_loop()
        
        def _whois_query():
            return whois.whois(target)
        
        try:
            w = await loop.run_in_executor(None, _whois_query)
            data = {
                "domain_name": w.domain_name,
                "registrar": w.registrar,
                "whois_server": w.whois_server,
                "creation_date": str(w.creation_date) if w.creation_date else None,
                "expiration_date": str(w.expiration_date) if w.expiration_date else None,
                "name_servers": w.name_servers,
                "status": w.status,
                "emails": w.emails,
                "dnssec": w.dnssec,
            }
            return data
        except Exception as e:
            return {"error": str(e)}
