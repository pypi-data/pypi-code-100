# -*- coding: UTF-8 -*-
import aiohttp as aiohttp

from itle.base import RestApi


class DDKPidQueryRequest(RestApi):
    def __init__(self, aio_http: aiohttp, domain: str, port: int):
        super(DDKPidQueryRequest, self).__init__(aio_http, domain, port)

        self.ddk_pid_list = None
        self.page_index = None
        self.page_size = None
        self.status = None

    def get_api_uri(self):
        return '/api/1.0/ddk/pid'

    def get_method(self):
        return 'GET'


class DDKPidCreateRequest(RestApi):
    def __init__(self, aio_http: aiohttp, domain: str, port: int):
        super(DDKPidCreateRequest, self).__init__(aio_http, domain, port)

        self.media_id = None
        self.pid_name_list = None
        self.count = None

    def get_api_uri(self):
        return '/api/1.0/ddk/pid'

    def get_method(self):
        return 'POST'
