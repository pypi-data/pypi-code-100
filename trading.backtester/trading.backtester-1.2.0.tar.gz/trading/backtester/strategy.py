"""Module containing the backtester strategy class."""

from __future__ import annotations

from trading.backtester import position as position_lib
from trading.backtester.config import AttrDict


__all__ = [
    # Class exports
    "BacktesterStrategy",
]


class BacktesterStrategy:
    """Base backtester strategy class.

    Arguments:
        backtester: An instance of the parent backtester.
        parameters: Strategy parameters that are used as overrides
            over the strategy parameters set in the parent backtester's
            internal configuration.
    """

    def __init__(
        self,
        backtester: Backtester,
        parameters: dict | AttrDict | None = None,
    ):

        """Creates an instance of a new Backtester strategy."""

        # Check if strategy parameters configuration is dictionary
        if parameters and not isinstance(parameters, AttrDict):
            raise TypeError(
                "strategy parameters configuration must be an AttrDict, "
                f"got {type(parameters)}")

        self._backtester = backtester
        self._parameters = (
            AttrDict(parameters) if parameters
            else self.config.strategy_parameters)

    def initialize(self):
        """Data initialization for the strategy.

        This function is where all the indicator data are calculated.
        Only runs once and it runs when the strategy class is
        initialized. Similar to how the `__init__` function works.

        The correct way of adding a new indicator is by creating a new
        attribute in the `self` variable. The value should be an
        instance of `pd.Series` which is usually the result of our
        TA functions.

        ```python
        from trading.backtester import ta

        self.ema50 = ta.ema(self.close, timeperiod=50)

        # Use `indicator_period` parameter from configuration
        self.another_indicator = ta.ema(self.close, timeperiod=self.p.period)
        ```

        This function can also be used to initialize new variables that
        can help the overall strategy.
        """

    def start(self):
        """Runs at the first period of each asset of a backtest run."""

    def end(self):
        """Runs at the last period of each asset of a backtest run."""

    def prenext(self):
        """Runs before the minimum indicator period is reached.

        See documentation for `bt.Backtester.minimum_indicator_period`
        for an explanation of what the minimum indicator period is.
        """

    def nextstart(self):
        """Runs when the minimum indicator period is reached.

        See documentation for `bt.Backtester.minimum_indicator_period`
        for an explanation of what the minimum indicator period is.
        """

    def next(self):
        """Runs after the minimum indicator period is reached.

        This is the main function of the strategy. The different order
        functions are used here to generate long or short signals.

        See documentation for `bt.Backtester.minimum_indicator_period`
        for an explanation of what the minimum indicator period is.
        """
        raise NotImplementedError

    def stop(self):
        """Runs at the last period of each asset of a backtest run."""

    def buy(
        self,
        order_id: str = "buy",
        limit: float | None = None,
        stop: float | None = None,
        amount: float | None = None,
        amount_percent: float | None = None,
        leverage: float = 1,
    ) -> Order:

        """Go long or reduce/close a short position."""
        return self.order(
            order_id, position_lib.LONG, limit=limit, stop=stop,
            amount=amount, amount_percent=amount_percent, leverage=leverage)

    def sell(
        self,
        order_id: str = "sell",
        limit: float | None = None,
        stop: float | None = None,
        amount: float | None = None,
        amount_percent: float | None = None,
        leverage: float = 1,
    ) -> Order:

        """Go short or reduce/close a long position."""
        return self.order(
            order_id, position_lib.SHORT, limit=limit, stop=stop,
            amount=amount, amount_percent=amount_percent, leverage=leverage)

    def order(
        self,
        order_id: str,
        position: str,
        limit: float | None = None,
        stop: float | None = None,
        amount: float | None = None,
        amount_percent: float | None = None,
        leverage: float = 1,
    ) -> Order:

        """Lower-level order creation function.

        See the documentation for `bt.BacktesterExchange.order()`
        for an explanation of what the different function arguments are.
        """
        return self.bt.exchange.order(
            order_id=order_id,
            position=position,
            limit=limit,
            stop=stop,
            amount=amount,
            amount_percent=amount_percent,
            leverage=leverage)

    def cancel_all(self):
        """Cancels all pending orders."""
        self.bt.exchange.cancel_all()

    def cancel(self, order_or_id : Order | str):
        """Cancels a pending order by referencing the order or its ID.

        See the documentation for `bt.BacktesterExchange.cancel()`
        for an explanation of what the different function arguments are.
        """
        self.bt.exchange.cancel(order_or_id)

    def exit_all(self):
        """Exits all trades."""
        self.bt.exchange.exit_all()

    def exit(self, order_id : str):
        """Exit a trade by referencing the order or its ID.

        See the documentation for `bt.BacktesterExchange.exit()`
        for an explanation of what the different function arguments are.
        """
        self.bt.exchange.exit(order_id=order_id)

    @property
    def bt(self) -> Backtester:
        """Shorthand for self.backtester."""
        return self._backtester

    @property
    def backtester(self) -> Backtester:
        return self._backtester

    @property
    def config(self) -> BacktesterConfig:
        return self.bt.config

    @property
    def p(self) -> AttrDict:
        """Shorthand for self.parameters."""
        return self.parameters

    @property
    def parameters(self) -> AttrDict:
        return self._parameters
