import pytest
import json
import random


from .dummy import Dummy
from .string import String
from .boolean import Boolean
from .integer import Integer
from .number import Number
from .util import _test_valid_args, _test_invalid_args, Values, Value


class Json(Dummy):
    def __init__(self, max_depth: int = 2,
                 lists: bool = True, dicts: bool = True,
                 strings: bool = True, booleans: bool = True,
                 integers: bool = True, numbers: bool = True,
                 nulls: bool = True):
        super().__init__()
        self.max_depth = max_depth
        self.lists = lists
        self.dicts = dicts
        self.strings = strings
        self.booleans = booleans
        self.integers = integers
        self.numbers = numbers
        self.nulls = nulls

    def valid(self, value, raise_error=False):
        try:
            json.loads(value)
            return True
        except json.decoder.JSONDecodeError as e:
            if raise_error:
                raise ValueError("{} is not a valid json string: {}".format(
                    value, e
                ))
            return False

    def _data(self, depth):
        if depth == 0:
            return {}
        data = {
            **({"list_value": [
                *([self._data(depth - 1)] if self.dicts else []),
                *([String().valids()[0]] if self.strings else []),
                *([Boolean().valids()[0]] if self.booleans else []),
                *([Integer().valids()[0]] if self.integers else []),
                *([Number().valids()[0]] if self.numbers else []),
                *([None] if self.nulls else []),
            ]} if self.lists else {}),
            **({"dict_value": self._data(depth - 1)} if self.dicts else {}),
            **({"string_value": String().valids()[0]} if self.strings else {}),
            **({"boolean_value": Boolean().valids()[0]} if self.booleans else {}),
            **({"integer_value": Integer().valids()[0]} if self.integers else {}),
            **({"number_value": Number().valids()[0]} if self.numbers else {}),
            **({"null_value": None} if self.nulls else {}),
        }
        return data

    def _valids(self):
        valids = [
            self._data(self.max_depth),
            [self._data(self.max_depth)],
            {},
            [],
            String().valids()[0],
            Boolean().valids()[0],
            Integer().valids()[0],
            Number().valids()[0],
            None,
        ]
        return Values([json.dumps(v) for v in valids])

    def _invalids(self):
        return Values([
            '{a: "a"}',
            '{"a": "a",}',
            '[1, 2, 3,]',
        ])

    def __str__(self):
        config = {
            "lists": self.lists,
            "dicts": self.dicts,
            "strings": self.strings,
            "booleans": self.booleans,
            "integers": self.integers,
            "numbers": self.numbers,
            "nulls": self.nulls,
        }
        config = [
            k for k, v in config.items()
            if v
        ]
        return "Json: {}, {}".format(self.max_depth, config)


def test_json():
    _test_valid_args(Json, [
        [], [2],
        {
            "max_depth": 4,
        },
        {
            "lists": True,
            "dicts": False,
            "strings": False,
            "booleans": False,
            "integers": False,
            "numbers": False,
            "nulls": False,
        }
    ])

    _test_invalid_args(Json, [
        {"x": True}
    ])

    for max_depth in range(5):
        json.loads(Json(max_depth).valids()[0])
    print(Json(0).valids(exhaustive=True))
    assert len([v for v in Json(0).valids(exhaustive=True) if v == "{}"]) == 2
    assert len([v for v in Json(1).valids(exhaustive=True) if v == "{}"]) == 1
    assert len([v for v in Json(0, *[False for _ in range(7)]).valids(exhaustive=True) if v == "{}"]) == 2
    for i in range(7):
        valids = Json(1, *[False for _ in range(i)]).valids(exhaustive=True)
        main_dict = [
            v for v in valids
            if v.startswith("{") and v != "{}"
        ]
        print(len(main_dict))
        assert len(main_dict) == 1
        main_dict = main_dict[0]
        assert len(json.loads(main_dict)) == 7 - i
    
    for i in range(5):
        for v in Json(i).valids(exhaustive=True):
            json.loads(v)
    
    for v in Json().invalids(exhaustive=True):
        with pytest.raises(Exception):
            json.loads(v)
