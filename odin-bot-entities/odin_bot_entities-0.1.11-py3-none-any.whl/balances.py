import time
from datetime import datetime
from typing import Dict, List
from pydantic import BaseModel

from .currencies import (
    CEROS,
    MINIMUM_TO_TRADE,
    COINS,
    RENAME_COINS_INV,
)


class Coin(BaseModel):
    name: str
    amount: float

    def __add__(self, other):
        amount = round(self.amount + other.amount, CEROS[self.name])
        return Coin(name=self.name, amount=amount)

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __rmul__(self, sign: int):
        return Coin(name=self.name, amount=self.amount * sign)

    def __abs__(self):
        return Coin(name=self.name, amount=abs(self.amount))


class Wallet(BaseModel):
    exchange: str
    coins: Dict[str, Coin]
    sign: int
    time: float
    date: datetime

    def __getitem__(self, standard_name: str):
        if standard_name in self.coins:
            return self.sign * self.coins[standard_name]
        else:
            coin = Coin(name=standard_name, amount=0.0)
            self.coins[standard_name] = coin
            return self.sign * self.coins[standard_name]

    def __str__(self):
        out = ""
        for coin in self.coins.values():
            out += f"\t\t **{coin.name}**: {coin.amount}"
        return out


class Balance(BaseModel):
    balance: Dict[str, Dict[str, float]]
    wallets: List[Wallet]
    time: float
    date: datetime
    name: str = "OdinBalance"

    @classmethod
    def from_wallets(cls, coin_names: List[str], wallets: List[Wallet]):
        try:
            balance_dict = {}
            for coin in coin_names:
                balance_dict[coin] = {}
                coin_balances = [wallet[coin] for wallet in wallets]
                absolute_balances = [abs(wallet[coin]) for wallet in wallets]
                total = sum(absolute_balances)
                diff = sum(coin_balances)
                balance_dict[coin]["Total"] = round(total.amount, CEROS[coin])
                balance_dict[coin]["Difference"] = round(
                    diff.amount, CEROS[coin])

            return cls(
                balance=balance_dict,
                time=time.time(),
                date=datetime.now(),
                wallets=wallets,
            )
        except Exception as err:
            logging.debug(err)
            raise err

    def __str__(self):
        out = ""
        for name, value in self.balance.items():
            out += f"\t**{name}**: {value}"

        return out

    def is_unbalanced(self, other_exchange: str) -> List[Coin]:
        try:
            non_stable_coins = {
                coin_name: amount
                for coin_name, amount in self.balance.items()
                if coin_name in COINS
            }

            unbalanced = dict(
                filter(
                    lambda elem: abs(elem[1])
                    > MINIMUM_TO_TRADE[other_exchange][
                        RENAME_COINS_INV[other_exchange][elem[0]]
                    ],
                    non_stable_coins.items(),
                )
            )
            out = ""
            for name, amount in unbalanced.items():
                out += f"\t\t **{name}**: __{amount}__"
            return out

        except Exception:
            return ""
