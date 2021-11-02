
from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel

from .trades import Transaction


class TradeReport(BaseModel):
    order_id: str
    order_type: str
    usd_observed: float
    utility_currency: float
    utility_pair_currency: float
    time: float
    date: datetime
    trade_id: Optional[str] = None

    def __str__(self):
        out = ""
        out += f"\t**Order Id**: {self.order_id}"
        out += f"\t**Order Type**: {self.order_type}"
        out += f"\t**Utility Currency**: {self.utility_currency}"
        out += f"\t**Utility Pair Currency**: {self.utility_pair_currency}"
        out += f"\t**USD Observed**: {self.usd_observed}"
        out += f"\t**Time**: {self.time}"
        return out


class OneSideUtilityReport(TradeReport):
    market: str
    transaction: Transaction
    usd_real: float = 0.0

    def __init__(self, **data):
        super().__init__(**data)
        self.trade_id = self.transaction.id

    def __str__(self):
        out = super().__str__()
        out += f"\t**Market**: {self.market}"
        out += f"\t**USD Real**: {self.usd_real}"
        return out


class TwoSideUtilityReport(TradeReport):
    origin_transaction: Transaction
    target_transaction: List[Transaction]

    def __init__(self, **data):
        super().__init__(**data)
        self.trade_id = f"{self.origin_transaction.id}:{':'.join([tx.id for tx in self.target_transaction])}"

    def __str__(self):
        out = super().__str__()
        target_ids = [tx.id for tx in self.target_transaction]
        target_exchange = self.target_transaction[0].exchange
        target_market = self.target_transaction[0].market
        out += f"\t**{target_exchange.upper()} Tx IDs**: {target_ids}"
        out += f"\t**Origin Market**: {self.origin_transaction.market}"
        out += f"\t**Target Market**: {target_market}"
        return out
