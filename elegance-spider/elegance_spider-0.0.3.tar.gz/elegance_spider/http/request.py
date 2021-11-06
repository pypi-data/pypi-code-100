"""封装Request对象"""


class Request(object):
    """
    Request对象
    """

    def __init__(self, url, method='GET', headers=None, params=None, data=None, parse='parse', filter=True):
        self.url = url
        self.method = method
        self.headers = headers
        self.data = data
        self.params = params
        self.parse = parse
        self.meta = None
        self.filter = filter
        self.retry_time = 0
