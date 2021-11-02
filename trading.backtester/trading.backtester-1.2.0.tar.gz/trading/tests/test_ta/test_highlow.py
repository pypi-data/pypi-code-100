"""Tests for trading.backtester.ta.highlow."""

from numpy.testing import assert_almost_equal
import numpy as np
import pytest
import talib

from trading.backtester import ta


class TestHighestLowestFunctions:

    def test_highest_function_is_visible(self):
        assert not hasattr(talib, "HIGHEST")
        assert not hasattr(talib, "HIGH")
        assert hasattr(ta, "highest")

    def test_highest_set_length_to_non_number(self, mina_1w_series):
        with pytest.raises(TypeError):
            ta.highest(mina_1w_series, "invalid length")

    def test_highest_set_length_to_3(self, mina_1w_series):
        expected_output = [
            4.502, 4.502, 5.381, 5.381, 5.381,
            5.144, 4.247, 3.142, np.nan, np.nan
        ]

        assert_almost_equal(ta.highest(mina_1w_series, 3), expected_output)

    def test_highest_set_length_to_6(self, mina_1w_series):
        expected_output = [
            5.381, 5.381, 5.381, 5.381, 5.381,
            np.nan, np.nan, np.nan, np.nan, np.nan,
        ]

        assert_almost_equal(ta.highest(mina_1w_series, 6), expected_output)

    def test_highest_set_length_to_large_number(self, mina_1w_series, all_nan):
        assert_almost_equal(ta.highest(mina_1w_series, 99), all_nan)

    def test_highest_set_length_to_0(self, mina_1w_series, all_nan):
        assert_almost_equal(ta.highest(mina_1w_series, 0), all_nan)

    def test_highest_set_length_to_negative_1(self, mina_1w_series, all_nan):
        assert_almost_equal(ta.highest(mina_1w_series, -1), all_nan)

    def test_lowest_function_is_visible(self):
        assert not hasattr(talib, "LOWEST")
        assert not hasattr(talib, "LOW")
        assert hasattr(ta, "lowest")

    def test_lowest_set_length_to_non_number(self, mina_1w_series):
        with pytest.raises(TypeError):
            ta.lowest(mina_1w_series, "invalid length")

    def test_lowest_set_length_to_3(self, mina_1w_series):
        expected_output = [
            4.099, 4.157, 4.394, 4.394, 4.247,
            2.887, 2.887, 2.887, np.nan, np.nan
        ]

        assert_almost_equal(ta.lowest(mina_1w_series, 3), expected_output)

    def test_lowest_set_length_to_6(self, mina_1w_series):
        expected_output = [
            4.099, 4.157, 2.887, 2.887, 2.887,
            np.nan, np.nan, np.nan, np.nan, np.nan,
        ]

        assert_almost_equal(ta.lowest(mina_1w_series, 6), expected_output)

    def test_lowest_set_length_to_large_number(self, mina_1w_series, all_nan):
        assert_almost_equal(ta.lowest(mina_1w_series, 99), all_nan)

    def test_lowest_set_length_to_0(self, mina_1w_series, all_nan):
        assert_almost_equal(ta.lowest(mina_1w_series, 0), all_nan)

    def test_lowest_set_length_to_negative_1(self, mina_1w_series, all_nan):
        assert_almost_equal(ta.lowest(mina_1w_series, -1), all_nan)
