# -*- coding: utf-8 -*-
from enum import Enum


class DDKChannelType1(Enum):
    TODAY_HOT_SALES = 1  # 今日热销榜
    SIMILAR_GOODS = 3  # 相似商品推荐
    GUESS_U_LIKE = 4  # 猜你喜欢(和进宝网站精选一致)
    REALTIME_HOT_SALES = 5  # 实时热销榜
    REALTIME_EARNINGS = 6  # 实时收益榜


class DDKChannelType2(Enum):
    ACTIVITY_LIST = 1  # 活动列表
    RED_PACKET = 0  # 红包(需申请推广权限)
    FRESH_RED_PACKET = 2  # 新人红包
    SCRAPING_CARD = 3  # 刮刮卡
    EMPLOYEE_PURCHASE = 5  # 员工内购，
    GENERATE_BIND_URL = 10  # 生成绑定备案链接
    SMASH_GOLDEN_EGGS = 12  # 砸金蛋，
    ONE_YUAN_C = 13  # 一元购C端页面，
    BILLIONS_SUBSIDE_B = 14  # 千万补贴B端页面，
    RECHARGE_CENTER_B = 15  # 充值中心B端页面，
    BILLIONS_SUBSIDE_C = 16  # 千万补贴C端页面，
    BILLIONS_SUBSIDE_VOTE = 17  # 千万补贴投票页面，
    ONE_YUAN_B = 18  # 一元购B端页面，
    DD_BRAND_START_SEL_B = 19  # 多多品牌星选B端页面
    DD_BRAND_START_SEL_C = 20  # 多多品牌星选C端页面；


class DDKChannelType3(Enum):
    # 1.9包邮
    ONE_NINE = 0
    # 今日爆款
    EXPLOSIVE_TODAY = 1
    # 品牌清仓
    BRAND_CLEARANCE = 2
    # pc端专属商城
    PC_SHOPPING = 4
