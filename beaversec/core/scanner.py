"""
Base scanner classes for BeaverSec.
Unifies TCP, UDP, SYN, and ICMP scanning logic.
"""

import asyncio
import socket
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from beaversec.core.logging import get_logger
from beaversec.core.rate_limiter import RateLimiter

logger = get_logger("beaversec.core.scanner")


class BaseScanner(ABC):
    """Classe base para todos os scanners."""
    
    def __init__(
        self,
        target: str,
        timeout: float = 2.0,
        rate_limit: int = 100,
        proxy: Optional[str] = None,
        **kwargs
    ):
        self.target = target
        self.timeout = timeout
        self.rate_limiter = RateLimiter(rate_limit)
        self.proxy = proxy
        self.kwargs = kwargs
        self._results: List[Dict[str, Any]] = []
        self._semaphore = asyncio.Semaphore(kwargs.get('max_concurrent', 100))
    
    @abstractmethod
    async def scan(self) -> List[Dict[str, Any]]:
        """Executa o scan e retorna os resultados."""
        pass
    
    async def _execute_with_timeout(self, coro):
        """Executa uma coroutine com timeout."""
        try:
            return await asyncio.wait_for(coro, timeout=self.timeout)
        except asyncio.TimeoutError:
            logger.debug(f"Timeout ao executar scan em {self.target}")
            return None
        except Exception as e:
            logger.debug(f"Erro ao executar scan em {self.target}: {e}")
            return None
    
    async def _rate_limit(self):
        """Aplica rate limiting usando token bucket."""
        await self.rate_limiter.acquire()
    
    def _resolve_host(self, host: str) -> Optional[str]:
        """Resolve hostname para IP."""
        try:
            return socket.gethostbyname(host)
        except socket.gaierror:
            logger.error(f"Não foi possível resolver {host}")
            return None


class TCPScanner(BaseScanner):
    """Scanner TCP (conexão completa)."""
    
    def __init__(self, target: str, ports: List[int], **kwargs):
        super().__init__(target, **kwargs)
        self.ports = ports
    
    async def scan(self) -> List[Dict[str, Any]]:
        tasks = []
        for port in self.ports:
            await self._rate_limit()
            tasks.append(self._scan_port(port))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, dict) and result.get("open"):
                self._results.append(result)
        return self._results
    
    async def _scan_port(self, port: int) -> Dict[str, Any]:
        async with self._semaphore:
            try:
                reader, writer = await asyncio.open_connection(
                    self.target, port, timeout=self.timeout
                )
                writer.close()
                await writer.wait_closed()
                return {"port": port, "open": True, "service": "tcp"}
            except Exception:
                return {"port": port, "open": False}


class SYNScanner(BaseScanner):
    """Scanner SYN (half-open scan - requer privilégios)."""
    
    def __init__(self, target: str, ports: List[int], **kwargs):
        super().__init__(target, **kwargs)
        self.ports = ports
        # Nota: Implementação real com scapy seria necessário.
        # Este é um esqueleto que simula SYN scan.
    
    async def scan(self) -> List[Dict[str, Any]]:
        # Simulação: usa TCPScanner como fallback
        logger.warning("SYN scan requer privilégios. Usando TCP scan como fallback.")
        tcp_scanner = TCPScanner(self.target, self.ports, **self.kwargs)
        return await tcp_scanner.scan()


class UDPScanner(BaseScanner):
    """Scanner UDP."""
    
    def __init__(self, target: str, ports: List[int], **kwargs):
        super().__init__(target, **kwargs)
        self.ports = ports
    
    async def scan(self) -> List[Dict[str, Any]]:
        tasks = []
        for port in self.ports:
            await self._rate_limit()
            tasks.append(self._scan_udp_port(port))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, dict) and result.get("open"):
                self._results.append(result)
        return self._results
    
    async def _scan_udp_port(self, port: int) -> Dict[str, Any]:
        async with self._semaphore:
            try:
                loop = asyncio.get_running_loop()
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(self.timeout)
                
                # Envia um pacote vazio
                await loop.run_in_executor(
                    None, sock.sendto, b"", (self.target, port)
                )
                
                # Tenta receber resposta (ICMP unreachable indica fechado)
                try:
                    data, addr = await loop.run_in_executor(
                        None, sock.recvfrom, 1024
                    )
                    sock.close()
                    return {"port": port, "open": True, "service": "udp"}
                except socket.timeout:
                    sock.close()
                    return {"port": port, "open": True, "service": "udp (filtered)"}
            except Exception:
                return {"port": port, "open": False}


class ICMPScanner(BaseScanner):
    """Scanner ICMP (ping sweep)."""
    
    def __init__(self, targets: List[str], **kwargs):
        super().__init__(targets[0] if targets else "", **kwargs)
        self.targets = targets
    
    async def scan(self) -> List[Dict[str, Any]]:
        tasks = []
        for target in self.targets:
            await self._rate_limit()
            tasks.append(self._ping(target))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, dict) and result.get("alive"):
                self._results.append(result)
        return self._results
    
    async def _ping(self, target: str) -> Dict[str, Any]:
        # Simulação simples usando socket (ICMP requer privilégios)
        # Fallback: tenta conectar na porta 7 (echo)
        try:
            _, writer = await asyncio.open_connection(target, 7, timeout=self.timeout)
            writer.close()
            await writer.wait_closed()
            return {"target": target, "alive": True}
        except Exception:
            return {"target": target, "alive": False}