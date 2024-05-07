#!/usr/bin/python3
"""class LRUCache that inherits from BaseCaching and is a caching system
"""
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """
    LRUCache class inherits from BaseCaching and is a caching system and
    it implements the put and get methods to
    add and retrieve items from the cache
    with a LRU algorithm
    """
    def __init__(self):
        super().__init__()
        self._LRU_key = None
        self._recentlyUsedKeys = []

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return None

        data = self.cache_data
        if len(data) == self.MAX_ITEMS and key not in data.keys():
            self._LRU_key = self._recentlyUsedKeys[0]
            discarded_key = self._LRU_key
            del data[discarded_key]
            self._recentlyUsedKeys.remove(discarded_key)
            print("DISCARD: {}".format(discarded_key))

        data[key] = item
        if key in self._recentlyUsedKeys:
            self._recentlyUsedKeys.remove(key)
        self._recentlyUsedKeys.append(key)

    def get(self, key):
        """ Get an item by key
        """
        if key is not None and key in self.cache_data.keys():
            if key in self._recentlyUsedKeys:
                self._recentlyUsedKeys.remove(key)
            self._recentlyUsedKeys.append(key)
            return self.cache_data[key]
