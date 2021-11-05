# -*- coding: utf-8 -*-

from enum import Enum


class DDKResourceType(Enum):
    SECOND_KILL = 4  # - 限时秒杀,
    RECHARGE_CENTER = 39997  # - 充值中心
    ACTIVITY_URL_TRANS = 39998  # - 活动转链
    BILLIONS_SUBSIDE = 39996  # - 百亿补贴
    ELECTRIC_MALL = 39999  # - 电器城
    VOUCHER_CENTER = 40000  # - 领券中心
    TRAIN_TICKETS = 50005  # - 火车票

