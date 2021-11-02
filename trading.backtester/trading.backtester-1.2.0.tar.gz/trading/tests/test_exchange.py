"""Tests for trading.backtester.exchange."""

from numpy.testing import assert_almost_equal
import pytest

import trading.backtester as bt


@pytest.fixture(name="exchange", scope="class")
def fixture_exchange(input_dict_config):
    backtester = bt.Backtester(input_dict_config)
    exchange = bt.exchange.BacktesterExchange(
        backtester,
        backtester.config.initial_balance,
        backtester.config.initial_balance_currency)

    return exchange


class TestBacktesterExchange:

    def test_exchange_init(self, exchange):
        # Instance is already created in the fixture
        assert isinstance(exchange, bt.exchange.BacktesterExchange)

    def test_exchange_accounting_variables(self, exchange):
        assert_almost_equal(exchange.asset["ADAUSD"].balance, 53.0091)
        assert_almost_equal(exchange.asset["ADAUSD"].equity, 53.0091)
        assert_almost_equal(exchange.asset["ADAUSD"].position_size, 0)

        assert_almost_equal(exchange.asset["XBTUSD"].balance, 53.0091)
        assert_almost_equal(exchange.asset["XBTUSD"].equity, 53.0091)
        assert_almost_equal(exchange.asset["XBTUSD"].position_size, 0)

    def test_exchange_not_shared_balance_init(self, golden_cross_input_config):
        backtester = bt.Backtester(golden_cross_input_config)
        exchange = bt.exchange.BacktesterExchange(
            backtester,
            backtester.config.initial_balance,
            backtester.config.initial_balance_currency)

        assert_almost_equal(exchange.asset["XBTUSD"].balance, 100000)
        assert_almost_equal(exchange.asset["XBTUSD"].equity, 100000)
        assert_almost_equal(exchange.asset["XBTUSD"].position_size, 0)

    def test_exchange_order_and_trade_tracking(self, exchange):
        assert exchange.asset["ADAUSD"].open_trades == []
        assert exchange.asset["ADAUSD"].closed_trades == []
        assert exchange.asset["ADAUSD"].pending_orders == []
        assert exchange.asset["ADAUSD"].cancelled_orders == []

        assert exchange.asset["XBTUSD"].open_trades == []
        assert exchange.asset["XBTUSD"].closed_trades == []
        assert exchange.asset["XBTUSD"].pending_orders == []
        assert exchange.asset["XBTUSD"].cancelled_orders == []

    def test_exchange_properties(self, exchange):
        assert isinstance(exchange.bt, bt.Backtester)
        assert isinstance(exchange.backtester, bt.Backtester)
        assert isinstance(exchange.initial_balance, float)
        assert isinstance(exchange.currency, str)

        assert exchange.initial_balance == 53.0091
        assert exchange.currency == "BTC"

    def test_exchange_insufficient_balance_order(self, exchange):
        # Simulate backtester data: add low, high, close, datetime
        # trading_symbol, and trading_signal_source property to exchange
        exchange.trading_symbol = "XBTUSD"
        exchange.signal_source_symbol = "BTC/USDT"

        exchange.datetime = ["2018-03-31 00:00:00", "2018-03-30 00:00:00"]
        exchange.high = [7223.36, 7292,43]
        exchange.low = [6777.00, 6600.10]
        exchange.close = [6923.91, 6840.23]

        with pytest.raises(bt.InsufficientBalanceError):
            exchange.order("buy", bt.position.LONG, amount=999999999)

    def test_exchange_next_postprocess_tradingview_btcusd(
        self, golden_cross_input_config
    ):

        """Golden Cross Strategy Test Case

        Backtester Configuration:
            Start Time: 2018-03-04 00:00:00
            End Time: 2018-04-09 00:00:00
            Stating Balance: 100,000
            Signal Source Symbol:
                - BTC/USDT
            Signal Source Exchange: Binance
            Timeframe: 1d
            Indicators:
                - Fast MA: SMA(50)
                - Slow MA: SMA(200)

        Pine Script Equivalent Code:

        ```pinescript
        //@version=5
        strategy("Golden Cross", process_orders_on_close=true)

        fast_ma = ta.sma(close, 50)
        slow_ma = ta.sma(close, 200)

        if ta.crossover(fast_ma, slow_ma)
            strategy.close("short")
            strategy.entry("long", strategy.long)

        if ta.crossunder(fast_ma, slow_ma)
            strategy.close("long")
            strategy.entry("short", strategy.short)
        ```
        """

        backtester = bt.Backtester(golden_cross_input_config)
        exchange = bt.exchange.BacktesterExchange(
            backtester,
            backtester.config.initial_balance,
            backtester.config.initial_balance_currency)

        # Simulate backtester data: add low, high, close, datetime
        # trading_symbol, and trading_signal_source property to exchange
        exchange.trading_symbol = "XBTUSD"
        exchange.signal_source_symbol = "BTC/USDT"

        # ______________________________________________________________
        # ==============================================================

        exchange.datetime = ["2018-03-31 00:00:00", "2018-03-30 00:00:00"]
        exchange.high = [7223.36, 7292,43]
        exchange.low = [6777.00, 6600.10]
        exchange.close = [6923.91, 6840.23]

        order = exchange.order("sell", bt.position.SHORT, amount=6923.91)

        assert len(exchange.asset["XBTUSD"].open_trades) == 0
        assert len(exchange.asset["XBTUSD"].closed_trades) == 0
        assert len(exchange.asset["XBTUSD"].pending_orders) == 1
        assert len(exchange.asset["XBTUSD"].cancelled_orders) == 0

        assert order in exchange.asset["XBTUSD"].pending_orders

        exchange.next_postprocess()
        exchange.end_period()

        assert len(exchange.asset["XBTUSD"].open_trades) == 1
        assert len(exchange.asset["XBTUSD"].closed_trades) == 0
        assert len(exchange.asset["XBTUSD"].pending_orders) == 0
        assert len(exchange.asset["XBTUSD"].cancelled_orders) == 0

        assert order in exchange.asset["XBTUSD"].open_trades

        assert_almost_equal(exchange.asset["XBTUSD"].balance, 93076.09)
        assert_almost_equal(exchange.asset["XBTUSD"].equity, 100000.0)
        assert_almost_equal(exchange.asset["XBTUSD"].position_size, -6923.91)

        # ______________________________________________________________
        # ==============================================================

        exchange.datetime = ["2018-04-01 00:00:00", "2018-03-31 00:00:00"]
        exchange.high = [7049.98, 7223.36]
        exchange.low = [6430.00, 6777.00]
        exchange.close = [6813.01, 6923.91]

        exchange.next_postprocess()
        exchange.end_period()

        assert_almost_equal(exchange.asset["XBTUSD"].balance, 93076.09)
        assert_almost_equal(exchange.asset["XBTUSD"].equity, 100110.9)
        assert_almost_equal(exchange.asset["XBTUSD"].position_size, -6923.91)

        # ______________________________________________________________
        # ==============================================================

        exchange.datetime = ["2018-04-02 00:00:00", "2018-04-01 00:00:00"]
        exchange.high = [7125.00, 7049.98]
        exchange.low = [6765.00, 6430.00]
        exchange.close = [7056.00, 6813.01]

        exchange.next_postprocess()
        exchange.end_period()

        assert_almost_equal(exchange.asset["XBTUSD"].balance, 93076.09)
        assert_almost_equal(exchange.asset["XBTUSD"].equity, 99867.91)
        assert_almost_equal(exchange.asset["XBTUSD"].position_size, -6923.91)

        # ______________________________________________________________
        # ==============================================================

        exchange.datetime = ["2018-06-28 00:00:00", "2018-06-27 00:00:00"]
        exchange.high = [6173.01, 6190.43]
        exchange.low = [5827.00, 5971.00]
        exchange.close = [5853.98, 6133.73]

        exchange.next_postprocess()
        exchange.end_period()

        assert_almost_equal(exchange.asset["XBTUSD"].balance, 93076.09)
        assert_almost_equal(exchange.asset["XBTUSD"].equity, 101069.93)
        assert_almost_equal(exchange.asset["XBTUSD"].position_size, -6923.91)

        # ______________________________________________________________
        # ==============================================================

        exchange.datetime = ["2019-04-23 00:00:00", "2019-04-22 00:00:00"]
        exchange.high = [5600.00, 5400.00]
        exchange.low = [5332.41, 5208.35]
        exchange.close = [5493.31, 5357.14]

        exchange.next_postprocess()
        exchange.end_period()

        assert_almost_equal(exchange.asset["XBTUSD"].balance, 93076.09)
        assert_almost_equal(exchange.asset["XBTUSD"].equity, 101430.60)
        assert_almost_equal(exchange.asset["XBTUSD"].position_size, -6923.91)

        # ______________________________________________________________
        # ==============================================================

        exchange.datetime = ["2019-04-24 00:00:00", "2019-04-23 00:00:00"]
        exchange.high = [5582.20, 5600.00]
        exchange.low = [5333.35, 5332.41]
        exchange.close = [5415.00, 5493.31]

        assert len(exchange.asset["XBTUSD"].open_trades) == 1
        assert len(exchange.asset["XBTUSD"].closed_trades) == 0
        assert len(exchange.asset["XBTUSD"].pending_orders) == 0
        assert len(exchange.asset["XBTUSD"].cancelled_orders) == 0

        exchange.exit("sell")

        assert len(exchange.asset["XBTUSD"].open_trades) == 0
        assert len(exchange.asset["XBTUSD"].closed_trades) == 1
        assert len(exchange.asset["XBTUSD"].pending_orders) == 0
        assert len(exchange.asset["XBTUSD"].cancelled_orders) == 0

        assert_almost_equal(exchange.asset["XBTUSD"].balance, 101508.91)
        assert_almost_equal(exchange.asset["XBTUSD"].position_size, -6923.91)

        order = exchange.order("buy", bt.position.LONG, amount=5415.00)

        assert len(exchange.asset["XBTUSD"].open_trades) == 0
        assert len(exchange.asset["XBTUSD"].closed_trades) == 1
        assert len(exchange.asset["XBTUSD"].pending_orders) == 1
        assert len(exchange.asset["XBTUSD"].cancelled_orders) == 0

        assert order in exchange.asset["XBTUSD"].pending_orders

        exchange.next_postprocess()
        exchange.end_period()

        assert len(exchange.asset["XBTUSD"].open_trades) == 1
        assert len(exchange.asset["XBTUSD"].closed_trades) == 1
        assert len(exchange.asset["XBTUSD"].pending_orders) == 0
        assert len(exchange.asset["XBTUSD"].cancelled_orders) == 0

        assert order in exchange.asset["XBTUSD"].open_trades

        assert_almost_equal(exchange.asset["XBTUSD"].balance, 96093.91)
        assert_almost_equal(exchange.asset["XBTUSD"].equity, 101508.91)
        assert_almost_equal(exchange.asset["XBTUSD"].position_size, 5415.00)

        # ______________________________________________________________
        # ==============================================================

        exchange.datetime = ["2019-06-26 00:00:00", "2019-06-25 00:00:00"]
        exchange.high = [13970.00, 11850.00]
        exchange.low = [11741.00, 11026.00]
        exchange.close = [13093.80, 11820.86]

        exchange.next_postprocess()
        exchange.end_period()

        assert_almost_equal(exchange.asset["XBTUSD"].balance, 96093.91)
        assert_almost_equal(exchange.asset["XBTUSD"].equity, 109187.71)
        assert_almost_equal(exchange.asset["XBTUSD"].position_size, 5415.00)

        # ______________________________________________________________
        # ==============================================================

        exchange.datetime = ["2019-10-26 00:00:00", "2019-10-25 00:00:00"]
        exchange.high = [10370.00, 8799.00]
        exchange.low = [8470.38, 7361.00]
        exchange.close = [9230.00, 8655.02]

        assert len(exchange.asset["XBTUSD"].open_trades) == 1
        assert len(exchange.asset["XBTUSD"].closed_trades) == 1
        assert len(exchange.asset["XBTUSD"].pending_orders) == 0
        assert len(exchange.asset["XBTUSD"].cancelled_orders) == 0

        exchange.exit("buy")

        assert len(exchange.asset["XBTUSD"].open_trades) == 0
        assert len(exchange.asset["XBTUSD"].closed_trades) == 2
        assert len(exchange.asset["XBTUSD"].pending_orders) == 0
        assert len(exchange.asset["XBTUSD"].cancelled_orders) == 0

        assert_almost_equal(exchange.asset["XBTUSD"].balance, 105323.91)
        assert_almost_equal(exchange.asset["XBTUSD"].position_size, 5415.00)

        order = exchange.order("sell", bt.position.SHORT, amount=9230.00)

        assert len(exchange.asset["XBTUSD"].open_trades) == 0
        assert len(exchange.asset["XBTUSD"].closed_trades) == 2
        assert len(exchange.asset["XBTUSD"].pending_orders) == 1
        assert len(exchange.asset["XBTUSD"].cancelled_orders) == 0

        assert order in exchange.asset["XBTUSD"].pending_orders

        exchange.next_postprocess()
        exchange.end_period()

        assert len(exchange.asset["XBTUSD"].open_trades) == 1
        assert len(exchange.asset["XBTUSD"].closed_trades) == 2
        assert len(exchange.asset["XBTUSD"].pending_orders) == 0
        assert len(exchange.asset["XBTUSD"].cancelled_orders) == 0

        assert order in exchange.asset["XBTUSD"].open_trades

        assert_almost_equal(exchange.asset["XBTUSD"].balance, 96093.91)
        assert_almost_equal(exchange.asset["XBTUSD"].equity, 105323.91)
        assert_almost_equal(exchange.asset["XBTUSD"].position_size, -9230.00)

        # ______________________________________________________________
        # ==============================================================

        exchange.datetime = ["2019-10-27 00:00:00", "2019-10-26 00:00:00"]
        exchange.high = [9794.98, 13970.00]
        exchange.low = [9074.34, 11741.00]
        exchange.close = [9529.93, 13093.80]

        exchange.next_postprocess()
        exchange.end_period()

        assert_almost_equal(exchange.asset["XBTUSD"].balance, 96093.91)
        assert_almost_equal(exchange.asset["XBTUSD"].equity, 105023.98)
        assert_almost_equal(exchange.asset["XBTUSD"].position_size, -9230.00)

        # ______________________________________________________________
        # ==============================================================

        exchange.datetime = ["2020-02-17 00:00:00", "2020-02-16 00:00:00"]
        exchange.high = [9964.16, 10050.00]
        exchange.low = [9452.67, 9638.12]
        exchange.close = [9706.00, 9917.27]

        assert len(exchange.asset["XBTUSD"].open_trades) == 1
        assert len(exchange.asset["XBTUSD"].closed_trades) == 2
        assert len(exchange.asset["XBTUSD"].pending_orders) == 0
        assert len(exchange.asset["XBTUSD"].cancelled_orders) == 0

        order = exchange.order(
            "buy", bt.position.LONG, amount=10164.71, limit=10164.71)

        assert len(exchange.asset["XBTUSD"].open_trades) == 1
        assert len(exchange.asset["XBTUSD"].closed_trades) == 2
        assert len(exchange.asset["XBTUSD"].pending_orders) == 1
        assert len(exchange.asset["XBTUSD"].cancelled_orders) == 0

        assert order in exchange.asset["XBTUSD"].pending_orders

        assert_almost_equal(exchange.asset["XBTUSD"].balance, 85929.20)
        assert_almost_equal(exchange.asset["XBTUSD"].equity, 105023.98)
        assert_almost_equal(exchange.asset["XBTUSD"].position_size, -9230.00)

        exchange.next_postprocess()
        exchange.end_period()

        assert len(exchange.asset["XBTUSD"].open_trades) == 1
        assert len(exchange.asset["XBTUSD"].closed_trades) == 2
        assert len(exchange.asset["XBTUSD"].pending_orders) == 1
        assert len(exchange.asset["XBTUSD"].cancelled_orders) == 0

        assert order in exchange.asset["XBTUSD"].pending_orders

        assert_almost_equal(exchange.asset["XBTUSD"].balance, 85929.20)
        assert_almost_equal(exchange.asset["XBTUSD"].equity, 104847.91)
        assert_almost_equal(exchange.asset["XBTUSD"].position_size, -9230.00)

        # ______________________________________________________________
        # ==============================================================

        exchange.datetime = ["2020-02-18 00:00:00", "2020-02-17 00:00:00"]
        exchange.high = [10250.00, 9964.16]
        exchange.low = [9576.01, 9452.67]
        exchange.close = [10164.71, 9706.00]

        assert len(exchange.asset["XBTUSD"].open_trades) == 1
        assert len(exchange.asset["XBTUSD"].closed_trades) == 2
        assert len(exchange.asset["XBTUSD"].pending_orders) == 1
        assert len(exchange.asset["XBTUSD"].cancelled_orders) == 0

        exchange.exit("sell")

        assert len(exchange.asset["XBTUSD"].open_trades) == 0
        assert len(exchange.asset["XBTUSD"].closed_trades) == 3
        assert len(exchange.asset["XBTUSD"].pending_orders) == 1
        assert len(exchange.asset["XBTUSD"].cancelled_orders) == 0

        exchange.next_postprocess()
        exchange.end_period()

        assert len(exchange.asset["XBTUSD"].open_trades) == 1
        assert len(exchange.asset["XBTUSD"].closed_trades) == 3
        assert len(exchange.asset["XBTUSD"].pending_orders) == 0
        assert len(exchange.asset["XBTUSD"].cancelled_orders) == 0

        assert order in exchange.asset["XBTUSD"].open_trades

        assert_almost_equal(exchange.asset["XBTUSD"].balance, 94224.49)
        assert_almost_equal(exchange.asset["XBTUSD"].equity, 104389.20)
        assert_almost_equal(exchange.asset["XBTUSD"].position_size, 10164.71)
