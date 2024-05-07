#!/usr/bin/python3
"""class LFUCache that inherits from BaseCaching and is a caching system
"""
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """
    LFUCache class inherits from BaseCaching and is a caching system and
    it implements the put and get methods to
    add and retrieve items from the cache
    with a LFU algorithm
    and if frequency is equal it perform as LRU algotithm
    """
    def __init__(self):
        super().__init__()
        self._LFU_key = None
        self._recentlyUsedKeys = []
        self._freqDict = {}

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return None

        data = self.cache_data
        if len(data) == self.MAX_ITEMS and key not in data.keys():
            freqDict = self._freqDict
            min_freq = min(freqDict.values())
            min_freq_keys = [k for k, v in freqDict.items() if v == min_freq]
            if len(freqDict) > 1:
                for k in self._recentlyUsedKeys:
                    if k in min_freq_keys:
                        self._LFU_key = k
                        break
            else:
                self._LFU_key = min_freq_keys[0]

            discarded_key = self._LFU_key
            del data[discarded_key]
            del self._freqDict[discarded_key]
            self._recentlyUsedKeys.remove(discarded_key)
            print("DISCARD: {}".format(discarded_key))

        data[key] = item
        if key in self._recentlyUsedKeys:
            self._recentlyUsedKeys.remove(key)
        self._recentlyUsedKeys.append(key)
        if key in self._freqDict.keys():
            self._freqDict[key] += 1
        else:
            self._freqDict[key] = 0

    def get(self, key):
        """ Get an item by key
        """
        if key is not None and key in self.cache_data.keys():
            if key in self._recentlyUsedKeys:
                self._recentlyUsedKeys.remove(key)
            self._recentlyUsedKeys.append(key)
            if key in self._freqDict.keys():
                self._freqDict[key] += 1
            else:
                self._freqDict[key] = 0
            return self.cache_data[key]
