'''爬虫引擎'''
import time
import datetime
import importlib

from elegance_spider.http.request import Request
from elegance_spider.utils.log import logger
from elegance_spider.utils.stats_collector import StatsColector

from .scheduler import Scheduler
from .downloader import Downloader

from elegance_spider.conf.settings import SPIDERS, PIPLINES, SPIDER_MIDDLEWARES, DOWNLOADER_MIDDLEWARES, MAX_ASYNC_NUMBER, ASYNC_TYPE


if ASYNC_TYPE == 'thread':
    from multiprocessing.dummy import Pool
elif ASYNC_TYPE == 'coroutine':
    from elegance_spider.utils.coroutine import Pool
else:
    raise Exception('不支持的异步类型，%s, 只能支持thread和coroutine' % ASYNC_TYPE)


class Engine(object):

    def __init__(self):
        self.spiders = self._auto_import_instances(SPIDERS, isspider=True)
        self.downloader = Downloader()
        self.piplines = self._auto_import_instances(PIPLINES)
        self.collector = StatsColector(self.spiders)
        self.scheduler = Scheduler(self.collector)
        self.spider_middlewares = self._auto_import_instances(
            SPIDER_MIDDLEWARES)
        self.downloader_middlewares = self._auto_import_instances(
            DOWNLOADER_MIDDLEWARES)
        self.pool = Pool(4)
        self.running = False

    def _auto_import_instances(self, path=[], isspider=False):
        if isspider is True:
            instances = {}
        else:
            instances = []
        for p in path:
            module_name = p.rsplit(".", 1)[0]
            cls_name = p.rsplit(".", 1)[-1]
            model = importlib.import_module(module_name)
            cls = getattr(model, cls_name)
            if isspider is True:
                instances[cls.name] = cls()
            else:
                instances.append(cls())
        return instances

    def start(self):
        start_time = datetime.datetime.now()
        logger.info('爬虫开始：{}' . format(start_time))
        logger.info('爬虫运行模式：{}' . format(ASYNC_TYPE))
        logger.info('最大并发数：{}' . format(MAX_ASYNC_NUMBER))
        logger.info('启动的爬虫：{}' . format(list(self.spiders.keys())))
        logger.info('启动的下载中间件：\n{}' . format(DOWNLOADER_MIDDLEWARES))
        logger.info('启动的爬虫中间件：\n{}' . format(SPIDER_MIDDLEWARES))
        logger.info('启动的爬虫管道：\n{}' . format(PIPLINES))
        self._start_engine()
        end_time = datetime.datetime.now()
        logger.info("爬虫结束: {}" . format(end_time))
        logger.info("耗时：%s 秒" % (end_time - start_time).total_seconds())
        logger.info("总请求量: {}" . format(self.collector.request_nums))
        logger.info("重复的请求: {}个" . format(self.collector.repeat_request_nums))
        logger.info("成功的请求: {}个" . format(self.collector.response_nums))
        self.collector.clear()

    def _start_request_callback(self, temp):
        self.collector.incr(self.collector.start_request_nums_key)

    def _start_request(self):
        def _func(spider_name, spider):
            for start_request in spider.start_requests():
                for spider_middleware in self.spider_middlewares:
                    start_request = spider_middleware.process_request(
                        start_request)
                start_request.spider_name = spider_name
                self.scheduler.add_request(start_request)
                self.collector.incr(self.collector.request_nums_key)
        for spider_name, spider in self.spiders.items():
            self.pool.apply_async(_func, args=(
                spider_name, spider), callback=self._start_request_callback)

    def _execute_request_response_item(self):
        request = self.scheduler.get_request()
        if request is None:
            return

        spider = self.spiders[request.spider_name]

        for downloader_middleware in self.downloader_middlewares:
            request = downloader_middleware.process_request(request)

        response = self.downloader.get_response(request)

        response.meta = request.meta

        for downloader_middleware in self.downloader_middlewares:
            response = downloader_middleware.process_response(response)

        for spider_middleware in self.spider_middlewares:
            response = spider_middleware.process_response(response)

        parse = getattr(spider, request.parse)

        for result in parse(response):
            if isinstance(result, Request):
                result.spider_name = request.spider_name
                for spider_middleware in self.spider_middlewares:
                    result = spider_middleware.process_request(result)
                self.scheduler.add_request(result)
                self.collector.incr(self.collector.request_nums_key)
            else:
                for pipline in self.piplines:
                    result = pipline.process_item(result, spider)
        self.collector.incr(self.collector.response_nums_key)

    def _callback(self, _):
        if self.running:
            self.pool.apply_async(
                self._execute_request_response_item, callback=self._callback)

    def _start_engine(self):
        self.running = True
        self.pool.apply_async(self._start_request, callback=self._callback)
        for i in range(MAX_ASYNC_NUMBER):
            self.pool.apply_async(
                self._execute_request_response_item, callback=self._callback)

        while True:
            time.sleep(0.001)
            if self.collector.response_nums + self.collector.repeat_request_nums >= self.collector.request_nums:
                self.running = False
                break

        self.pool.close()
        self.pool.join()
