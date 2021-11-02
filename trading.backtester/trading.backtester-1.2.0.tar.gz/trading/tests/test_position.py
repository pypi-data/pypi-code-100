"""Tests for trading.backtester.position."""

import trading.backtester as bt


class TestBacktesterPosition:

    def test_constants(self):
        assert bt.position.LONG == "long"
        assert bt.position.SHORT == "short"

    def test_is_valid_position_true_cases(self):
        assert bt.position.is_valid_position("long")
        assert bt.position.is_valid_position("short")

    def test_is_valid_position_false_cases(self):
        assert not bt.position.is_valid_position("bilibili")
        assert not bt.position.is_valid_position("sell tayo")

    def test_get_position_multiplier(self):
        assert bt.position.get_position_multiplier("???") == 1
        assert bt.position.get_position_multiplier("long") == 1
        assert bt.position.get_position_multiplier("short") == -1
