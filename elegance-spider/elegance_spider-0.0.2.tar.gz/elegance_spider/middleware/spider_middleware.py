class SpiderMiddleware(object):
    '''爬虫中间件'''

    def process_request(self, request):
        '''请求处理'''
        print('爬虫中间件')
        return request

    def process_response(self, response):
        '''预处理数据'''
        print('爬虫中间件预处理')
        return response


class TestSpiderMiddleware1(object):
    ''''''

    def process_request(self, request):
        print('TestSpiderMiddleware1: process_request')
        return request

    def process_item(self, item):
        print('TestSpiderMiddleware1: process_item')
        return item


class TestSpiderMiddleware2(object):
    ''''''

    def process_request(self, request):
        print('TestSpiderMiddleware2: process_request')
        return request

    def process_item(self, item):
        print('TestSpiderMiddleware2: process_item')
        return item
