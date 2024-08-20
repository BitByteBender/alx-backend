#!/usr/bin/env python3
""" LIFO caching """
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
        Class defines a LIFO caching sys
    """

    def __init__(self):
        """
            Inits the class
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """
            Assigns the item value to the dict for the given key
        """
        if key is None and item is None:
            return

        rslt = self.cache_data
        if len(rslt) >= BaseCaching.MAX_ITEMS and key not in rslt:
            k = self.order.pop()
            del self.cache_data[k]
            print("DISCARD: {}".format(k))

        self.cache_data[key] = item
        if key not in self.order:
            self.order.append(key)

    def get(self, key):
        """
            Returns the value associated with key from self.cache_data
        """
        return self.cache_data.get(key, None)
