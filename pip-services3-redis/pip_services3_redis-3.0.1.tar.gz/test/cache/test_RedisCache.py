# -*- coding: utf-8 -*-
import os

from pip_services3_commons.config import ConfigParams

from pip_services3_redis.cache.RedisCache import RedisCache
from test.fixtures.CacheFixture import CacheFixture


class TestRedisCache:
    _cache: RedisCache = None
    _fixture: CacheFixture = None

    def setup_method(self):
        host = os.environ.get('REDIS_SERVICE_HOST') or 'localhost'
        port = os.environ.get('REDIS_SERVICE_PORT') or 6379

        self._cache = RedisCache()

        config = ConfigParams.from_tuples(
            'connection.host', host,
            'connection.port', port
        )

        self._cache.configure(config)

        self._fixture = CacheFixture(self._cache)

        self._cache.open(None)

    def teardown_method(self):
        self._cache.close(None)

    def test_store_and_retrieve(self):
        self._fixture.test_store_and_retrieve()

    def test_retrieve_expired(self):
        self._fixture.test_retrieve_expired()

    def test_remove(self):
        self._fixture.test_remove()
