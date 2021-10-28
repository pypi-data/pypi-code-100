# -*- coding: utf-8 -*-
import time

from pip_services3_components.cache import ICache

KEY1: str = "key1"
KEY2: str = "key2"

VALUE1: str = "value1"
VALUE2: str = "value2"


class CacheFixture:

    def __init__(self, cache: ICache):
        self.__cache: ICache = cache

    def test_store_and_retrieve(self):
        self.__cache.store(None, KEY1, VALUE1, 5000)
        self.__cache.store(None, KEY2, VALUE2, 5000)

        time.sleep(0.5)

        val = self.__cache.retrieve(None, KEY1).decode('utf-8')
        assert val is not None
        assert VALUE1 == val

        val = self.__cache.retrieve(None, KEY2).decode('utf-8')
        assert val is not None
        assert VALUE2 == val

    def test_retrieve_expired(self):
        self.__cache.store(None, KEY1, VALUE1, 1000)

        time.sleep(1.5)

        val = self.__cache.retrieve(None, KEY1)
        assert val is None

    def test_remove(self):
        self.__cache.store(None, KEY1, VALUE1, 1000)

        self.__cache.remove(None, KEY1)

        val = self.__cache.retrieve(None, KEY1)
        assert val is None
