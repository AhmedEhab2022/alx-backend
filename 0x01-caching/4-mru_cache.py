#!/usr/bin/python3
"""class MRUCache that inherits from BaseCaching and is a caching system
"""
BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """
    MRUCache class inherits from BaseCaching and is a caching system and
    it implements the put and get methods to
    add and retrieve items from the cache
    with a MRU algorithm
    """
    def __init__(self):
        super().__init__()
        self._MRU_key = None
        self._recentlyUsedKeys = []

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return None

        data = self.cache_data
        if len(data) == self.MAX_ITEMS and key not in data.keys():
            last_index = len(self._recentlyUsedKeys) - 1
            self._MRU_key = self._recentlyUsedKeys[last_index]
            discarded_key = self._MRU_key
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
