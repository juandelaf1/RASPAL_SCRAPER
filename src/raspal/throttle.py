import random
import time
from collections import defaultdict
from typing import Self


class AutoThrottle:
    def __init__(
        self,
        min_delay: float = 0.5,
        max_delay: float = 60.0,
        target_avg: float = 1.0,
        jitter: float = 0.1,
    ):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.target_avg = target_avg
        self.jitter = jitter
        self._delays: dict[str, float] = defaultdict(lambda: min_delay)
        self._last_request: dict[str, float] = defaultdict(float)
        self._response_times: dict[str, list[float]] = defaultdict(list)
        self._closed = False

    def wait(self, engine: str):
        if self._closed:
            return
        delay = self._delays[engine]
        jitter_amount = delay * self.jitter * random.random()
        effective = delay + jitter_amount
        elapsed = time.time() - self._last_request[engine]
        if elapsed < effective:
            time.sleep(effective - elapsed)

    def record(self, engine: str, status: int):
        if self._closed:
            return
        self._last_request[engine] = time.time()
        if status in (429, 503, 403):
            self._delays[engine] = min(self._delays[engine] * 2, self.max_delay)
        elif status in (200, 201, 301, 302):
            self._delays[engine] = max(self._delays[engine] * 0.9, self.min_delay)

    def reset(self, engine: str | None = None):
        if engine:
            self._delays[engine] = self.min_delay
        else:
            for k in self._delays:
                self._delays[k] = self.min_delay

    @property
    def current_delays(self) -> dict[str, float]:
        return dict(self._delays)

    def close(self):
        self._closed = True

    def __enter__(self) -> Self:
        self._closed = False
        return self

    def __exit__(self, *args):
        self.close()
