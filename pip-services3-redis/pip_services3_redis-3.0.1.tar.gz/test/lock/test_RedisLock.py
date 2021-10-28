# -*- coding: utf-8 -*-
import os

from pip_services3_commons.config import ConfigParams

from pip_services3_redis.lock.RedisLock import RedisLock
from test.fixtures.LockFixture import LockFixture


class TestRedisLock:
    _lock: RedisLock = None
    _fixture: LockFixture = None

    def setup_method(self):
        host = os.environ.get('REDIS_SERVICE_HOST') or 'localhost'
        port = os.environ.get('REDIS_SERVICE_PORT') or 6379

        self._lock = RedisLock()

        config = ConfigParams.from_tuples(
            'connection.host', host,
            'connection.port', port
        )

        self._lock.configure(config)

        self._fixture = LockFixture(self._lock)

        self._lock.open(None)

    def teardown_method(self):
        self._lock.close(None)

    def test_try_acquire_lock(self):
        self._fixture.test_try_acquire_lock()

    def test_acquire_lock(self):
        self._fixture.test_acquire_lock()

    def test_release_lock(self):
        self._fixture.test_release_lock()
