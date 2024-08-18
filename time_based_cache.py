from datetime import datetime
from enum import Enum
import time
from collections import OrderedDict


class CacheReturnState(Enum):
    HIT = "HIT"
    MISS = "MISS"


class ExpiryCache:
    def __init__(self, ttl = 1):
        self.items = {}

    def __getitem__(self, key):
        if key not in self.items:
            return None, CacheReturnState.MISS.value

        if (datetime.now() - self.items[key]["last_retrieved"]).total_seconds() > 1:
            del self.items[key]
            return None, CacheReturnState.MISS.value

        self.items[key]["last_retrieved"] = datetime.now()

        return self.items[key], CacheReturnState.HIT.value

    def __setitem__(self, key, value):
        self.items[key] = {"value": value, "added": datetime.now()}


data = OrderedDict({
    "exile": "folklore",
    "evermore": "folklore",
    "say don't go": "1989"
})

cache = ExpiryCache()

for key, value in data.items():
    cache[key] = value

print(cache["exile"])
time.sleep(2)
print(cache["exile"])
