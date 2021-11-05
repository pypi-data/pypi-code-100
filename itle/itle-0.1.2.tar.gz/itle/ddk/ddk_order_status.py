# -*- coding: utf-8 -*-
from enum import Enum


# @see https://jinbao.pinduoduo.com/third-party/api-detail?apiName=pdd.ddk.order.list.increment.get

class DDKQueryOrderType(Enum):
    # 推广订单
    PROMOTION = 1
    # 直播订单
    LIVE_BROADCAST = 2


class DDKOrderStatus(Enum):
    PAID = 0  # -已支付；
    MASSED = 1  # -已成团；
    RECVD = 2  # -确认收货；
    APPROVED = 3  # -审核成功；
    AUDITED_FAILED = 4  # -审核失败（不可提现）；
    SETTLED = 5  # -已经结算 ;
    PUNISHED = 10  # -已处罚
