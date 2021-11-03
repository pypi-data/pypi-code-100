# -*- coding: utf-8 -*-

# 拼多多活动配置
from enum import Enum


class DDKActiveStat(Enum):
    # 新人红包
    DDK_NEWCOMER_RED_ENVELOPE = 2
    # 刮刮卡
    DDK_SCRATCH_CARD = 3
    # 限时秒杀
    DDK_LIMITED_TIME_SPIKE = 4
    # 员工内购
    DDK_EMPLOYEE_APP_PURCHASE = 5
    # 购物车
    DDK_SHOPPING_CART = 6
    # 大促会场
    DDK_BIG_PROMOTION_VENUE = 7
    # 直播间列表集合
    DDK_COLLECTION_ROOM_LIST = 8
    # 1.9包邮
    DDK_ONE_NINE = 9
    # 今日爆款
    DDK_EXPLOSIVE_TODAY = 10
    # 品牌清仓
    DDK_BRAND_CLEARANCE = 11
    # pc端专属商城
    DDK_PC_SHOPPING = 12
    # 充值中心
    DDK_RECHARGE_CENTRE = 13
    # 百亿补贴
    DDK_BILLIONS_SUBSIDIES = 14

