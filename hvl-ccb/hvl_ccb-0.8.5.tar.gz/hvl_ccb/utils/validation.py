#  Copyright (c) 2019-2021 ETH Zurich, SIS ID and HVL D-ITET
#
"""

"""
import logging
from logging import Logger
from typing import (
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

import numpy as np

from hvl_ccb.utils.typing import Number


def validate_number(
    x_name: str,
    x: object,
    limits: Optional[Tuple] = (None, None),
    number_type: Union[Type[Number], Tuple[Type[Number], ...]] = (int, float),
    logger: Optional[Logger] = None,
) -> None:
    """
    Validate if given input `x` is a number of given `number_type` type, with value
    between given `limits[0]` and `limits[1]` (inclusive), if not `None`.
    For array-like objects (npt.NDArray, List, Tuple, Dict) it is checked if all
    elements are within the limits and have the correct type.

    :param x_name: string name of the validate input, use for the error message
    :param x: an input object to validate as number of given type within given range
    :param logger: logger of the calling submodule
    :param limits: [lower, upper] limit, with `None` denoting no limit: [-inf, +inf]
    :param number_type: expected type or tuple of types of a number,
        by default `(int, float)`
    :raises TypeError: when the validated input does not have expected type
    :raises ValueError: when the validated input has correct number type but is not
        within given range
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    if limits is None:
        limits = (-np.inf, np.inf)
    if limits[0] is None:
        limits = (-np.inf, limits[1])
    if limits[1] is None:
        limits = (limits[0], np.inf)

    data_type = type(x)
    if not isinstance(number_type, Sequence):
        number_type = (number_type,)

    if isinstance(x, (float, int)):
        if not isinstance(x, number_type):
            msg = (
                f"{x_name} = {x} has to be of type "
                f"{' or '.join(nt.__name__ for nt in number_type)}"
            )
            logger.error(msg)
            raise TypeError(msg)
    elif isinstance(x, (list, tuple, dict, np.ndarray)):
        if isinstance(x, dict):
            x = np.asarray(list(x.values()))
        x = np.asarray(x)
        if x.dtype not in number_type:
            msg = (
                f"{x_name} = {x} needs to include only numbers type "
                f"{' or '.join(nt.__name__ for nt in number_type)}"
            )
            logger.error(msg)
            raise TypeError(msg)
    else:
        msg = (
            f"{x_name} = {x} must be an Integer, a Float, a Tuple, a List, "
            f"a Dictionary or a Numpy array, but the received type is {data_type}."
        )
        logger.error(msg)
        raise TypeError(msg)

    if np.any(x < limits[0]) or np.any(x > limits[1]):
        if np.isinf(limits[0]):
            suffix = f"less or equal than {limits[1]}"
        elif np.isinf(limits[1]):
            suffix = f"greater or equal than {limits[0]}"
        else:
            suffix = f"between {limits[0]} and {limits[1]} inclusive"
        msg = f"{x_name} = {x} has to be {suffix}"
        logger.error(msg)
        raise ValueError(msg)


def validate_bool(x_name: str, x: object, logger: Optional[Logger] = None) -> None:
    """
    Validate if given input `x` is a `bool`.

    :param x_name: string name of the validate input, use for the error message
    :param x: an input object to validate as boolean
    :param logger: logger of the calling submodule
    :raises TypeError: when the validated input does not have boolean type
    """
    if logger is None:
        logger = logging.getLogger(__name__)
    if not isinstance(x, bool):
        msg = f"{x_name} = {x} has to of type bool"
        logger.error(msg)
        raise TypeError(msg)
