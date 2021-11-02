"""Tests for trading.backtester.ta.alma."""

from numpy.testing import assert_almost_equal
import numpy as np
import pytest
import talib

from trading.backtester import ta


class TestArnaudLegouxMovingAverageFunction:

    def test_alma_function_is_visible(self):
        assert not hasattr(talib, "ALMA")
        assert hasattr(ta, "alma")

    def test_alma_set_length_to_non_number(self, mina_1w_series):
        with pytest.raises(TypeError):
            ta.alma(mina_1w_series, "invalid length", 0.85, 6)

    def test_alma_set_offset_to_non_number(self, mina_1w_series):
        with pytest.raises(TypeError):
            ta.alma(mina_1w_series, 9, "invalid offset", 6)

    def test_alma_set_sigma_to_non_number(self, mina_1w_series):
        with pytest.raises(TypeError):
            ta.alma(mina_1w_series, 9, 0.85, "invalid sigma")

    def test_alma_offset_set_to_true(self, mina_1w_series):
        expected_output = [
            4.347225720077040, 4.555227009878008,
            np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan,
        ]

        assert not hasattr(talib, "ALMA")
        assert hasattr(ta, "alma")
        assert_almost_equal(
            ta.alma(mina_1w_series, 9, 0.85, 6), expected_output)

    def test_alma_offset_set_to_false(self, mina_1w_series):
        expected_output = [
            4.475788383633046, 4.6778305216298905,
            np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan,
        ]

        assert not hasattr(talib, "ALMA")
        assert hasattr(ta, "alma")
        assert_almost_equal(
            ta.alma(mina_1w_series, 9, 0.85, 6, floor=True), expected_output)

    def test_alma_set_length_to_large_number(self, mina_1w_series, all_nan):
        assert_almost_equal(ta.alma(mina_1w_series, 999, 0.85, 6), all_nan)

    def test_alma_set_length_to_0(self, mina_1w_series, all_nan):
        assert_almost_equal(ta.alma(mina_1w_series, 0, 0.85, 6), all_nan)

    def test_alma_set_length_to_negative_1(self, mina_1w_series, all_nan):
        assert_almost_equal(ta.alma(mina_1w_series, -1, 0.85, 6), all_nan)

    def test_alma_set_offset_to_8(self, mina_1w_series):
        expected_output = [
            4.099000000000722, 4.15700000004288,
            np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan,
        ]

        assert_almost_equal(ta.alma(mina_1w_series, 9, 8, 6), expected_output)

    def test_alma_set_offset_to_large_number(self, mina_1w_series, all_nan):
        assert_almost_equal(ta.alma(mina_1w_series, 9, 999, 6), all_nan)

    def test_alma_set_offset_to_0(self, mina_1w_series):
        expected_output = [
            3.385409, 3.1849391,
            np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan,
        ]

        assert_almost_equal(ta.alma(mina_1w_series, 9, 0, 6), expected_output)

    def test_alma_set_offset_to_negative_1(self, mina_1w_series):
        expected_output = [
            3.1259176, 3.1416739,
            np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan,
        ]

        assert_almost_equal(ta.alma(mina_1w_series, 9, -1, 6), expected_output)
