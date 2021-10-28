# -*- coding: utf-8 -*-
from pip_services3_commons.refer import Descriptor
from pip_services3_components.build import Factory

from pip_services3_redis.cache.RedisCache import RedisCache
from pip_services3_redis.lock.RedisLock import RedisLock


class DefaultRedisFactory(Factory):
    """
    Creates Redis components by their descriptors.

    See: :class:`RedisCache <pip_services3_redis.cache.RedisCache.RedisCache>`, :class:`RedisLock <pip_services3_redis.lock.RedisLock.RedisLock>`

    """
    __RedisCacheDescriptor = Descriptor("pip-services", "cache", "redis", "*", "1.0")
    __RedisLockDescriptor = Descriptor("pip-services", "lock", "redis", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super().__init__()

        self.register_as_type(DefaultRedisFactory.__RedisCacheDescriptor, RedisCache)
        self.register_as_type(DefaultRedisFactory.__RedisLockDescriptor, RedisLock)
