"""Tests for trading.backtester.ta.cross."""

import numpy as np
import pandas as pd
import talib

from trading.backtester import ta


class TestCrossFunctions:

    def test_crossover_function_is_visible(self):
        assert not hasattr(talib, "CROSSOVER")
        assert hasattr(ta, "crossover")

    def test_crossover_true_cases(self):
        assert ta.crossover((2, 1), [1, 3])
        assert ta.crossover([10, 6, 5, 5], [7, 8, 5, 2])
        assert ta.crossover([19, 7, 7, 8], pd.Series([9, 8, 7, 5]))
        assert ta.crossover(np.asarray([19, 7, 7, 8]), (9, 8, 7, 5))

    def test_crossover_false_cases(self):
        assert not ta.crossover([1, 2], [3, 1])
        assert not ta.crossover([7, 8, 5, 2], (10, 6, 5, 5))
        assert not ta.crossover([9, 11, 7, 5], pd.Series([19, 8, 7, 8]))
        assert not ta.crossover(np.asarray([9, 11, 7, 5]), [19, 8, 7, 8])

    def test_crossunder_function_is_visible(self):
        assert not hasattr(talib, "CROSSUNDER")
        assert hasattr(ta, "crossunder")

    def test_crossunder_true_cases(self):
        assert ta.crossunder([1, 2], [3, 1])
        assert ta.crossunder([7, 8, 5, 2], (10, 6, 5, 5))
        assert ta.crossunder([9, 11, 7, 5], pd.Series([19, 8, 7, 8]))
        assert ta.crossunder(np.asarray([9, 11, 7, 5]), [19, 8, 7, 8])

    def test_crossunder_false_cases(self):
        assert not ta.crossunder((2, 1), [1, 3])
        assert not ta.crossunder([10, 6, 5, 5], [7, 8, 5, 2])
        assert not ta.crossunder([19, 7, 7, 8], pd.Series([9, 8, 7, 5]))
        assert not ta.crossunder(np.asarray([19, 7, 7, 8]), (9, 8, 7, 5))

    def test_cross_function_is_visible(self):
        assert not hasattr(talib, "CROSS")
        assert hasattr(ta, "cross")

    def test_cross_true_cases(self):
        assert ta.cross((2, 1), [1, 3])
        assert ta.cross([1, 2], [3, 1])
        assert ta.cross([10, 6, 5, 5], [7, 8, 5, 2])
        assert ta.cross([7, 8, 5, 2], (10, 6, 5, 5))
        assert ta.cross([19, 7, 7, 8], pd.Series([9, 8, 7, 5]))
        assert ta.cross(np.asarray([19, 7, 7, 8]), (9, 8, 7, 5))
        assert ta.cross([9, 11, 7, 5], pd.Series([19, 8, 7, 8]))
        assert ta.cross(np.asarray([9, 11, 7, 5]), [19, 8, 7, 8])

    def test_cross_false_cases(self):
        assert not ta.cross((2, 1), [3, 2])
        assert not ta.cross([1, 2], [2, 3])
        assert not ta.cross([10, 6, 5, 5], [11, 8, 6, 7])
        assert not ta.cross([7, 8, 5, 2], (10, 9, 6, 5))
        assert not ta.cross([19, 7, 7, 8], pd.Series([29, 8, 9, 9]))
