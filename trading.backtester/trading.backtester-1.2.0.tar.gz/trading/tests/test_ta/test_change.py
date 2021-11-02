"""Tests for trading.backtester.ta.change."""

from numpy.testing import assert_almost_equal
import numpy as np
import pytest
import talib

from trading.backtester import ta


class TestSeriesChangeFunction:

    def test_change_function_is_visible(self):
        assert not hasattr(talib, "CHANGE")
        assert hasattr(ta, "change")

    def test_change_set_length_to_non_number(self, mina_1w_series):
        with pytest.raises(TypeError):
            ta.change(mina_1w_series, "invalid length")

    def test_change_set_length_to_default(self, mina_1w_series):
        expected_output = [
            -0.058, -0.345, 0.108, -0.987, 0.237,
            0.897, 1.36, -0.244, -0.011, np.nan,
        ]

        assert_almost_equal(ta.change(mina_1w_series), expected_output)

    def test_change_set_length_to_3(self, mina_1w_series):
        expected_output = [
            -0.295, -1.224, -0.642, 0.147, 2.494,
            2.013, 1.105, np.nan, np.nan, np.nan,
        ]

        assert_almost_equal(ta.change(mina_1w_series, 3), expected_output)

    def test_change_set_length_to_large_number(self, mina_1w_series, all_nan):
        assert_almost_equal(ta.change(mina_1w_series, 999), all_nan)

    def test_change_set_length_to_0(self, mina_1w_series, all_nan):
        assert_almost_equal(ta.change(mina_1w_series, 0), all_nan)

    def test_change_set_length_to_negative_1(self, mina_1w_series, all_nan):
        assert_almost_equal(ta.change(mina_1w_series, -1), all_nan)
