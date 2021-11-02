"""Tests for trading.backtester.ta.bbw."""

from numpy.testing import assert_almost_equal
import numpy as np
import pytest
import talib

from trading.backtester import ta


class TestBollingerBandsWidthFunction:

    def test_bbw_function_is_visible(self):
        assert not hasattr(talib, "BBW")
        assert hasattr(ta, "bbw")

    def test_bbw_set_arguments_to_non_numbers(self, mina_1w_series):
        with pytest.raises(TypeError):
            ta.bbw(mina_1w_series, "invalid length", 2)

        with pytest.raises(TypeError):
            ta.bbw(mina_1w_series, 9, "invalid mult")

    def test_bbw_set_arguments_to_9_2(self, mina_1w_series):
        expected_output = [
            0.727665680679024, 0.8163844747141804,
            np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan,
        ]

        assert_almost_equal(ta.bbw(mina_1w_series, 9, 2), expected_output)

    def test_bbw_set_length_to_large_number(self, mina_1w_series, all_nan):
        assert_almost_equal(ta.bbw(mina_1w_series, 999, 2), all_nan)

    def test_bbw_set_length_to_0(self, mina_1w_series, all_nan):
        assert_almost_equal(ta.bbw(mina_1w_series, 0, 2), all_nan)

    def test_bbw_set_length_to_negative_1(self, mina_1w_series, all_nan):
        assert_almost_equal(ta.bbw(mina_1w_series, -1, 2), all_nan)

    def test_bbw_set_mult_to_large_number(self, mina_1w_series):
        expected_output = [
            363.469007499172928, 407.78404511973928,
            np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan,
        ]

        assert_almost_equal(ta.bbw(mina_1w_series, 9, 999), expected_output)

    def test_bbw_set_mult_to_0(self, mina_1w_series, all_nan):
        assert_almost_equal(ta.bbw(mina_1w_series, 9, 0), all_nan)

    def test_bbw_set_mult_to_negative_1(self, mina_1w_series, all_nan):
        assert_almost_equal(ta.bbw(mina_1w_series, 9, -1), all_nan)
