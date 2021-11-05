# -*- coding: UTF-8 -*-
import aiohttp as aiohttp

from itle.base import RestApi


class DDKIncrementalOrderListRequest(RestApi):
    """按最后更新时间段增量同步推广订单信息"""

    def __init__(self, aio_http: aiohttp, domain: str, port: int):
        super(DDKIncrementalOrderListRequest, self).__init__(aio_http, domain, port)
        self.start_tm = None
        self.end_tm = None
        self.page_index = None
        self.page_size = None
        self.query_order_type = None
        self.return_count = None
        self.cash_gift_order = None

    def get_api_uri(self):
        return '/api/1.0/ddk/incremental_order_list'

    def get_method(self):
        return 'GET'


class DDKRangedOrderListRequest(RestApi):
    """用支付时间段查询推广订单接口"""

    def __init__(self, aio_http: aiohttp, domain: str, port: int):
        super(DDKRangedOrderListRequest, self).__init__(aio_http, domain, port)

        self.start_time = None
        self.end_time = None
        self.last_order_id = None
        self.page_index = None
        self.page_size = None

    def get_api_uri(self):
        return '/api/1.0/ddk/ranged_order_list'

    def get_method(self):
        return 'GET'


class DDKOrderDetailsRequest(RestApi):
    """获取订单详情"""

    def __init__(self, aio_http: aiohttp, domain: str, port: int):
        super(DDKOrderDetailsRequest, self).__init__(aio_http, domain, port)

        self.order_sn = None
        self.query_order_type = None

    def get_api_uri(self):
        return '/api/1.0/ddk/order_details'

    def get_method(self):
        return 'GET'
