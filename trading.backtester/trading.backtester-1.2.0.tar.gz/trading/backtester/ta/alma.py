"""Module containing the Arnaud Legoux Moving Average function."""

from __future__ import annotations

from typing import Sequence
import math

import numpy as np


__all__ = [
    # Function exports
    "alma",
]


def alma(
    series: Sequence[int | float],
    length: int,
    offset: int | float,
    sigma: int | float,
    floor: bool = False,
) -> np.array:

    """Arnaud Legoux Moving Average.

    Uses Gaussian distribution as weights for moving average.

    Arguments:
        series: Series of values to process.
        length: Number of bars (length).
        offset: Controls tradeoff between smoothness (closer to 1) and
            responsiveness (closer to 0).
        sigma: Changes the smoothness of ALMA. The larger sigma the
            smoother ALMA.
        floor: An optional parameter. Specifies whether the offset
            calculation is floored before ALMA is calculated. Default
            value is `False`.

    Raises:
        TypeError: Raised if `length` is not a number, or
            if `multi` is not a number, or `sigma` is not a number.

    Returns:
        Arnaud Legoux Moving Average.
    """

    # Make sure input series is a numpy array
    if not isinstance(series, np.ndarray):
        series = np.asarray(series)

    # Length should be a number
    if not isinstance(length, (float, int)):
        raise TypeError(f"length must be a number: {length}")

    # Offset should be a number
    if not isinstance(offset, (float, int)):
        raise TypeError(f"offset must be a number: {offset}")

    # Sigma should be a number
    if not isinstance(sigma, (float, int)):
        raise TypeError(f"sigma must be a number: {sigma}")

    # Make sure arguments are correct data types
    length = int(length)
    offset = float(offset)
    sigma = float(sigma)
    floor = bool(floor)

    # Return a list of np.nan if the length is 0, negative,
    # or larger than the length of the series
    if length > len(series) - 1 or length <= 0 or offset >= length:
        processed_return = np.empty(series.shape)
        processed_return.fill(np.nan)
        return processed_return

    m_fn = math.floor if floor else float
    m = m_fn(offset * (length - 1))
    s = length / sigma

    alma = np.empty(series.shape)

    for i in range(len(series)):
        subseries = series[i:]

        if len(subseries) > (length - 1):
            norm = 0.0
            _sum = 0.0

            for j in range(length):
                weight = math.exp(-1 * ((j - m) ** 2) / (2 * (s ** 2)))
                norm = norm + weight
                _sum = _sum + subseries[length - j - 1] * weight

            alma[i] = _sum / norm

        else:
            alma[i] = np.nan

    return alma
