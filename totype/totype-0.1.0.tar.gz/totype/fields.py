import datetime as dt
from typing import Any, Callable, Optional, Dict, List, Tuple, Union

from totype import func
from totype.annotation_types import OldValueT, NewValueT, ErrorPolicyLiteralT
from totype.exceptions import TransformError
from totype.func import FunctionSet

NOT_RAISE_ERROR_FOR_VALUES = {
    None,
    "",
    "--",
    " --",
    "null",
    "Null",
    "NULL",
    "none",
    "None",
    "NONE",
    "NaN",
    "nan",
}


def _functionset_from(transform_funcs):
    if isinstance(transform_funcs, list):
        return FunctionSet(*transform_funcs)

    elif isinstance(transform_funcs, FunctionSet):
        return transform_funcs

    return FunctionSet()


class Field:
    def __init__(
        self,
        name: str = None,
        errors: ErrorPolicyLiteralT = "default",
        default_value: Any = None,
        transform_funcs: Union[List[Callable], FunctionSet] = None,
        clear_values: Optional[set] = None,
        map_replace_values: Optional[Dict[OldValueT, NewValueT]] = None,
    ):
        self.name = name
        self.errors = errors
        self.default_value = default_value
        self.func = FunctionSet()

        map_replace_values = map_replace_values or {}
        for v in clear_values or []:
            map_replace_values[v] = default_value

        if map_replace_values:
            self.func.add_func(func.replace_values, mapping=map_replace_values)

        self.func.add_func(_functionset_from(transform_funcs))

    def _process_error(self, value: Any, exception) -> Any:
        if self.errors == "default":
            return self.default_value

        elif self.errors == "ignore":
            return value

        raise TransformError(self, value, exception)

    def __call__(self, value: Any, /) -> Tuple[bool, Any]:
        try:
            value = self.func(value)
        except Exception as exc:
            if value in NOT_RAISE_ERROR_FOR_VALUES:
                valid = True
                value = self.default_value
            else:
                valid = False
                value = self._process_error(value, exc)
        else:
            valid = True

        return valid, value

    def __str__(self):
        return self.name

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"name={self.name}, "
            f'errors="{self.errors}", '
            f"default_value={self.default_value},...)"
        ).replace(" '\n ", " ")


class IntField(Field):
    def __init__(
        self,
        name: str = None,
        errors: ErrorPolicyLiteralT = "default",
        default_value: Any = 0,
        transform_funcs: Union[List[Callable], FunctionSet] = None,
        clear_values: set = None,
        map_replace_values: Dict[OldValueT, NewValueT] = None,
    ):
        _functions = FunctionSet(int)
        _functions.add_func(_functionset_from(transform_funcs))

        super().__init__(
            name=name,
            errors=errors,
            default_value=default_value,
            transform_funcs=_functions,
            clear_values=clear_values,
            map_replace_values=map_replace_values,
        )


class UIntField(Field):
    def __init__(
        self,
        name: str = None,
        errors: ErrorPolicyLiteralT = "default",
        default_value: Any = 0,
        transform_funcs: Union[List[Callable], FunctionSet] = None,
        clear_values: set = None,
        map_replace_values: Dict[OldValueT, NewValueT] = None,
    ):
        _functions = FunctionSet(func.to_uint)
        _functions.add_func(_functionset_from(transform_funcs))
        super().__init__(
            name=name,
            errors=errors,
            default_value=default_value,
            transform_funcs=_functions,
            clear_values=clear_values,
            map_replace_values=map_replace_values,
        )


class FloatField(Field):
    def __init__(
        self,
        name: str = None,
        errors: ErrorPolicyLiteralT = "default",
        default_value: Any = 0.0,
        transform_funcs: Union[List[Callable], FunctionSet] = None,
        clear_values: set = None,
        map_replace_values: Dict[OldValueT, NewValueT] = None,
    ):
        _functions = FunctionSet(float)
        _functions.add_func(_functionset_from(transform_funcs))
        super().__init__(
            name=name,
            errors=errors,
            default_value=default_value,
            transform_funcs=_functions,
            clear_values=clear_values,
            map_replace_values=map_replace_values,
        )


class TextField(Field):
    def __init__(
        self,
        name: str = None,
        errors: ErrorPolicyLiteralT = "default",
        default_value: Any = "",
        transform_funcs: Union[List[Callable], FunctionSet] = None,
        clear_values: set = None,
        map_replace_values: Dict[OldValueT, NewValueT] = None,
    ):
        _functions = FunctionSet(str)
        _functions.add_func(_functionset_from(transform_funcs))
        super().__init__(
            name=name,
            errors=errors,
            default_value=default_value,
            transform_funcs=_functions,
            clear_values=clear_values,
            map_replace_values=map_replace_values,
        )


class TimestampField(Field):
    def __init__(
        self,
        name: str = None,
        errors: ErrorPolicyLiteralT = "default",
        default_value: Any = ...,
        transform_funcs: Union[List[Callable], FunctionSet] = None,
        clear_values: set = None,
        map_replace_values: Dict[OldValueT, NewValueT] = None,
        tz_name: Optional[str] = None,
    ):
        self.__tz_name = tz_name
        _functions = FunctionSet()
        _functions.add_func(func.timestamp_to_datetime, tz_name=tz_name)

        if tz_name is not None:
            _functions.add_func(func.datetime_replace_tz, tz_name=tz_name)

        _functions.add_func(_functionset_from(transform_funcs))

        if default_value is ...:
            default_value = dt.datetime(1970, 1, 1)
            if tz_name is not None:
                default_value = func.datetime_replace_tz(default_value, tz_name=tz_name)

        super().__init__(
            name=name,
            errors=errors,
            default_value=default_value,
            transform_funcs=_functions,
            clear_values=clear_values,
            map_replace_values=map_replace_values,
        )

    def __repr__(self):
        return super().__repr__().replace("...", f" tz_name={self.__tz_name},...")


class DateTimeField(Field):
    def __init__(
        self,
        name: str = None,
        errors: ErrorPolicyLiteralT = "default",
        default_value: Any = ...,
        transform_funcs: Union[List[Callable], FunctionSet] = None,
        clear_values: set = None,
        map_replace_values: Dict[OldValueT, NewValueT] = None,
        fmt: str = None,
        tz_name: Optional[str] = None,
    ):
        self.__fmt = fmt
        self.__tz_name = tz_name
        _functions = FunctionSet()

        if fmt is not None:
            _functions.add_func(func.datetime_strptime, fmt=fmt)
        else:
            _functions.add_func(func.datetime_parse)

        if tz_name is not None:
            _functions.add_func(func.datetime_replace_tz, tz_name=tz_name)

        _functions.add_func(_functionset_from(transform_funcs))

        if default_value is ...:
            default_value = dt.datetime(1970, 1, 1)
            if tz_name is not None:
                default_value = func.datetime_replace_tz(default_value, tz_name=tz_name)

        super().__init__(
            name=name,
            errors=errors,
            default_value=default_value,
            transform_funcs=_functions,
            clear_values=clear_values,
            map_replace_values=map_replace_values,
        )

    def __repr__(self):
        return (
            super()
            .__repr__()
            .replace("...", f" fmt={self.__fmt}, tz_name={self.__tz_name},...")
        )


class DateField(DateTimeField):
    def __init__(
        self,
        name: str = None,
        errors: ErrorPolicyLiteralT = "default",
        default_value: Any = ...,
        transform_funcs: Union[List[Callable], FunctionSet] = None,
        clear_values: set = None,
        map_replace_values: Dict[OldValueT, NewValueT] = None,
        fmt: str = None,
    ):
        self.__fmt = fmt
        _functions = FunctionSet()

        if fmt is not None:
            _functions.add_func(func.datetime_strptime, fmt=fmt)
        else:
            _functions.add_func(func.datetime_parse)

        _functions.add_func(func.datetime_to_date)
        _functions.add_func(_functionset_from(transform_funcs))

        if default_value is ...:
            default_value = dt.date(1970, 1, 1)

        super().__init__(
            name=name,
            errors=errors,
            default_value=default_value,
            transform_funcs=_functions,
            clear_values=clear_values,
            map_replace_values=map_replace_values,
        )

    def __repr__(self):
        return super().__repr__().replace("...", f" fmt={self.__fmt},...")


class ArrayField(Field):
    def __init__(
        self,
        name: str = None,
        errors: ErrorPolicyLiteralT = "default",
        default_value: Any = ...,
        transform_funcs: Union[List[Callable], FunctionSet] = None,
        clear_values: set = None,
        map_replace_values: Dict[OldValueT, NewValueT] = None,
        depth: int = 1,
        transform_funcs_for_array_values: List[Callable] = None,
        replace_no_valid_array_array: bool = True,
    ):
        self.__depth = depth
        self.__transform_funcs_for_array_values = transform_funcs_for_array_values
        self.__replace_no_valid_array_array = replace_no_valid_array_array
        _functions = FunctionSet()
        if default_value is ...:
            default_value = []

        _functions.add_func(func.deserialize_not_valid_list)

        if transform_funcs_for_array_values:
            if depth == 1:
                _functions.add_func(
                    func.apply_array, funcs=transform_funcs_for_array_values
                )
            elif depth > 1:
                _functions.add_func(
                    func.apply_array_array,
                    funcs=transform_funcs_for_array_values,
                    depth=depth,
                    replace_no_valid_array_array=replace_no_valid_array_array,
                )
            else:
                raise TypeError("Permitted 'depth' >= 1")

        _functions.add_func(_functionset_from(transform_funcs))

        super().__init__(
            name=name,
            errors=errors,
            default_value=default_value,
            transform_funcs=_functions,
            clear_values=clear_values,
            map_replace_values=map_replace_values,
        )

    def __repr__(self):
        return (
            super()
            .__repr__()
            .replace(
                "...",
                f" depth={self.__depth}, "
                f"transform_funcs_for_array_values={self.__transform_funcs_for_array_values}, "
                f"replace_no_valid_array_array={self.__replace_no_valid_array_array},...",
            )
        )


class JSONField(Field):
    def __init__(
        self,
        name: str = None,
        errors: ErrorPolicyLiteralT = "default",
        default_value: Any = ...,
        transform_funcs: Union[List[Callable], FunctionSet] = None,
        clear_values: set = None,
        map_replace_values: Dict[OldValueT, NewValueT] = None,
    ):
        if default_value is ...:
            default_value = {}
        _functions = FunctionSet()
        _functions.add_func(func.json_loads)
        _functions.add_func(_functionset_from(transform_funcs))

        super().__init__(
            name=name,
            errors=errors,
            default_value=default_value,
            transform_funcs=_functions,
            clear_values=clear_values,
            map_replace_values=map_replace_values,
        )
