#!/usr/bin/env python3
""" FIFO caching """
from base_caching import BaseCaching
from collections import OrderedDict


class FIFOCache(BaseCaching):
    """
        Class defines a FIFO caching sys
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

        self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            k, v = self.cache_data.popitem(False)
            print("DISCARD: {}".format(k))

    def get(self, key):
        """
            Returns the value associated with key from self.cache_data
        """
        return self.cache_data.get(key, None)
