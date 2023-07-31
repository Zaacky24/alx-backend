from collections import defaultdict
from datetime import datetime
from base_caching import BaseCaching

class LFUCache(BaseCaching):
    def __init__(self):
        super().__init__()
        self.frequency = defaultdict(int)
        self.time_used = {}
        self.min_frequency = 1

    def update_frequency(self, key):
        self.frequency[key] += 1
        self.time_used[key] = datetime.now()
        if self.frequency[key] < self.min_frequency:
            self.min_frequency = self.frequency[key]

    def update_cache(self, key, item):
        self.cache_data[key] = item
        self.update_frequency(key)

    def discard_least_frequency(self):
        keys_to_discard = [key for key in self.cache_data if self.frequency[key] == self.min_frequency]
        if len(keys_to_discard) > 1:
            least_recently_used = min(keys_to_discard, key=lambda key: self.time_used[key])
            keys_to_discard = [key for key in keys_to_discard if key != least_recently_used]
        return keys_to_discard

    def put(self, key, item):
        if key is None or item is None:
            return

        if len(self.cache_data) >= self.MAX_ITEMS:
            keys_to_discard = self.discard_least_frequency()
            for key in keys_to_discard:
                self.frequency.pop(key)
                self.cache_data.pop(key)
                self.time_used.pop(key)
                print(f"DISCARD: {key}")

        self.update_cache(key, item)

    def get(self, key):
        if key is None or key not in self.cache_data:
            return None

        self.update_frequency(key)
        return self.cache_data[key]

