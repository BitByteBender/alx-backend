#!/usr/bin/env python3
""" LIFO caching """
from base_caching import BaseCaching
from collections import OrderedDict


class LIFOCache(BaseCaching):
    """
        Class defines a LIFO caching sys
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

        rslt = self.cache_data
        if len(rslt) >= BaseCaching.MAX_ITEMS:
            k, v = self.cache_data.popitem(True)
            print("DISCARD: {}".format(k))

        self.cache_data[key] = item

    def get(self, key):
        """
            Returns the value associated with key from self.cache_data
        """
        return self.cache_data.get(key, None)
