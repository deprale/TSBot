from __future__ import annotations

import asyncio
import time
import logging


logger = logging.getLogger(__name__)


class RateLimiter:
    def __init__(self, max_calls: int, period: float) -> None:
        self._max_calls: int = max_calls
        self._period: float = period

        self._calls: int = 0
        self._since: float = time.monotonic_ns()

    async def wait(self):
        remaining = self._period - (time.monotonic_ns() - self._since)

        if remaining <= 0:
            self._calls = 0
            self._since = time.monotonic_ns()

        self._calls += 1

        if self._calls > self._max_calls:
            logger.debug("Ratelimiting, sleeping for %ss", remaining)
            await asyncio.sleep(remaining)