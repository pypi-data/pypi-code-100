'''爬虫组件'''
from elegance_spider.item import Item
from elegance_spider.http.request import Request


class Spider(object):
    '''
    '''
    start_urls = []

    def start_requests(self):
        '''构建初始请求对象并返回'''
        for url in self.start_urls:
            yield Request(url)

    def parse(self, response):
        '''解析响应对象'''
        yield Item(response.body)
