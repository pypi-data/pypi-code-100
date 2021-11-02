"""Module containing the backtester exchange class."""

from __future__ import annotations

import pandas as pd
import trading.datasets_core as tdc

from trading.backtester import order as order_lib
from trading.backtester import position as position_lib
from trading.backtester.config import AttrDict
from trading.backtester.exceptions import InsufficientBalanceError


__all__ = [
    # Class exports
    "BacktesterExchange",
]


class BacktesterExchange:
    """Exchange/Broker abstraction for the backtester.

    This represents a hyper exchange that can download any data from any
    real exchange and it also contains all the balance, orders, trades,
    and positions information.

    Arguments:
        backtester: An instance of the parent backtester.
        initial_balance: Initial balance of the exchange when
            the instance is created.
        currency: Determines the quote currency of the balance.

    """

    ACCOUNT_COLUMNS = [
        "balance",
        "equity",
        "position_size",
    ]

    def __init__(
        self,
        backtester: Backtester,
        initial_balance: int | float = 100_000,
        currency: str = "USD",
    ):

        """Create an new exchange instance."""
        self._backtester = backtester
        self._initial_balance = float(initial_balance)
        self._currency = str(currency)
        self._asset = {}

        # Prepare accounting variables
        self.initialize_asset_accounts()
        self.initialize_order_tracking()

        # Load OHLCV datasets
        self._fetch_ohlcv()

    def reset(self):
        self.__init__(self.backtester, self._initial_balance, self.currency)

    def initialize_asset_accounts(self):
        """Prepares all the accounting variables."""

        # Prepare financials historical variable
        self._financials = pd.DataFrame(columns=self.ACCOUNT_COLUMNS)

        # Set per-asset accounting variables
        for asset in self.bt.config.assets:
            self._asset[asset.trading_symbol] = AttrDict()
            self._asset[asset.trading_symbol].balance = self.initial_balance
            self._asset[asset.trading_symbol].equity = self.initial_balance
            self._asset[asset.trading_symbol].position_size = 0

            # Prepare per-asset historical variables
            self._asset[asset.trading_symbol].financials = pd.DataFrame(
                columns=self.ACCOUNT_COLUMNS)

            # Divide the balance for each asset if `shared_balance`
            # in the backtester configuration is set to `False`
            if not self.bt.config.shared_balance:
                self._asset[asset.trading_symbol].balance *= asset.allocation
                self._asset[asset.trading_symbol].equity *= asset.allocation

    def initialize_order_tracking(self):
        """Prepares all the order and trade tracking variables."""

        # Set per-asset accounting variables
        for asset in self.bt.config.assets:
            self._asset[asset.trading_symbol].open_trades = []
            self._asset[asset.trading_symbol].closed_trades = []
            self._asset[asset.trading_symbol].pending_orders = []
            self._asset[asset.trading_symbol].cancelled_orders = []

    def start(self):
        """Runs at the first period of each asset of a backtest run."""

    def end_period(self):
        self.update_equity()
        self.update_position_size()
        self.update_financials()

    def end_asset(self):
        """Runs at the last period of each asset of a backtest run."""

    def end_run(self):
        """Runs at the end of the backtest run."""

    def next_preprocess(self):
        """Runs before the start of `bt.BacktesterStrategy.next()`."""

    def next_postprocess(self):
        """Runs after every end of `bt.BacktesterStrategy.next()`."""
        for pending_order in self.asset[self.trading_symbol].pending_orders:
            if pending_order.type == order_lib.MARKET:
                pending_order.execute()

            elif pending_order.type == order_lib.LIMIT:
                if ((pending_order.position == position_lib.LONG and
                     pending_order.limit <= self.high[0]) or
                    (pending_order.position == position_lib.SHORT and
                     pending_order.limit >= self.low[0])
                ):
                    pending_order.execute()

        for open_trade in self.asset[self.trading_symbol].open_trades:
            if open_trade.leverage == 1:
                continue

            if ((pending_order.position == position_lib.LONG and
                 pending_order.get_liquidation_price() >= self.low[0]) or
                (pending_order.position == position_lib.SHORT and
                 pending_order.get_liquidation_price() <= self.high[0])
            ):
                open_trade.liquidate()

    def update_equity(self):
        """Updates the equity variables."""

        # Add current wallet balance for the asset
        self._asset[self.trading_symbol].equity = (
            self.asset[self.trading_symbol].balance)

        # Add pending order values into the equity
        for pending_order in self.asset[self.trading_symbol].pending_orders:
            self._asset[self.trading_symbol].equity += pending_order.amount

        # Add open trades values into the equity
        for open_trade in self.asset[self.trading_symbol].open_trades:
            self._asset[self.trading_symbol].equity += (
                open_trade.openprofit + open_trade.amount)

    def update_position_size(self):
        """Updates the position size variables."""

        self._asset[self.trading_symbol].position_size = 0

        # Add open trades values into the position size
        for open_trade in self.asset[self.trading_symbol].open_trades:
            self._asset[self.trading_symbol].position_size += (
                open_trade.position_size)

    def update_financials(self):
        """Add current per-asset accounting variables to history."""
        timestamp = self.datetime[0]

        for column in self.ACCOUNT_COLUMNS:
            # Record value to asset account history
            self._asset[self.trading_symbol].financials.at[timestamp, column] = (
                self.asset[self.trading_symbol][column])

            # Check for whether or not there's a cell value then
            # record/add column value to financials account history
            if (timestamp not in self._financials.index or
                pd.isna(self._financials.loc[timestamp, column])
            ):
                self._financials.at[timestamp, column] = (
                    self.asset[self.trading_symbol][column])
            else:
                self._financials.at[timestamp, column] += (
                    self.asset[self.trading_symbol][column])

    def order(
        self,
        order_id: str,
        position: str,
        limit: float | None = None,
        stop: float | None = None,
        amount: float | None = None,
        amount_percent: float | None = None,
        leverage: float = 1,
    ) -> order_lib.Order:

        """Create an order.

        The value of `limit` and `stop` determines the order type:
        - both `limit` and `stop` prices are not provided for market orders
        - both `limit` and `stop` prices are provided for stop-limit orders
        - just `limit is provided for limit orders
        - just `stop is provided for stop orders

        Arguments:
            order_id: The order identifier. It is possible to cancel
                or modify an order by referencing its identifier.
            position: 'long' is for buy, 'short' is for sell.
            limit: Optional order limit price .
            stop: Optional order stop price.
            amount: Optional absolute order amount.
            amount_percent: Optional order amount in percentage. This
                argument takes precedence over the `amount` parameter.
                If both are not provided, the order will use the
                available wallet balance.
            leverage: Leverage of the order.

        Raises:
            ValueError: Raised when the input position type is not
                found in the list of valid values. Check out
                `bt.position.VALID_POSITION_TYPES` for the valid values.
            InsufficientBalanceError: Raised when the remaining wallet
                balance in the exchange is no longer enough to create
                an order.
            ValueError: Raised when number arguments are negative
                numbers or zero.

        Return:
            The created order instance. This is only for the user's
            copy. The order returned is automatically added to the
            exchange's record of pending orders.
        """

        order = order_lib.Order(
            exchange=self,
            order_id=order_id,
            position=position,
            limit=limit,
            stop=stop,
            amount=amount,
            amount_percent=amount_percent,
            leverage=leverage,
        )

        # Make sure we still have enough balance in the
        # exchange for the specified order amount
        if order.amount > self.asset[self.trading_symbol].balance:
            raise InsufficientBalanceError(
                f"balance reached {self.asset[self.trading_symbol].balance} "
                f"after creating order: {order}")

        self.asset[self.trading_symbol].balance -= order.amount

        return order

    def cancel_all(self):
        """Cancel all pending orders."""
        self.cancel(None)

    def cancel(self, order_id: str):
        """Cancel an order with the specified ID.

        Arguments:
            order_id: The order identifier. It is possible to cancel
                or modify an order by referencing its identifier.
        """
        for pending_order in self.asset[self.trading_symbol].pending_orders:
            if pending_order.id == order_id or order_id is None:
                pending_order.cancel()

                self.asset[self.trading_symbol].balance += pending_order.amount

    def exit_all(self):
        """Exit/close all open trades."""
        self.exit(None)

    def exit(self, order_id: str):
        """Exit/close a trade with the specified ID.

        Arguments:
            order_id: The order identifier. It is possible to cancel
                or modify an order by referencing its identifier.
        """
        for open_trade in self.asset[self.trading_symbol].open_trades:
            if open_trade.id == order_id or order_id is None:
                open_trade.exit()

                self.asset[self.trading_symbol].balance += (
                    open_trade.netprofit + open_trade.amount)

    # TODO: Refactor
    def _fetch_ohlcv(self) -> dict[str, pd.DataFrame]:  # pragma: no cover
        """Needs improvement: Currently just using Datasets Core."""

        self._data = {}

        for asset in self.bt.config.assets:
            # Create a dynamic starting datetime based on the assumption
            # the max strategy parameter is the minimum indicator period
            diff = tdc.Timeframe(asset.signal_timeframe).to_timedelta()
            diff *= self.bt.minimum_indicator_period
            start = self.bt.config.starting_timestamp
            start = tdc.utils.datetime_utils.to_datetime(start) - diff

            exchange = tdc.exchange.get(asset.signal_source_exchange)
            ohlcv = pd.DataFrame(exchange.fetch_ohlcv(
                symbol=asset.signal_source_symbol,
                timeframe=asset.signal_timeframe,
                end=self.bt.config.ending_timestamp,
                start=start,
            ))

            # Preprocess the columns and index of the dataframe return
            ohlcv.columns = [
                "datetime", "open", "high", "low", "close", "volume"
            ]

            ohlcv["datetime"] = pd.to_datetime(
                ohlcv["datetime"], unit="ms", utc=True)

            ohlcv.set_index("datetime", inplace=True)
            ohlcv.sort_index(inplace=True)

            # Download collateral
            vsymbol = exchange.get_valid_symbol(asset.signal_source_symbol)
            quote_currency = exchange.markets[vsymbol]["quote"]

            invert = False
            if "USD" in quote_currency:
                quote_currency = "USD"
                invert = True

            if quote_currency == self.currency:
                ohlcv["conversion"] = 1
            else:
                if invert:
                    collateral_symbol = f"{self.currency}{quote_currency}"
                else:
                    collateral_symbol = f"{quote_currency}{self.currency}"
                conversion_ohlcv = pd.DataFrame(exchange.fetch_ohlcv(
                    symbol=collateral_symbol,
                    timeframe=asset.signal_timeframe,
                    end=self.bt.config.ending_timestamp,
                    start=start,
                ))

                # Preprocess the columns and index of the dataframe return
                conversion_ohlcv.columns = [
                    "datetime", "open", "high", "low", "close", "volume"
                ]

                conversion_ohlcv["datetime"] = pd.to_datetime(
                    conversion_ohlcv["datetime"], unit="ms", utc=True)

                conversion_ohlcv.set_index("datetime", inplace=True)
                conversion_ohlcv.sort_index(inplace=True)

                if invert:
                    ohlcv["conversion"] = 1 / conversion_ohlcv["close"]
                else:
                    ohlcv["conversion"] = conversion_ohlcv["close"]

            self._data[asset.signal_source_symbol] = ohlcv

    @property
    def financials(self):
        return self._financials

    @property
    def asset(self) -> dict[str, AttrDict]:
        return self._asset

    @property
    def bt(self) -> Backtester:
        """Shorthand for self.backtester."""
        return self.backtester

    @property
    def backtester(self) -> Backtester:
        return self._backtester

    @property
    def currency(self) -> str:
        return self._currency

    @property
    def data(self) -> str:
        return self._data

    @property
    def initial_balance(self) -> float:
        return self._initial_balance
