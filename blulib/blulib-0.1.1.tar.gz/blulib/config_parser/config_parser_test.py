from enum import Enum
from pathlib import Path
from typing import Any, List

import pytest

from .config_parser import ConfigParser, SectionNotFoundError
from .key_info import KeyError


@pytest.fixture
def parser() -> ConfigParser:
    path = Path("fixtures", "config_parser.cfg")
    parser = ConfigParser()
    parser.read(path)
    return parser


class Object:
    def __init__(
        self,
        str_value: Any = "",
        str_list: List[str] = [],
        int_value: int = 0,
        int_list: List[int] = [],
        float_value: float = 0,
        float_list: List[float] = [],
        bool_value: bool = False,
        bool_list: List[bool] = [],
    ) -> None:
        self.str_value = str_value
        self.str_list = str_list
        self.int_value = int_value
        self.int_list = int_list
        self.float_value = float_value
        self.float_list = float_list
        self.bool_value = bool_value
        self.bool_list = bool_list

    def __members(self):
        return [
            self.str_value,
            self.str_list,
            self.int_value,
            self.int_list,
            self.float_value,
            self.float_list,
            self.bool_value,
            self.bool_list,
        ]

    def __eq__(self, other) -> bool:
        if type(other) is type(self):
            return self.__members() == other.__members()
        return False

    def __hash__(self) -> int:
        return hash(self.__members())

    def __repr__(self) -> str:
        return str(self.__members())


@pytest.mark.parametrize(
    "name,object,section,keys,expected",
    [
        (
            "str test - works to read str variables",
            Object(),
            "str test",
            ["str:str_value", "str_list:str_list"],
            Object(str_value="str test", str_list=["One", "Two", "Three"]),
        ),
        (
            "int test - works to read int variables",
            Object(),
            "int test",
            ["int:int_value", "int_list:int_list"],
            Object(int_value=15, int_list=[1, 2, 3]),
        ),
        (
            "float test - works to read float variables",
            Object(),
            "float test",
            ["float:float_value", "float_list:float_list"],
            Object(float_value=20.5, float_list=[1, 2.0, 0.003]),
        ),
        (
            "bool test - works to read bool variables",
            Object(),
            "bool test",
            ["bool:bool_value", "bool_list:bool_list"],
            Object(bool_value=True, bool_list=[True, False, True, False, True, False, True, False, True, False]),
        ),
        (
            "Should use default value from object when the key is missing",
            Object(str_value="default"),
            "missing key test",
            ["str_value"],
            Object(str_value="default"),
        ),
        (
            "Should return SectionNotFoundError if the section doesn't exist",
            Object(),
            "section does not exist",
            [],
            SectionNotFoundError,
        ),
        (
            "Should return KeyError if the key format is invalid",
            Object(),
            "str test",
            ["type is: invol$->i eon"],
            KeyError,
        ),
        (
            "Should return AttributeError if the object doesn't have the key",
            Object(),
            "str test",
            ["key->doesnt_exist"],
            AttributeError,
        ),
    ],
)
def test_to_object(
    name: str, object: Object, section: str, keys: List[str], expected: Any, parser: ConfigParser
) -> None:
    print(name)

    if type(expected) != Object:
        with pytest.raises(expected):
            parser.to_object(object, section, *keys)
    else:
        parser.to_object(object, section, *keys)
        assert expected == object


class StrEnum(Enum):
    test = "test"


class ContainsEnum:
    def __init__(self) -> None:
        self.use_default = StrEnum.test
        self.replaced = StrEnum.test


def test_to_object_read_str_but_is_object(parser: ConfigParser) -> None:
    expected = {
        "use_default": StrEnum.test,
        "replaced": "hello",
    }
    actual = ContainsEnum()
    parser.to_object(actual, "enum as string", "use_default", "replaced")

    assert expected["use_default"] == actual.use_default
    assert expected["replaced"] == actual.replaced
