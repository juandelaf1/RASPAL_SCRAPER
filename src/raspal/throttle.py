import time
from collections import defaultdict


class AutoThrottle:
    def __init__(self, min_delay: float = 0.5, max_delay: float = 60.0, target_avg: float = 1.0):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.target_avg = target_avg
        self._delays: dict[str, float] = defaultdict(lambda: min_delay)
        self._last_request: dict[str, float] = defaultdict(float)
        self._response_times: dict[str, list[float]] = defaultdict(list)

    def wait(self, engine: str):
        delay = self._delays[engine]
        elapsed = time.time() - self._last_request[engine]
        if elapsed < delay:
            time.sleep(delay - elapsed)

    def record(self, engine: str, status: int):
        self._last_request[engine] = time.time()
        if status in (429, 503, 403):
            self._delays[engine] = min(self._delays[engine] * 2, self.max_delay)
        elif status in (200, 201, 301, 302):
            self._delays[engine] = max(self._delays[engine] * 0.9, self.min_delay)

    @property
    def current_delays(self) -> dict[str, float]:
        return dict(self._delays)
