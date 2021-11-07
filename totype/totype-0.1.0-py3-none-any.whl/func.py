import datetime as dt
import re
from functools import partial
from importlib.util import find_spec
from typing import Any, Union, Callable, List, Dict, Optional

from totype.annotation_types import (
    OldValueT,
    NewValueT,
    OldStringT,
    NewStringT,
    StrOrDatetime,
)


def _get_utc():
    if find_spec("zoneinfo"):
        from zoneinfo import ZoneInfo

        return ZoneInfo("UTC")

    elif find_spec("pendulum"):
        import pendulum

        return pendulum.UTC

    elif find_spec("pytz"):
        import pytz

        return pytz.UTC

    else:
        raise ImportError("'pytz' or 'pendulum' packages are required")


def _get_tz(tz_name: Optional[str]):
    if tz_name is None:
        return None

    elif find_spec("zoneinfo"):
        from zoneinfo import ZoneInfo

        return ZoneInfo(tz_name)

    elif find_spec("pendulum"):
        import pendulum

        return pendulum.timezone(tz_name)

    elif find_spec("pytz"):
        import pytz

        return pytz.timezone(tz_name)

    else:
        raise ImportError("'pytz' or 'pendulum' packages are required")


def set_args_to_func(func: Callable, **kwargs) -> Callable:
    return partial(func, **kwargs)


class FunctionSet:
    def __init__(self, *funcs: Callable):
        self.funcs = list(funcs)

    def add_func(self, func: Callable, **kwargs):
        self.funcs.append(set_args_to_func(func, **kwargs))

    def add_funcs(self, *funcs: Callable):
        self.funcs += funcs

    def __call__(self, value: Any):
        for func in self.funcs:
            value = func(value)

        return value


def json_loads(value: Union[str, bytes, list, dict]) -> Any:
    if isinstance(value, (list, dict)):
        return value

    if find_spec("orjson"):
        import orjson

        loads_func = orjson.loads

    elif find_spec("ujson"):
        import ujson

        loads_func = ujson.loads

    elif find_spec("simplejson"):
        import simplejson

        loads_func = simplejson.loads

    else:
        import json

        loads_func = json.loads

    return loads_func(value)


def deserialize_not_valid_list(value: Union[str, bytes, list]) -> list:
    def _parse(x: str):
        x = re.sub(r"^\[", "", x)
        x = re.sub(r"\]$", "", x)
        x = x.replace("\\'", "'")
        # This lexer takes a JSON-like 'array' string and converts
        # single-quoted array items into escaped double-quoted items,
        # then puts the 'array' into a python list
        # Issues such as  ["item 1", '","item 2 including those double quotes":"',
        # "item 3"] are resolved with this lexer
        items = []  # List of lexed items
        item = ""  # Current item container
        dq = True  # Double-quotes active (False->single quotes active)
        bs = 0  # backslash counter
        # True if currently lexing an item within the quotes
        # (False if outside the quotes; ie comma and whitespace)
        in_item = False
        for i, c in enumerate(x):  # Assuming encasement by brackets
            if c == "\\":
                # if there are backslashes, count them! Odd numbers escape the quotes...
                bs += 1
                continue
            if ((dq and c == '"') or (not dq and c == "'")) and (
                not in_item or i + 1 == len(x) or x[i + 1] == ","
            ):  # quote matched at start/end of an item
                if (
                    bs & 1 == 1
                ):  # if escaped quote, ignore as it must be part of the item
                    continue
                else:  # not escaped quote - toggle in_item
                    in_item = not in_item
                    if item != "":  # if item not empty, we must be at the end
                        items += [item]  # so add it to the list of items
                        item = ""  # and reset for the next item
                    else:
                        if not in_item:
                            items.append("")
                    continue
            if not in_item:  # toggle of single/double quotes to enclose items
                if dq and c == "'":
                    dq = False
                    in_item = True
                elif not dq and c == '"':
                    dq = True
                    in_item = True
                continue
            if in_item:  # character is part of an item, append it to the item
                if not dq and c == '"':  # if we are using single quotes
                    item += bs * "\\" + '"'  # escape double quotes for JSON
                else:
                    item += bs * "\\" + c
                bs = 0
                continue
        return items

    if isinstance(value, list):
        return value

    try:
        return json_loads(value)
    except ValueError:
        return _parse(str(value))


def apply_array(array: Union[list, tuple], funcs: List[Callable]):
    for i, value in enumerate(array):
        for func in funcs:
            array[i] = func(value)

    return array


def apply_array_array(
    array_array: Union[list, tuple],
    funcs: List[Callable],
    depth: int = 1,
    replace_no_valid_array_array: bool = True,
):
    for i, arr in enumerate(array_array):
        if not isinstance(arr, (tuple, list)):
            if replace_no_valid_array_array:
                array_array[i] = []
            else:
                raise TypeError(f"Expected array, received {type(arr)}")
        elif depth - 1 > 1:
            array_array[i] = apply_array_array(arr, funcs, depth - 1)
        else:
            array_array[i] = apply_array(arr, funcs)

    return array_array


def datetime_parse(value: StrOrDatetime) -> dt.datetime:
    if isinstance(value, (dt.datetime, dt.date)):
        return value

    elif find_spec("dateutil"):
        from dateutil import parser

        return parser.parse(value)

    elif find_spec("pendulum"):
        import pendulum

        return pendulum.parse(value)

    else:
        raise ImportError("'pendulum' or 'dateutil' packages are required")


def datetime_fromisoformat(value: StrOrDatetime) -> dt.datetime:
    if isinstance(value, (dt.datetime, dt.date)):
        return value

    return dt.datetime.fromisoformat(value)


def datetime_strptime(value: StrOrDatetime, /, fmt: str) -> dt.datetime:
    if isinstance(value, (dt.datetime, dt.date)):
        return value

    return dt.datetime.strptime(value, fmt)


def datetime_strftime(value: Union[dt.datetime, dt.date], /, fmt: str) -> str:
    return value.strftime(fmt)


def datetime_to_date(value: dt.datetime) -> dt.date:
    return value.date()


def date_to_datetime(value: dt.date) -> dt.datetime:
    value = dt.datetime.fromisoformat(value.isoformat())
    return value


def timestamp_to_datetime(
    value: Union[str, float, int], tz_name: Optional[str] = None
) -> dt.datetime:
    value = float(value)
    value = dt.datetime.fromtimestamp(value, tz=_get_utc())
    return datetime_replace_tz(value, tz_name)


def datetime_to_timestamp(value: dt.datetime) -> float:
    return value.timestamp()


def to_uint(value: Any) -> int:
    value = int(value)
    if value < 0:
        raise ValueError(f"{value} less than 0")
    return value


def datetime_replace_tz(value: dt.datetime, tz_name: str) -> dt.datetime:
    return value.replace(tzinfo=_get_tz(tz_name))


def datetime_astimezone(value: dt.datetime, /, tz_name: str) -> dt.datetime:
    return value.astimezone(tz=_get_tz(tz_name))


def replace_values(value: Any, mapping: Dict[OldValueT, NewValueT]) -> Any:
    for old, new in mapping.items():
        if value == old:
            return new
    return value


def replace_str(
    value: str, mapping: Dict[OldStringT, NewStringT], count: int = ...
) -> str:
    for old, new in mapping.items():
        value = value.replace(old, new, count=count)

    return value
