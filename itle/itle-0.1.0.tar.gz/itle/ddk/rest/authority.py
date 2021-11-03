# -*- coding: UTF-8 -*-
import aiohttp as aiohttp

from itle.base import RestApi


class DDKPidAuthorityRequest(RestApi):
    """查询是否完成备案"""

    def __init__(self, aio_http: aiohttp, domain: str, port: int):
        super(DDKPidAuthorityRequest, self).__init__(aio_http, domain, port)

        self.ddk_pid = None
        self.custom_params = None

    def get_api_uri(self):
        return '/api/1.0/ddk/pid_auth'

    def get_method(self):
        return "GET"


class DDKPidAuthorityUrlRequest(RestApi):
    """创建备案链接"""

    def __init__(self, aio_http: aiohttp, domain: str, port: int):
        super(DDKPidAuthorityUrlRequest, self).__init__(aio_http, domain, port)
        self.ddk_pid_list = None
        self.channel_type = None
        self.custom_params = None
        self.amount = None
        self.scratch_card_amount = None
        self.diy_one_yuan_param = None
        self.diy_red_packet_param = None
        self.generate_qq_app = None
        self.generate_we_app = None
        self.generate_schema_url = None
        self.generate_short_url = None

    def get_api_uri(self):
        return '/api/1.0/ddk/pid_auth'

    def get_method(self):
        return 'POST'
