#!/usr/bin/env python3
""" LFU caching """
from base_caching import BaseCaching
from collections import defaultdict, OrderedDict


class LFUCache(BaseCaching):
    """
        Class defines an LFU caching sys
    """

    def __init__(self):
        """
            Inits the class
        """
        super().__init__()
        self.cache_data = {}
        self.freq = defaultdict(int)
        self.order = defaultdict(OrderedDict)

    def put(self, key, item):
        """
            Assigns the item value to the dict for the given key
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.freq[key] += 1
            del self.order[self.freq[key] - 1][key]
            self.order[self.freq[key]][key] = None
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                min_frq = min(self.freq.values())
                least = self.order[min_frq]
                if least:
                    k, v = least.popitem(last=False)
                    del self.cache_data[k]
                    del self.freq[k]
                    print("DISCARD: {}".format(k))

        self.cache_data[key] = item
        self.freq[key] = 1
        self.order[1][key] = None

    def get(self, key):
        """
            Returns the value associated with key from self.cache_data
        """
        if key is None or key not in self.cache_data:
            return None

        this_frq = self.freq[key]
        self.freq[key] += 1
        new_frq = self.freq[key]

        del self.order[this_frq][key]
        if not self.order[this_frq]:
            del self.order[this_frq]

        if new_frq not in self.order:
            self.order[new_frq] = OrderedDict()
        self.order[new_frq][key] = None

        return self.cache_data[key]
