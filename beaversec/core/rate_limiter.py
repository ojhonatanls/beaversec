"""
Token-bucket rate limiter for async operations.
"""

import asyncio
import time
from typing import Optional


class RateLimiter:
    """Token bucket rate limiter for async operations."""
    
    def __init__(self, rate: float, burst: Optional[int] = None, capacity: Optional[int] = None):
        """
        Initialize rate limiter.
        
        Args:
            rate: Tokens per second.
            burst: Maximum burst size (default: rate).
            capacity: Alias for burst (for compatibility with older modules).
        """
        # Se capacity for fornecido, usa ele como burst (compatibilidade)
        if capacity is not None:
            burst = capacity
        self.rate = rate
        self.burst = burst if burst is not None else int(rate)
        self.tokens = self.burst
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()
    
    async def acquire(self, tokens: int = 1) -> None:
        """Acquire tokens from the bucket."""
        async with self._lock:
            self._refill()
            if self.tokens < tokens:
                wait_time = (tokens - self.tokens) / self.rate
                await asyncio.sleep(wait_time)
                self._refill()
            self.tokens -= tokens
    
    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill
        new_tokens = elapsed * self.rate
        self.tokens = min(self.burst, self.tokens + new_tokens)
        self.last_refill = now


# Alias para compatibilidade com módulos antigos
TokenBucket = RateLimiter