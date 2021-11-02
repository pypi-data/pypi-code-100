"""Module containing the Series change function."""

from __future__ import annotations

from typing import Sequence

import numpy as np


__all__ = [
    # Function exports
    "change",
]


def change(series: Sequence[int | float], length: int = 1) -> np.array:
    """Difference between current value and previous.

    Arguments:
        series: Series of values to process.
        length: Optional parameter. Number of bars (length).

    Raises:
        TypeError: Raised if `length` is provided but is not a number.

    Returns:
        The result of subtraction.
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

    else:
        shifted_series = series[length:]
        processed_return = series[:len(shifted_series)] - shifted_series

    return np.pad(
        processed_return, (0, (len(series) - len(processed_return))),
        mode="constant", constant_values=(np.nan,))
