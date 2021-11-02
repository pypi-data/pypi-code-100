"""Tests for trading.backtester.ta.stdev."""

from numpy.testing import assert_almost_equal
import numpy as np
import pytest
import talib

from trading.backtester import ta


class TestStandardDeviationFunction:

    def test_stdev_function_is_visible(self):
        assert not hasattr(talib, "STDEV")
        assert hasattr(ta, "stdev")

    def test_stdev_set_length_to_non_number(self, mina_1w_series):
        with pytest.raises(TypeError):
            ta.stdev(mina_1w_series, "invalid length")

    def test_stdev_set_length_to_9(self, mina_1w_series):
        expected_output = [
            0.7669192015645423, 0.8387216610362213,
            np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan,
        ]

        assert_almost_equal(ta.stdev(mina_1w_series, 9), expected_output)

    def test_stdev_set_length_to_large_number(self, mina_1w_series, all_nan):
        assert_almost_equal(ta.stdev(mina_1w_series, 999), all_nan)

    def test_stdev_set_length_to_0(self, mina_1w_series, all_nan):
        assert_almost_equal(ta.stdev(mina_1w_series, 0), all_nan)

    def test_stdev_set_length_to_negative_1(self, mina_1w_series, all_nan):
        assert_almost_equal(ta.stdev(mina_1w_series, -1), all_nan)
