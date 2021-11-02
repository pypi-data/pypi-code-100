"""Module containing highest and lowest functions."""

from __future__ import annotations

from typing import Sequence

import numpy as np


__all__ = [
    # Function exports
    "highest",
    "lowest",
]


def highest(series: Sequence[int | float], length: int) -> np.array:
    """Highest value for a given number of bars back.

    Arguments:
        series: Series of values to process.
        length: Optional parameter. Number of bars (length).

    Raises:
        TypeError: Raised if `length` is not a number.

    Returns:
        Highest value in the series.
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

    # Highest Bar process
    highest = np.empty(series.shape)
    for i in range(len(series)):
        subseries = series[i:i + length]

        if len(subseries) > (length - 1):
            highest[i] = np.max(subseries)
        else:
            highest[i] = np.nan

    return highest


def lowest(series: Sequence[int | float], length: int) -> np.array:
    """Lowest value for a given number of bars back.

    Arguments:
        series: Series of values to process.
        length: Optional parameter. Number of bars (length).

    Raises:
        TypeError: Raised if `length` is not a number.

    Returns:
        Lowest value in the series.
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

    # Lowest Bar process
    lowest = np.empty(series.shape)
    for i in range(len(series)):
        subseries = series[i:i + length]

        if len(subseries) > (length - 1):
            lowest[i] = np.min(subseries)
        else:
            lowest[i] = np.nan

    return lowest
