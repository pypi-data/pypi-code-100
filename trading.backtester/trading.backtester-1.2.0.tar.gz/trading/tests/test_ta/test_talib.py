"""Tests for trading.backtester.ta.talib."""

from numpy.testing import assert_almost_equal
import numpy as np
import talib

from trading.backtester import ta


class TestTechnicalAnalysisLibraryFunctions:

    def test_atr_function_is_visible(self):
        assert hasattr(talib, "ATR")
        assert hasattr(ta, "atr")

    def test_bb_function_is_visible(self):
        assert hasattr(talib, "BBANDS")
        assert hasattr(ta, "bbands")
        assert hasattr(ta, "bb")

    def test_cci_function_is_visible(self):
        assert hasattr(talib, "CCI")
        assert hasattr(ta, "cci")

    def test_ema_function_is_visible(self):
        assert hasattr(talib, "EMA")
        assert hasattr(ta, "ema")

    def test_sma_function_is_visible(self):
        assert hasattr(talib, "SMA")
        assert hasattr(ta, "sma")

    def test_sma_set_length_to_9(self, mina_1w_series):
        expected_output = [
            4.215777777777777, 4.109444444444446,
            np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan,
        ]

        assert_almost_equal(ta.sma(mina_1w_series, 9), expected_output)

    def test_ema_set_length_to_9(self):
        input_series = [
            4285.08, 4108.37, 4139.98, 4086.29, 4016.00, 4040.00, 4114.01,
            4316.01, 4280.68, 4337.44, 4310.01, 4386.69, 4587.48, 4555.14,
            4724.89, 4834.91, 4472.14, 4509.08, 4100.11, 4366.47, 4619.77,
            4691.61, 4282.80, 4258.81, 4130.37, 4208.47, 4163.72, 3944.69,
            3189.02, 3700.00, 3714.95, 3699.99, 4035.01, 3910.04, 3900.00,
            3609.99, 3595.87, 3780.00, 3660.02, 3920.75, 3882.35, 4193.00,
            4174.50, 4174.69, 4378.51, 4378.48, 4380.00, 4310.00, 4208.59,
            4292.43,
        ]

        expected_output = [
            4159.1842, np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan, np.nan,
        ]

        assert_almost_equal(ta.ema(input_series, 50), expected_output)
