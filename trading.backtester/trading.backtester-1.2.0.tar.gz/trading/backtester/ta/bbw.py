"""Module containing the Bollinger Bands Width function."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from trading.backtester.ta.talib import sma
from trading.backtester.ta.stdev import stdev


__all__ = [
    # Function exports
    "bbw",
]


def bbw(
    series: Sequence[int | float],
    length: int,
    mult: int | float,
) -> np.array:

    """Bollinger Bands Width.

    The Bollinger Band Width is the difference between the upper and
    the lower Bollinger Bands divided by the middle band.

    Arguments:
        series: Series of values to process.
        length: Number of bars (length).
        mult: Standard deviation factor.

    Raises:
        TypeError: Raised if `length` is not a number or
            if `multi` is not a number.

    Returns:
        Bollinger Bands Width.
    """

    # Make sure input series is a numpy array
    if not isinstance(series, np.ndarray):
        series = np.asarray(series)

    # Length should be a number
    if not isinstance(length, (float, int)):
        raise TypeError(f"length must be a number: {length}")

    # Multiplier should be a number
    if not isinstance(mult, (float, int)):
        raise TypeError(f"mult must be a number: {mult}")

    # Make sure arguments are correct data types
    length = int(length)
    mult = float(mult)

    # Return a list of np.nan if the length is 0, negative,
    # or larger than the length of the series
    if (length > len(series) - 1 or length <= 0) or mult <= 0:
        processed_return = np.empty(series.shape)
        processed_return.fill(np.nan)
        return processed_return

    # Bollinger Bands Width process
    basis = sma(series, length)
    dev = mult * stdev(series, length)

    return ((basis + dev) - (basis - dev)) / basis
