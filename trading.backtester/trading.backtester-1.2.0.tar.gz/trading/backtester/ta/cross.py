"""Module containing a variety of cross functions."""

from __future__ import annotations

from typing import Sequence

import numpy as np


__all__ = [
    # Function exports
    "cross",
    "crossover",
    "crossunder",
]


def cross(
    series_1: Sequence[int | float],
    series_2: Sequence[int | float]
) -> bool:

    """Checks if a cross between two series occured.

    Arguments:
        series_1: First data series.
        series_2: Second data series.

    Returns:
        `True` if two series have crossed each other, otherwise `False`.
    """
    if not isinstance(series_1, np.ndarray):
        series_1 = np.asarray(series_1)

    if not isinstance(series_2, np.ndarray):
        series_2 = np.asarray(series_2)

    return crossover(series_1, series_2) or crossunder(series_1, series_2)


def crossover(
    series_1: Sequence[int | float],
    series_2: Sequence[int | float]
) -> bool:

    """Checks if `series_1` crossed over `series_2`.

    The `series_1`-series is defined as having crossed over
    `series_2`-series if, on index-0, the value of `series_1` is
    greater than the value of `series_2`, and on index-1, the value
    of `series_1` was less than the value of `series_2`.

    Arguments:
        series_1: First data series.
        series_2: Second data series.

    Returns:
        `True` if `series_1` crossed over `series_2` otherwise `False`.
    """
    if not isinstance(series_1, np.ndarray):
        series_1 = np.asarray(series_1)

    if not isinstance(series_2, np.ndarray):
        series_2 = np.asarray(series_2)

    return series_1[0] > series_2[0] and series_1[1] < series_2[1]


def crossunder(
    series_1: Sequence[int | float],
    series_2: Sequence[int | float]
) -> bool:

    """Checks if `series_1` crossed under `series_2`.

    The `series_1`-series is defined as having crossed under
    `series_2`-series if, on index-0, the value of `series_2` is
    greater than the value of `series_1`, and on index-1, the value
    of `series_2` was less than the value of `series_1`.

    Arguments:
        series_1: First data series.
        series_2: Second data series.

    Returns:
        `True` if `series_1` crossed under `series_2` otherwise `False`.
    """
    if not isinstance(series_1, np.ndarray):
        series_1 = np.asarray(series_1)

    if not isinstance(series_2, np.ndarray):
        series_2 = np.asarray(series_2)

    return series_1[0] < series_2[0] and series_1[1] > series_2[1]
