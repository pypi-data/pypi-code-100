"""Tests for trading.backtester.order."""

import pytest

import trading.backtester as bt


@pytest.fixture(name="exchange", scope="class")
def fixture_exchange(input_dict_config):
    backtester = bt.Backtester(input_dict_config)
    exchange = bt.exchange.BacktesterExchange(
        backtester,
        backtester.config.initial_balance,
        backtester.config.initial_balance_currency)

    # Simulate backtester data: add low, high, close, datetime
    # trading_symbol, and trading_signal_source property to exchange
    exchange.trading_symbol = "XBTUSD"
    exchange.signal_source_symbol = "BTC/USDT"

    exchange.datetime = ["2018-03-31 00:00:00", "2018-03-30 00:00:00"]
    exchange.high = [7223.36, 7292,43]
    exchange.low = [6777.00, 6600.10]
    exchange.close = [6923.91, 6840.23]

    return exchange


class TestBacktesterOrder:

    def test_constants(self):
        assert bt.order.LIMIT == "limit"
        assert bt.order.MARKET == "market"
        assert bt.order.STOP_LIMIT == "stop-limit"
        assert bt.order.STOP_MARKET == "stop-market"

    def test_order_set_position_to_unknown(self, exchange):
        with pytest.raises(ValueError):
            bt.order.Order(exchange, "order-id", "unknown-position")

    def test_order_use_amount_percent(self, exchange):
        order = bt.order.Order(
            exchange, "order-id", bt.position.LONG, amount_percent=0.5)

        assert order.amount == exchange.initial_balance / 2

    def test_order_set_amount_to_none(self, exchange):
        order = bt.order.Order(exchange, "order-id", bt.position.LONG)
        assert order.amount == exchange.initial_balance

    def test_order_set_limit_using_setter(self, exchange):
        order = bt.order.Order(exchange, "order-id", bt.position.LONG)
        order.limit = 1234
        assert order.limit == 1234

    def test_order_get_ordertype(self, exchange):
        assert bt.order.Order.get_ordertype(1234, None) == bt.order.LIMIT
        assert bt.order.Order.get_ordertype(None, None) == bt.order.MARKET
        assert bt.order.Order.get_ordertype(1234, 1234) == bt.order.STOP_LIMIT
        assert bt.order.Order.get_ordertype(None, 1234) == bt.order.STOP_MARKET

    def test_order_validate_amount_percent(self, exchange):
        # amount_percent must be between 0 and 100%
        with pytest.raises(ValueError):
            bt.order.Order.validate_amount_percent(-1)

        # amount_percent must be between 0 and 100%
        with pytest.raises(ValueError):
            bt.order.Order.validate_amount_percent(0)

        # amount_percent must be between 0 and 100%
        with pytest.raises(ValueError):
            bt.order.Order.validate_amount_percent(1.01)

        # amount_percent type is invalid
        with pytest.raises(ValueError):
            bt.order.Order.validate_amount_percent("invalid-value")

        try:
            bt.order.Order.validate_amount_percent(None)
        except ValueError:
            pytest.fail()

    def test_order_validate_amount(self, exchange):
        # amount must be positive
        with pytest.raises(ValueError):
            bt.order.Order.validate_amount(None, -1)

        # amount must be positive
        with pytest.raises(ValueError):
            bt.order.Order.validate_amount(None, 0)

        # amount type is invalid
        with pytest.raises(ValueError):
            bt.order.Order.validate_amount(None, "invalid-value")

        try:
            bt.order.Order.validate_amount(1, 1)
        except ValueError:
            pytest.fail()

        try:
            bt.order.Order.validate_amount(1, None)
        except ValueError:
            pytest.fail()

    def test_order_validate_limit(self, exchange):
        # limit must be positive
        with pytest.raises(ValueError):
            bt.order.Order.validate_limit(-1)

        # limit must be positive
        with pytest.raises(ValueError):
            bt.order.Order.validate_limit(0)

        # limit type is invalid
        with pytest.raises(ValueError):
            bt.order.Order.validate_limit("invalid-value")

        try:
            bt.order.Order.validate_limit(1234)
        except ValueError:
            pytest.fail()

    def test_order_validate_stop(self, exchange):
        # stop must be positive
        with pytest.raises(ValueError):
            bt.order.Order.validate_stop(-1)

        # stop must be positive
        with pytest.raises(ValueError):
            bt.order.Order.validate_stop(0)

        # stop type is invalid
        with pytest.raises(ValueError):
            bt.order.Order.validate_stop("invalid-value")

        try:
            bt.order.Order.validate_stop(1234)
        except ValueError:
            pytest.fail()
