import redis
import pickle

from elegance_spider.http.request import Request
from elegance_spider.conf import settings


class RedisBackupRequest(object):
    '''利用hash类型，存储每个请求对象，key是指纹，value是请求对象'''
    REDIS_BACKUP_NAME = settings.REDIS_BACKUP_NAME
    REDIS_BACKUP_HOST = settings.REDIS_BACKUP_HOST
    REDIS_BACKUP_PORT = settings.REDIS_BACKUP_PORT
    REDIS_BACKUP_DB = settings.REDIS_BACKUP_DB
    REDIS_BACKUP_PASSWORD = settings.REDIS_BACKUP_PASSWORD

    def __init__(self):
        self._redis = redis.StrictRedis(
            host=self.REDIS_BACKUP_HOST, port=self.REDIS_BACKUP_PORT, db=self.REDIS_BACKUP_DB, password=self.REDIS_BACKUP_PASSWORD)
        self._name = self.REDIS_BACKUP_NAME

    def save_request(self, fp, request):
        bytes_data = pickle.dumps(request)
        self._redis.hset(self._name, fp, bytes_data)

    def delete_request(self):
        self._redis.hdel(self._name, fp)

    def update_request(self, fp, request):
        self.save_request(fp, request)

    def get_requests(self):
        for _, bytes_request in self._redis.hscan_iter(self._name):
            request = pickle.loads(bytes_request)
            yield request
