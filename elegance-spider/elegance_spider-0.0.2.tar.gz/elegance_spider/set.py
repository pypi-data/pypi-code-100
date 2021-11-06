import redis
from elegance_spider.conf import settings


class BaseFilterContainer(object):

    def add_fp(self, fp):
        pass

    def exists(self, fp):
        pass


class NormalFilterContainer(BaseFilterContainer):
    def __init__(self):
        self._filter_container = set()

    def add_fp(self, fp):
        self._filter_container.add(fp)

    def exists(self, fp):
        if fp in self._filter_container:
            return True
        else:
            return False


class RedisFilterContainer(BaseFilterContainer):
    REDIS_SET_NAME = settings.REDIS_SET_NAME
    REDIS_SET_HOST = settings.REDIS_SET_HOST
    REDIS_SET_PORT = settings.REDIS_SET_PORT
    REDIS_SET_DB = settings.REDIS_SET_DB

    def __init__(self):
        self._redis = redis.StrictRedis(
            host=self.REDIS_SET_HOST, port=self.REDIS_SET_PORT, db=self.REDIS_SET_DB)
        self._name = self.REDIS_SET_NAME

    def add_fp(self, fp):
        self._redis.sadd(self._name, fp)

    def exists(self, fp):
        return self._redis.sismember(self._name, fp)
