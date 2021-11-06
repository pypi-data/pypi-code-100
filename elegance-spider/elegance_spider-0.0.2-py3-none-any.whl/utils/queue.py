'''队列'''
import time
import redis
import pickle
from six.moves import queue as BaseQueue

from elegance_spider.conf.settings import REDIS_QUEUE_HOST, REDIS_QUEUE_PORT, REDIS_QUEUE_DB, REDIS_QUEUE_NAME, REDIS_QUEUE_PASSWORD


class Queue(object):
    '''Redis as queue'''
    Empty = BaseQueue.Empty
    Full = BaseQueue.Full
    max_timeout = 0.3

    def __init__(self, maxsize=0, lazy_limit=True):
        self.name = REDIS_QUEUE_NAME
        self.redis = redis.StrictRedis(
            host=REDIS_QUEUE_HOST, port=REDIS_QUEUE_PORT, db=REDIS_QUEUE_DB, password=REDIS_QUEUE_PASSWORD)
        self.maxsize = maxsize
        self.lazy_limit = lazy_limit
        self.last_qsize = 0

    def qsize(self):
        self.last_qsize = self.redis.llen(self.name)
        return self.last_qsize

    def empty(self):
        if self.qsize() == 0:
            return True
        else:
            return False

    def full(self):
        if self.maxsize and self.qsize() >= self.maxsize:
            return True
        else:
            return False

    def put_nowait(self, obj):
        if self.lazy_limit and self.last_qsize < self.maxsize:
            pass
        elif self.full():
            raise self.Full
        self.last_qsize = self.redis.rpush(self.name, pickle.dumps(obj))
        return True

    def put(self, obj, block=True, timeout=None):
        if not block:
            return self.put_nowait(obj)

        start_time = time.time()
        while True:
            try:
                return self.put_nowait(obj)
            except self.Full:
                if timeout:
                    lasted = time.time() - start_time
                    if timeout > lasted:
                        time.sleep(min(self.max_timeout, timeout - lasted))
                    else:
                        raise
                else:
                    time.sleep(self.max_timeout)

    def get_nowait(self):
        ret = self.redis.lpop(self.name)
        if ret is None:
            raise self.Empty
        return pickle.loads(ret)

    def get(self, block=True, timeout=None):
        if not block:
            return self.get_nowait()

        start_time = time.time()
        while True:
            try:
                return self.get_nowait()
            except self.Empty:
                if timeout:
                    lasted = time.time() - start_time
                    if timeout > lasted:
                        time.sleep(min(self.max_timeout, timeout - lasted))
                    else:
                        raise
                else:
                    time.sleep(self.max_timeout)
