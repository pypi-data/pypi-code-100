"""Module containing the backtester class."""

from __future__ import annotations

from math import ceil
import inspect

import numpy as np
import pandas as pd

from trading.backtester.config import BacktesterConfig
from trading.backtester.exchange import BacktesterExchange
from trading.backtester.metrics import Metrics
from trading.backtester.strategy import BacktesterStrategy


__all__ = [
    # Class exports
    "Backtester",
]


class Backtester:
    """Base backtester class."""

    def __init__(self, config: dict | str | BacktesterConfig):
        """Create a new backtester instance."""
        self._config = BacktesterConfig.load(config)
        self._exchange = BacktesterExchange(
            backtester=self,
            initial_balance=self.config.initial_balance,
            currency=self.config.initial_balance_currency)

        self._strat_class = None
        self._strat = None

        self._metrics = Metrics(self)

    def run(self):
        """The core method to perform backtesting."""
        if self.strategy is None:
            raise ValueError("strategy is not set")

        if self.exchange.data is None:
            raise ValueError("data is not set")  # pragma: no cover

        for asset in self.config.assets:
            data = self.exchange.data[asset.signal_source_symbol]

            # Add current asset to the exchange
            setattr(self._exchange, "trading_symbol", asset.trading_symbol)
            setattr(self._exchange, "signal_source_symbol",
                asset.signal_source_symbol)

            # Add data columns to strategy for initialization function
            for column in data.columns:
                setattr(self._strat, column, data[column])

            # Remember old attributes and then get the new attributes
            # all the newly added Series datasets should be added
            # manually to the data attribute
            old_attributes = dir(self._strat)
            self._strat.initialize()
            new_attributes = list(set(dir(self._strat)) - set(old_attributes))

            # Filter new data by its type, only process pd.Series types
            for new_attribute in new_attributes[:]:
                trading_view_data = getattr(self._strat, new_attribute)

                if isinstance(trading_view_data, (pd.Series, np.ndarray)):
                    filter_series = np.isnan(trading_view_data)
                    trading_view_data = trading_view_data[~filter_series]
                    trading_view_data = np.pad(
                        trading_view_data,
                        ((len(data.index) - len(trading_view_data)), 0),
                        mode="constant",
                        constant_values=(np.nan,))

                    data[new_attribute] = trading_view_data
                else:
                    new_attributes.remove(new_attribute)

            for i, _ in enumerate(data.index):
                # Add the same Trading View-like data but for the index
                setattr(
                    self._exchange,
                    data.index.name,
                    data.index[:(i + 1)][::-1])

                # Create a Trading View-like data object and assign
                # it to the strategy object for Trader's use
                for column in data.columns:
                    padded_data = data[column][:(i + 1)][::-1]
                    padded_data = padded_data.astype(np.float64)
                    padded_data = np.pad(
                        padded_data,
                        (0, self.minimum_indicator_period),
                        mode="constant",
                        constant_values=(np.nan,))

                    setattr(self._strat, column, padded_data)
                    setattr(self._exchange, column, padded_data)

                setattr(
                    self._strat,
                    "position_size",
                    (
                        [self.exchange.asset[asset.trading_symbol].position_size]
                        if hasattr(self.exchange.asset[asset.trading_symbol], "position_size")
                        else [0] * self.minimum_indicator_period
                    )
                )

                # Very first period
                if i == 0:
                    self.exchange.start()
                    self.strategy.start()

                # Run next for the rest of the whole backtest
                if i > self.minimum_indicator_period:
                    self.exchange.next_preprocess()
                    self.strategy.next()
                    self.exchange.next_postprocess()

                # Run prenext if we"re still warming up
                elif i < self.minimum_indicator_period:
                    self.strategy.prenext()

                # Run nextstart if we just finished warming up
                else:
                    self.exchange.next_preprocess()
                    self.strategy.nextstart()
                    self.strategy.next()
                    self.exchange.next_postprocess()

                self.exchange.end_period()

            # Ending function calls
            self.strategy.end()
            self.exchange.end_asset()

            # Cleanup the added attributes for the next symbol
            for new_attribute in new_attributes:
                delattr(self._strat, new_attribute)

        # Last function call
        self.exchange.end_run()

    def set_strategy(
        self,
        strategy: BacktesterStrategy,
        parameters: dict | None = None,
    ):

        """Sets the strategy to be used by the Backtester.

        Arguments:
            strategy: A subclass of the `bt.BacktesterStrategy` class.
            parameters: A dictionary containing a set of strategy
                parameters. If the configuration given to the Backtester
                already has a set of parameters and the user still
                entered another set of parameters in this function,
                the latter is the one we would use.

        Raises:
            ValueError: Raised when the strategy is not a subclass of
                `bt.BacktesterStrategy`, is not a class at all, or if
                the input strategy is already an instance.

        """
        if not inspect.isclass(strategy):
            raise ValueError(f"input strategy is not a class: {strategy}")

        if (not issubclass(strategy, BacktesterStrategy) or
            strategy == BacktesterStrategy
        ):
            raise ValueError(f"not a strategy subclass: {type(strategy)}")

        # Try to get the parameters from the configuration if not given
        if not parameters:
            parameters = self.config.strategy_parameters
        else:
            parameters = AttrDict(parameters)

        self._strat_class = strategy
        self._strat = strategy(self, parameters=parameters)

    @property
    def config(self) -> BacktesterConfig:
        return self._config

    @property
    def exchange(self) -> BacktesterExchange:
        return self._exchange

    @property
    def metrics(self):
        return self._metrics

    @property
    def minimum_indicator_period(self) -> int:
        """Minimum number of periods for indicator warmup.

        There are different indicators used in a strategy and some of
        these indicators have different required number of periods
        before they can be used. The largest required indicator period
        is called the "minimum indicator period".

        For Example, our strategy uses this list of indicators:
        - EMA 200 (required number of periods is 200)
        - SMA 50 (required number of periods is 50)
        - RSI 14 (required number of periods is 14)

        So for this strategy, the minimum indicator period is 200 since
        that's the largest required indicator period. If there's no
        strategy parameters, the minimum indicator period is 0.
        """
        try:
            return int(ceil(max(self.config.strategy_parameters.values())) - 1)
        except (AttributeError, ValueError, TypeError):
            return 0

    @property
    def strategy(self) -> BacktesterStrategy:
        """The strategy to be used for the backtester.

        To set the strategy properly, use `Backtester.set_strategy()`.
        """
        return self._strat

    from trading.backtester.visuals import visualize
