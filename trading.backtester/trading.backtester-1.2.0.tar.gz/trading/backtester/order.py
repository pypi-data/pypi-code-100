"""Module containing order constants."""

from __future__ import annotations

from trading.backtester.position import is_valid_position
from trading.backtester.position import get_position_multiplier


__all__ = [
    # Constants export
    "LIMIT",
    "MARKET",
    "STOP_LIMIT",
    "STOP_MARKET",
]

LIMIT = "limit"
MARKET = "market"
STOP_LIMIT = "stop-limit"
STOP_MARKET = "stop-market"


class Order:

    def __init__(
        self,
        exchange: BacktesterExchange,
        order_id: str,
        position: str,
        limit: float | None = None,
        stop: float | None = None,
        amount: float | None = None,
        amount_percent: float | None = None,
        leverage: float = 1,
    ):

        # Set exchange and other related properties before validations
        self._exchange = exchange
        self._creation_datetime = self.exchange.datetime[0]
        self._trading_symbol = self.exchange.trading_symbol
        self._signal_source_symbol = self.exchange.signal_source_symbol

        # Make sure position is a valid value
        if not is_valid_position(position):
            raise ValueError(f"invalid position type: {position!r}")

        # Advance validation of other arguments
        self.validate_amount_percent(amount_percent)
        self.validate_amount(amount_percent, amount)
        self.validate_leverage(leverage)
        self.validate_limit(limit)
        self.validate_stop(stop)

        self._liquidated = False

        self._id = order_id
        self._position = position
        self._leverage = leverage
        self._limit = limit
        self._stop = stop

        # Automatically determine the actual order amount
        balance = self.exchange.asset[self.exchange.trading_symbol].balance
        if amount_percent:
            self._amount = balance * float(amount_percent)
        elif amount:
            self._amount = float(amount)
        else:
            self._amount = balance

        # Automatically determine the order type
        self._type = self.get_ordertype(limit, stop)

        # Auto-add this instance to the exchange
        self.exchange.asset[self.trading_symbol].pending_orders.append(self)

        # Set future possible properties
        self.close = None
        self.closing_timestamp = None
        self.execution_timestamp = None
        self.cancellation_timestamp = None

    def __repr__(self):
        properties = set([p.strip("_") for p in dir(self) if "__" not in p])
        properties = [p for p in properties if not callable(getattr(self, p))]
        properties = [p for p in properties if hasattr(self, p)]

        return (f"{self.__class__.__name__}(" +
                ", ".join([f"{p}={getattr(self, p)!r}" for p in properties]) +
                ")")

    def cancel(self):
        """Cancel the order."""
        self.cancellation_timestamp = self.exchange.datetime[0]
        self.exchange.asset[self.trading_symbol].pending_orders.remove(self)
        self.exchange.asset[self.trading_symbol].cancelled_orders.append(self)

    def execute(self):
        """Execute the order."""
        if self.limit is None or self.type == MARKET:
            self._limit = self.exchange.close[0]

        self.execution_timestamp = self.exchange.datetime[0]
        self.exchange.asset[self.trading_symbol].pending_orders.remove(self)
        self.exchange.asset[self.trading_symbol].open_trades.append(self)

    def liquidate(self):
        """Liquidate a trade."""
        self.liquidated = True
        self.exit()

    def exit(self):
        """Exit the trade."""
        self.close = self.exchange.close[0]
        self.closing_timestamp = self.exchange.datetime[0]
        self.exchange.asset[self.trading_symbol].open_trades.remove(self)
        self.exchange.asset[self.trading_symbol].closed_trades.append(self)

    def get_liquidation_price(self, mmr=0.02):
        imr = 1.0 / self.leverage * self.position_multiplier * -1
        mmr = mmr * self.position_multiplier

        return self.limit * (1 + imr + mmr)

    @staticmethod
    def get_ordertype(limit: float, stop: float) -> str:
        """Automatically determines the order type."""
        if limit is not None and stop is not None:
            return STOP_LIMIT
        if limit is None and stop is not None:
            return STOP_MARKET
        if limit is not None and stop is None:
            return LIMIT
        return MARKET

    @staticmethod
    def validate_amount_percent(amount_percent: float):
        """Checks if amount is a number and is between 0 to 100%"""
        if isinstance(amount_percent, (float, int)):
            if not(0 < amount_percent <= 1):
                raise ValueError(f"amount_percent must be between 0 and 100%")
        elif amount_percent is not None:
            raise ValueError(f"invalid amount_percent value: {amount_percent}")

    @staticmethod
    def validate_amount(amount_percent: float, amount: float):
        """Checks if amount is a number and positive."""
        if amount_percent is None and isinstance(amount, (float, int)):
            if amount <= 0:
                raise ValueError(f"amount must be a positive number: {amount}")
        elif amount_percent is None and amount is not None:
            raise ValueError(f"invalid amount value: {amount}")

    @staticmethod
    def validate_limit(limit: float):
        """Checks if limit price is a number and positive. """
        if isinstance(limit, (float, int)):
            if limit <= 0:
                raise ValueError(f"limit price must be positive: {limit}")
        elif limit is not None:
            raise ValueError(f"invalid limit price: {limit}")

    @staticmethod
    def validate_stop(stop: float):
        """Checks if stop price is a number and positive. """
        if isinstance(stop, (float, int)):
            if stop <= 0:
                raise ValueError(f"stop price must be positive: {stop}")
        elif stop is not None:
            raise ValueError(f"invalid stop price: {stop}")

    @staticmethod
    def validate_leverage(leverage: float):
        """Checks if leverage price is a number and positive. """
        if isinstance(leverage, (float, int)):
            if leverage <= 0:
                raise ValueError(f"leverage must be positive: {leverage}")
        else:
            raise ValueError(f"invalid leverage: {leverage}")

    def get_profit(
        self,
        exit_price: float,
        entry_price: float,
        qty: float,
        position: int,
    ) -> float:

        # multiplier = -1 if short position, 1 if long position
        # profit = exit price - entry price * qty * multiplier
        return float(
            (exit_price - entry_price) * qty * self.position_multiplier)

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def creation_datetime(self):
        return self._creation_datetime

    @property
    def exchange(self) -> BacktesterExchange:
        return self._exchange

    @property
    def id(self) -> str:
        return self._id

    @property
    def limit(self) -> float:
        return self._limit

    @limit.setter
    def limit(self, value: float):
        self._limit = value

    @property
    def leverage(self):
        return self._leverage

    @property
    def liquidated(self) -> float:
        return self._liquidated

    @liquidated.setter
    def liquidated(self, value: float):
        self._liquidated = value

    @property
    def netprofit(self) -> float:
        """Returns the net profits amount of this closed trade.

        If the trade is not yet closed - there's no closing price or
        closing timestamp set yet, then raise an error to the user.
        """
        if self.close is None or self.closing_timestamp is None:
            return 0.0

        return self.get_profit(self.close, self.limit, self.qty, self.position)

    @property
    def openprofit(self) -> float:
        """Returns the open profits amount of this open trade.

        If the trade is not yet executed, or the limit price is not
        yet set, the open profit is equal to zero.
        """
        if self.limit is None or self.execution_timestamp is None:
            return 0.0

        return self.get_profit(
            self.exchange.close[0], self.limit, self.qty, self.position)

    @property
    def position_multiplier(self) -> int:
        return get_position_multiplier(self.position)

    @property
    def position(self) -> str:
        return self._position

    @property
    def position_size(self) -> float:
        return abs(self.amount) * self.position_multiplier

    @property
    def qty(self) -> float | None:
        if self.limit is None:
            return None

        return float(self.amount / self.limit)

    @property
    def signal_source_symbol(self) -> str:
        return self._signal_source_symbol

    @property
    def stop(self) -> float:
        return self._stop

    @property
    def trading_symbol(self) -> str:
        return self._trading_symbol

    @property
    def type(self) -> str:
        return self._type
