from datetime import datetime
from enum import Enum
import time
from collections import OrderedDict


class CacheReturnState(Enum):
    HIT = "HIT"
    MISS = "MISS"


class LRUCache:
    def __init__(self, max_size = 2):
        self.cache = OrderedDict()
        self.max_size = max_size

    def __getitem__(self, key):
        if key not in self.cache:
            return CacheReturnState.MISS.value
        
        self.cache.move_to_end(key)

        return self.cache[key]
    
    def __setitem__(self, key, value):
        self.cache[key] = value

        if len(self.cache) > self.max_size:
            self.cache.popitem(last = False)

class TimedLRUCache:
    def __init__(self, max_size = 2, ttl = 1):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.ttl = ttl

    def __getitem__(self, key):
        if key not in self.cache:
            return CacheReturnState.MISS.value
        
        if (datetime.now() - self.cache[key]["added"]).total_seconds() > self.ttl:
            del self.cache[key]
            return CacheReturnState.MISS.value
        
        self.cache.move_to_end(key)

        return self.cache[key]["value"]
    
    def __setitem__(self, key, value):
        self.cache[key] = {"value": value, "added": datetime.now()}

        if len(self.cache) > self.max_size:
            self.cache.popitem(last = False)


data = OrderedDict({
    "exile": "folklore",
    "evermore": "folklore",
    "say don't go": "1989"
})

cache = LRUCache()

for key, value in data.items():
    cache[key] = value

print(cache["exile"])
print(cache["evermore"])
print(cache["say don't go"])
