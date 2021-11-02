"""Test fixtures for trading.backtester.ta."""

import numpy as np
import pytest


@pytest.fixture(name="mina_1w_series", scope="package")
def fixture_mina_1w_series():
    # This is the close data for MINA token using the 1w timeframe
    # data is from October 11, 2021 (index-0) to  August 9, 2021 (last)
    return [
        4.099, 4.157, 4.502, 4.394, 5.381,
        5.144, 4.247, 2.887, 3.131, 3.142,
    ]


@pytest.fixture(name="all_nan", scope="package")
def fixture_all_nan():
    return [
        np.nan, np.nan, np.nan, np.nan, np.nan,
        np.nan, np.nan, np.nan, np.nan, np.nan,
    ]


@pytest.fixture(name="all_zero", scope="package")
def fixture_all_zero():
    return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
