import threading
import time
from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class TokenBucket:
    """
    Thread-safe token bucket.

    rate:
        Tokens replenished per second.

    capacity:
        Maximum burst capacity.
    """

    rate: float
    capacity: float

    def __post_init__(self) -> None:
        if self.rate <= 0:
            raise ValueError("Token rate must be greater than zero.")

        if self.capacity <= 0:
            raise ValueError("Token capacity must be greater than zero.")

        self.tokens = self.capacity
        self.updated_at = time.monotonic()
        self.lock = threading.Lock()

    def acquire(self, tokens: float = 1.0) -> None:
        if tokens <= 0:
            raise ValueError("Requested tokens must be greater than zero.")

        while True:
            with self.lock:
                now = time.monotonic()
                elapsed = now - self.updated_at

                self.tokens = min(
                    self.capacity,
                    self.tokens + elapsed * self.rate,
                )

                self.updated_at = now

                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return

                wait_seconds = (
                    tokens - self.tokens
                ) / self.rate

            time.sleep(max(wait_seconds, 0.01))


class ConnectorRateLimiter:
    """
    Maintains a separate token bucket for each:

        connector + operation

    Examples:
        openalex.list
        openalex.lookup
        core.search
        core.download
    """

    def __init__(self, registry) -> None:
        self.registry = registry
        self.buckets: Dict[
            Tuple[str, str],
            TokenBucket
        ] = {}
        self.lock = threading.Lock()

    def _build_bucket(
        self,
        connector_name: str,
        operation: str,
    ) -> TokenBucket:
        policy = self.registry.get_policy(
            connector_name,
            operation,
        )

        rate = float(
            policy.get(
                "requests_per_second",
                1.0,
            )
        )

        capacity = float(
            policy.get(
                "burst_capacity",
                max(1.0, rate),
            )
        )

        return TokenBucket(
            rate=rate,
            capacity=capacity,
        )

    def get_bucket(
        self,
        connector_name: str,
        operation: str,
    ) -> TokenBucket:
        key = (
            connector_name,
            operation,
        )

        with self.lock:
            if key not in self.buckets:
                self.buckets[key] = (
                    self._build_bucket(
                        connector_name,
                        operation,
                    )
                )

            return self.buckets[key]

    def acquire(
        self,
        connector_name: str,
        operation: str,
    ) -> None:
        self.get_bucket(
            connector_name,
            operation,
        ).acquire()
