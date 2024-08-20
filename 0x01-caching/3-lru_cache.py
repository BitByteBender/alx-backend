#!/usr/bin/env python3
""" LRU caching """
from base_caching import BaseCaching
from collections import OrderedDict


class LRUCache(BaseCaching):
    """
        Class defines an LRU caching sys
    """

    def __init__(self):
        """
            Inits the class
        """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """
            Assigns the item value to the dict for the given key
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data.move_to_end(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            k, v = self.cache_data.popitem(last=False)
            print("DISCARD: {}".format(k))

        self.cache_data[key] = item
        self.cache_data.move_to_end(key)

    def get(self, key):
        """
            Returns the value associated with key from self.cache_data
        """
        if key is None or key not in self.cache_data:
            return
        self.cache_data.move_to_end(key)
        return self.cache_data[key]
