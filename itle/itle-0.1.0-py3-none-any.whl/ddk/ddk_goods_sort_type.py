# -*- coding: utf-8 -*-
from enum import Enum, auto


class DDKSortType(Enum):
    # 综合排序
    Synthetical = 0

    # 按佣金比率
    CommissionRateASC = 1
    CommissionRateDESC = 2

    # 按价格
    SalePriceASC = 3
    SalePriceDESC = 4

    # 按销量
    SaleVolumeASC = 5
    SaleVolumeDESC = 6

    # 优惠券金额排序
    CouponAmountASC = 7
    CouponAmountDESC = 8

    # 券后价升序排序
    PostCouponPriceASC = 9
    PostCouponPriceDESC = 10

    # 按照加入多多进宝时间
    JoinDDKTimeASC = 11
    JoinDDKTimeDESC = 12

    # 按佣金金额
    CommissionAmountASC = 13
    CommissionAmountDESC = 14

    # 店铺描述评分
    StoreDescScoreASC = 15
    StoreDescScoreDESC = 16

    # 店铺物流评分
    StoreLogisticsScoreASC = 17
    StoreLogisticsScoreDESC = 18

    # 店铺服务评分
    StoreServiceScoreASC = 19
    StoreServiceScoreDESC = 20

    # 描述评分击败同类店铺百分比
    SimilarStoreDescRankingASC = 27
    SimilarStoreDescRankingDESC = 28

    # 物流评分击败同类店铺百分比
    SimilarStoreLogisticsRankingASC = 29
    SimilarStoreLogisticsRankingDESC = 30

    # 服务评分击败同类店铺百分比
    SimilarStoreServiceRankingASC = 31
    SimilarStoreServiceRankingDESC = 32
