import redis
from elegance_spider.conf.settings import REDIS_QUEUE_HOST, REDIS_QUEUE_PORT, REDIS_QUEUE_DB, REDIS_QUEUE_PASSWORD


class StatsColector(object):

    def __init__(self, spider_names=[]):
        self.redis = redis.StrictRedis(
            host=REDIS_QUEUE_HOST, port=REDIS_QUEUE_PORT, db=REDIS_QUEUE_DB, password=REDIS_QUEUE_PASSWORD)
        self.request_nums_key = "_" . join(spider_names) + "_request_nums"
        self.response_nums_key = "_" . join(spider_names) + "_response_nums"
        self.repeat_request_nums_key = "_" . join(
            spider_names) + "_repeat_request_nums"
        self.start_request_nums_key = "_" . join(
            spider_names) + "_start_request_nums"

    def incr(self, key):
        self.redis.incr(key)

    def get(self, key):
        ret = self.redis.get(key)
        if not ret:
            ret = 0
        else:
            ret = int(ret)
        return ret

    def clear(self):
        self.redis.delete(self.request_nums_key, self.response_nums_key,
                          self.repeat_request_nums_key, self.start_request_nums_key)

    @property
    def request_nums(self):
        return self.get(self.request_nums_key)

    @property
    def response_nums(self):
        return self.get(self.response_nums_key)

    @property
    def repeat_request_nums(self):
        return self.get(self.repeat_request_nums_key)

    @property
    def start_request_nums(self):
        return self.get(self.start_request_nums_key)
