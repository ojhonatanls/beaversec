"""Token bucket rate limiter for BeaverSec."""

import time
from threading import Lock
from typing import Optional

from beaversec.core.exceptions import RateLimitError
from beaversec.utils.audit_logger import AuditLogger


class RateLimiter:
    """
    Thread-safe token bucket rate limiter.

    Implements a token bucket algorithm for rate limiting operations.
    """

    _instances = {}

    def __new__(cls, key: str = "default"):
        """Get or create rate limiter instance."""
        if key not in cls._instances:
            cls._instances[key] = super().__new__(cls)
        return cls._instances[key]

    def __init__(self, key: str = "default"):
        """Initialize rate limiter."""
        if not hasattr(self, "_initialized"):
            self.key = key
            self.rate = 100.0  # Tokens per second
            self.capacity = 100.0  # Maximum tokens
            self.tokens = self.capacity
            self.last_refill = time.time()
            self.lock = Lock()
            self.logger = AuditLogger.get_logger(f"rate_limiter_{key}")
            self._initialized = True

    def configure(self, rate: float, capacity: float) -> None:
        """
        Configure rate limiter parameters.

        Args:
            rate: Tokens per second
            capacity: Maximum token capacity
        """
        with self.lock:
            self.rate = max(0.1, rate)
            self.capacity = max(1.0, capacity)
            self.tokens = min(self.tokens, self.capacity)

    def acquire(self, tokens: float = 1.0, timeout: Optional[float] = None) -> bool:
        """
        Acquire tokens from the bucket.

        Args:
            tokens: Number of tokens to acquire
            timeout: Maximum time to wait (seconds)

        Returns:
            bool: True if tokens acquired, False if timeout

        Raises:
            RateLimitError: If rate limit exceeded and no timeout specified
        """
        if tokens > self.capacity:
            raise RateLimitError(
                f"Requested {tokens} tokens exceeds capacity {self.capacity}"
            )

        start_time = time.time()

        while True:
            with self.lock:
                self._refill()
                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return True

                if timeout is not None and (time.time() - start_time) >= timeout:
                    self.logger.warning(f"Rate limit timeout after {timeout}s")
                    return False

                # Calculate wait time
                wait_time = (tokens - self.tokens) / self.rate

            # Wait outside the lock
            if timeout is not None:
                wait_time = min(wait_time, timeout - (time.time() - start_time))
                if wait_time <= 0:
                    return False

            time.sleep(min(wait_time, 0.1))

    def _refill(self):
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_refill = now


class RateLimiterManager:
    """
    Manages rate limiters for different operations.

    Provides centralized configuration and monitoring.
    """

    _instance = None

    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize rate limiter manager."""
        self.limiters = {}
        self.default_rate = 100.0
        self.default_capacity = 100.0
        self.logger = AuditLogger.get_logger("rate_limiter_manager")

    def get_limiter(self, key: str) -> RateLimiter:
        """
        Get or create a rate limiter.

        Args:
            key: Unique identifier for the limiter

        Returns:
            RateLimiter: Rate limiter instance
        """
        if key not in self.limiters:
            self.limiters[key] = RateLimiter(key)
            self.limiters[key].configure(self.default_rate, self.default_capacity)
        return self.limiters[key]

    def set_defaults(self, rate: float, capacity: float) -> None:
        """
        Set default rate limiter parameters.

        Args:
            rate: Default rate (tokens per second)
            capacity: Default capacity (tokens)
        """
        self.default_rate = rate
        self.default_capacity = capacity

        # Update existing limiters
        for limiter in self.limiters.values():
            limiter.configure(rate, capacity)

    def configure_limiter(self, key: str, rate: float, capacity: float) -> None:
        """
        Configure a specific rate limiter.

        Args:
            key: Limiter identifier
            rate: Rate (tokens per second)
            capacity: Capacity (tokens)
        """
        limiter = self.get_limiter(key)
        limiter.configure(rate, capacity)
        self.logger.info(f"Configured limiter {key}: rate={rate}, capacity={capacity}")