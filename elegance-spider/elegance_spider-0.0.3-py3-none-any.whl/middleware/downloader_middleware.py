class DownloaderMiddleware(object):
    '''下载器中间件'''

    def process_request(self, request):
        '''预处理请求'''
        print('下载器中间件，预处理请求')
        return request

    def process_response(self, response):
        '''预处理响应'''
        print('下载器中间件，预处理响应')
        return response


class TestDownloaderMiddleware1(object):

    def process_request(self, request):
        '''处理请求头，添加默认的user-agent'''
        print("TestDownloaderMiddleware1: process_request")
        return request

    def process_response(self, item):
        '''处理数据对象'''
        print("TestDownloaderMiddleware1: process_response")
        return item


class TestDownloaderMiddleware2(object):

    def process_request(self, request):
        '''处理请求头，添加默认的user-agent'''
        print("TestDownloaderMiddleware2: process_request")
        return request

    def process_response(self, item):
        '''处理数据对象'''
        print("TestDownloaderMiddleware2: process_response")
        return item
