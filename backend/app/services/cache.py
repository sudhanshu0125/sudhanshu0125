import time
from collections.abc import Callable


class TTLCache:
    def __init__(self):
        self._cache: dict[str, tuple[float, object]] = {}

    def get_or_set(self, key: str, ttl_seconds: int, supplier: Callable[[], object]):
        now = time.time()
        if key in self._cache and self._cache[key][0] > now:
            return self._cache[key][1]
        value = supplier()
        self._cache[key] = (now + ttl_seconds, value)
        return value


cache = TTLCache()
