"""Module containing the Standard Deviation function."""

from __future__ import annotations

from typing import Sequence

import numpy as np


__all__ = [
    # Function exports
    "stdev",
]


def stdev(series: Sequence[int | float], length: int) -> np.array:
    """Standard deviation.

    Arguments:
        series: Series of values to process.
        length: Number of bars (length).

    Raises:
        TypeError: Raised if `length` is not a number.

    Returns:
        Standard deviation.
    """

    # Make sure input series is a numpy array
    if not isinstance(series, np.ndarray):
        series = np.asarray(series)

    # Length should be a number
    if not isinstance(length, (float, int)):
        raise TypeError(f"length must be a number: {length}")

    # Make sure length is an integer
    length = int(length)

    # Return a list of np.nan if the length is 0, negative,
    # or larger than the length of the series
    if length > len(series) - 1 or length <= 0:
        processed_return = np.empty(series.shape)
        processed_return.fill(np.nan)
        return processed_return

    # Standard Deviation process
    stdev = np.empty(series.shape)
    for i in range(len(series)):
        subseries = series[i:i + length]

        if len(subseries) > (length - 1):
            stdev[i] = np.std(subseries)
        else:
            stdev[i] = np.nan

    return stdev
