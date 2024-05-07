#!/usr/bin/python3
"""class FIFOCache that inherits from BaseCaching and is a caching system
"""
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFOCache class inherits from BaseCaching and is a caching system and
    it implements the put and get methods to
    add and retrieve items from the cache
    with a FIFO algorithm
    """
    def __init__(self):
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return

        data = self.cache_data
        if len(data) == self.MAX_ITEMS and key not in data.keys():
            discarded_key = list(data.keys())[0]
            del data[discarded_key]
            print("DISCARD: {}".format(discarded_key))

        data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        if key is not None and key in self.cache_data.keys():
            return self.cache_data[key]
