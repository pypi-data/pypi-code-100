"""
greenops
--------

Software to measure the footprints of deep learning models at training,
testing and evaluating to reduce energy consumption and carbon footprints.

Copyright rixel 2021
Distributed under the MIT License.
See accompanying file LICENSE.

File: submodule functions
"""


from numbers import Number


def extensionify_file(file_name : str, extension : str) -> str:
    """
    Add extension to the name of the file if needed
    ===============================================

    Parameters
    ----------
    file_name : str
        Name of the file.
    extension : str
        Extension to add if needed.

    Returns
    -------
        Name of the file with extension.
    """

    if file_name.split('.')[-1] != extension:
        result = '{}.{}'.format(file_name, extension)
    else:
        result = file_name
    return result


def join_any(delimiter : str, some_iterable : any) -> str:
    """
    Type agnostic solution for str.jon() functionality
    ==================================================

    Parameters
    ----------
    delimiter : str
        Basic string to join elements of list with.
    some_iterable : any
        Iterable to join together with the delimiter.

    Returns
    -------
    str
        String with the joined elements.

    Notes
    -----
        The function join_any(delimiter, some_iterable) is something like
        delimiter.join(list(some_iterable)) but some_iterable can contain
        any type of variables that implements the __str__() function.
    """

    result = ''
    len_some_iterable = len(some_iterable)
    if len_some_iterable > 0:
        result += str(some_iterable[0])
        pointer = 1
        while pointer < len_some_iterable:
            result += '{}{}'.format(delimiter, some_iterable[pointer])
            pointer += 1
    return result


def percentify(value : Number) -> str:
    """
    Transform value to percent
    ==========================

    Parameters
    ----------
    value : Number
        Value to transform.

    Returns
    -------
    str
        Value as percentage string. If the given parameter is not a number, the
        result is `0.00 %`.

    Notes
    -----
        However, function signature includes typing, type check is made to avoid
        run-time errors.
    """

    result = '0.00 %'
    if isinstance(value, Number):
        result = '{:.2f} %'.format(value * 100.0)
    return result


def ws_to_kwh(watt_seconds : Number) -> float:
    """
    Convert watt-second to kilowatt-hour
    ====================================

    Parameters
    ----------
    watt_seconds : Number
        Value in watt-sconds.

    Returns
    -------
    float
        Value in kilowatt-hours. If the given parameter is not a number, the
        result is zero.

    Notes
    -----
        However, function signature includes typing, type check is made to avoid
        run-time errors.
    """

    result = 0.0
    if isinstance(watt_seconds, Number):
        result = watt_seconds / 3600000
    return result
