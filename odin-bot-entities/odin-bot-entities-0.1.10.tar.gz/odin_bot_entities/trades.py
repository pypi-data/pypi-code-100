from abc import ABC, abstractmethod
from typing import Optional, List
from pydantic import BaseModel


class Transaction(BaseModel):
    id: str
    currency_name: str
    pair_currency_name: str
    market: str
    exchange: str
    time: float
    type: str
    currency_value: float
    pair_currency_value: float
    fee: float
    taker: Optional[str]
    order_id: Optional[str]
    owner: Optional[str]

    def __str__(self):
        out = "\n"
        out += f"\t**{self.exchange.upper()} Transaction Id**: {self.id}"
        out += f"\t\t**Order Type**: {self.type}"
        out += f"\t\t**Amount**: {self.currency_value}"
        out += f"\t\t**Price**: {self.pair_currency_value}"
        out += f"\t\t**Market**: {self.market}"
        out += f"\t\t**Time**: {self.time}"
        return out


class LedgerTransaction(BaseModel):
    id: str
    time: float
    type: str
    subtype: str
    asset: str
    asset_class: str
    amount: float
    fee: float
    exchange: str
    resulting_balance: Optional[float]

    def __str__(self):
        out = "\n"
        out += f"\t**{self.exchange.upper()} Ledger Transaction Id**: {self.id}"
        out += f"\t\t**Ledger Type**: {self.type}"
        out += f"\t\t**Amount**: {self.amount}"
        out += f"\t\t**Fee**: {self.fee}"
        out += f"\t\t**Asset**: {self.asset}"
        out += f"\t\t**Asset Class**: {self.asset_class}"
        out += f"\t\t**Time**: {self.time}"
        return out


class Order(BaseModel):
    id: str
    amount: float
    status: str
    type: str
    market: str
    exchange: str
    transactions: List[Transaction] = []

    @ property
    def currency_balance(self):
        balance = 0.0
        for tx in self.transactions:
            balance += tx.currency_value
        return balance

    @ property
    def pair_currency_balance(self):
        balance = 0.0
        for tx in self.transactions:
            balance += tx.pair_currency_value
        return balance


class Trade(BaseModel, ABC):
    order_id: str
    order_type: str
    usd_observed: float

    @abstractmethod
    def compute_utility(self):
        pass
