#!/usr/bin/python3
"""class LIFOCache that inherits from BaseCaching and is a caching system
"""
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFOCache class inherits from BaseCaching and is a caching system and
    it implements the put and get methods to
    add and retrieve items from the cache
    with a LIFO algorithm
    """
    def __init__(self):
        super().__init__()
        self._lastKey = None

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return None

        data = self.cache_data
        if len(data) == self.MAX_ITEMS and key not in data.keys():
            discarded_key = self._lastKey
            del data[discarded_key]
            print("DISCARD: {}".format(discarded_key))

        data[key] = item
        self._lastKey = key

    def get(self, key):
        """ Get an item by key
        """
        if key is not None and key in self.cache_data.keys():
            return self.cache_data[key]
