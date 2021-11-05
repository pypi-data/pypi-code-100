# -*- coding: UTF-8 -*-
import aiohttp as aiohttp

from itle.base import RestApi


class DDKCatsRequest(RestApi):
    def __init__(self, aio_http: aiohttp, domain: str, port: int):
        super(DDKCatsRequest, self).__init__(aio_http, domain, port)
        self.parent_cat_id = None

    def get_api_uri(self):
        return '/api/1.0/ddk/cats'

    def get_method(self):
        return "GET"
