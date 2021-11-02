"""Module containing wrapped functions from TA-lib."""

from __future__ import annotations

from typing import Callable

import numpy as np
import talib


__all__ = []

DUPLICATE_NAME_MAPPING = {
    "bbands": "bb",
}


def get_wrapped_talib_function(fn: Callable) -> Callable:
    """Wraps a TA-lib function to reverse and pad the return."""

    def wrapped_talib_function(*args, **kwargs) -> np.array:
        # Preprocess list and tuple inputs as numpy arrays
        preprocessed_args = []
        for arg in args:
            if isinstance(arg, (tuple, list)):
                preprocessed_args.append(np.asarray(arg))
            else:
                preprocessed_args.append(arg)

        raw_return = fn(*preprocessed_args, **kwargs)

        processed_return = raw_return[~np.isnan(raw_return)]
        processed_return = np.pad(
            processed_return, (0, (len(raw_return) - len(processed_return))),
            mode="constant", constant_values=(np.nan,))

        return processed_return

    return wrapped_talib_function


# Dynamically export the TA-lib functions as lowercased functions
for function_name in talib.__dict__["__TA_FUNCTION_NAMES__"]:

    # Get function from TA-lib library
    lowercase_function_name = function_name.lower()
    talib_function = getattr(talib, function_name)
    talib_function = get_wrapped_talib_function(talib_function)

    # Export as lowercased function name
    # Add function name to import * as well
    globals()[lowercase_function_name] = talib_function
    __all__.append(lowercase_function_name)

    # Apply other-name copy if there's any
    try:
        function_copy_name = DUPLICATE_NAME_MAPPING[lowercase_function_name]
        globals()[function_copy_name] = talib_function
        __all__.append(function_copy_name)

    except KeyError:
        pass
