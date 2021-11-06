'''调度器模块'''
import six
import w3lib.url
from hashlib import sha1
from six.moves.queue import Queue

from elegance_spider.conf import settings
from elegance_spider.utils.queue import Queue as RedisQueue
from elegance_spider.conf.settings import SCHEDULER_PRESIST
from elegance_spider.set import NormalFilterContainer, RedisFilterContainer
from elegance_spider.utils.log import logger


class Scheduler(object):
    '''调度器类'''

    def __init__(self, collector):
        self._filter_container = set()
        if SCHEDULER_PRESIST:
            self.queue = RedisQueue()
            self._filter_container = RedisFilterContainer()
        else:
            self.queue = Queue()
            self._filter_container = NormalFilterContainer()
        self.collectot = collector
        self.repeate_request_num = 0

    def add_request(self, request):
        if request.filter is False:
            self.queue.put(request)
            logger.info("添加请求成功：<disable去重>[%s %s]" %
                        (request.method, request.url))
            self.total_request_number += 1
            return

        fp = self._gen_fp(request)
        if not self._filter_request(fp, request):
            self.queue.put(request)
            logger.info("添加请求成功：<去重>[%s %s]" % (request.method, request.url))
            if settings.ROLE in ['master', 'slave']:
                self._backup_request.save_request(fp, request)
            self._filter_container.add_fp(fp)
            self.total_request_number += 1
        else:
            logger.info("重复请求 [%s %s]" % (request.method, request.url))
            self.repeate_request_num += 1

    def get_request(self):
        try:
            request = self.queue.get(False)
        except:
            return None
        else:
            if request.filter is True and settings.ROLE in ['master', 'salve']:
                fp = self._gen_fp(request)
                if request.retry_time >= settings.MAX_RETRY_TIMES:
                    self._backup_request.delete_request(fp)
                    logger.warning("出现异常请求，且超过最大尝试次数：[%s]%s" % (
                        request.method, request.url))
                request.retry_time += 1
                self._backup_request.update_request(fp, request)
            return request

    def delete_request(self, request):
        if settings.ROLE in ['master', 'slave']:
            fp = self._gen_fp(request)
            self._backup_request.delete_request(fp)

    def add_lost_request(self):
        if settings.ROLE in ['master', 'slave']:
            for request in self._backup_request.get_requests():
                self.queue.put(request)

    def _filter_request(self, request):
        request.fp = self._gen_fp(request)
        if not self._filter_container.exists(request.fp):
            self._filter_container.add_fp(request.fp)
            return True
        else:
            logger.info("发现重复的请求：<%s>" % request.url)
            self.repeate_request_num += 1
            return False

    def _gen_fp(self, request):
        '''请求去重，计算指纹'''
        url = w3lib.url.canonicalize_url(request.url)
        method = request.method.upper()
        data = request.data if request.data is not None else {}
        data = sorted(data.items(), key=lambda x: x[0])

        s1 = sha1()
        s1.update(self._to_bytes(url))
        s1.update(self._to_bytes(method))
        s1.update(self._to_bytes(str(data)))

        fp = s1.hexdigest()
        return fp

    @staticmethod
    def _to_bytes(s):
        if six.PY2:
            if isinstance(s, str):
                return s
            else:
                return s.encode('utf-8')
        elif six.PY3:
            if isinstance(s, str):
                return s.encode('utf-8')
            else:
                return s
