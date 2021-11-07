from typing import Any

import pytest

from .key_info import KeyError, KeyInfo


@pytest.mark.parametrize(
    "name,key,expected",
    [
        (
            "str is valid keyname",
            "str:key",
            KeyInfo(False, "str", "key", "key"),
        ),
        (
            "str list is valid keyname",
            "str_list:key",
            KeyInfo(True, "str", "key", "key"),
        ),
        (
            "int is valid keyname",
            "int:key",
            KeyInfo(False, "int", "key", "key"),
        ),
        (
            "int_list is valid keyname",
            "int_list:key",
            KeyInfo(True, "int", "key", "key"),
        ),
        (
            "float is valid keyname",
            "float:key",
            KeyInfo(False, "float", "key", "key"),
        ),
        (
            "float_list is valid keyname",
            "float_list:key",
            KeyInfo(True, "float", "key", "key"),
        ),
        (
            "bool is valid keyname",
            "bool:key",
            KeyInfo(False, "bool", "key", "key"),
        ),
        (
            "bool_list is valid keyname",
            "bool_list:key",
            KeyInfo(True, "bool", "key", "key"),
        ),
        (
            "default to str when no type is specified",
            "key",
            KeyInfo(False, "str", "key", "key"),
        ),
        (
            "different config and object keys",
            "config_key->object_key",
            KeyInfo(False, "str", "config_key", "object_key"),
        ),
        (
            "everything is specified",
            "int_list:conf->obj",
            KeyInfo(True, "int", "conf", "obj"),
        ),
        (
            "Invalid type",
            "sup:key",
            KeyError,
        ),
        (
            "Invalid key",
            "this is $ not a valid key",
            KeyError,
        ),
        (
            "conf key with spaces converts obj to snake_case",
            "key with spaces",
            KeyInfo(False, "str", "key with spaces", "key_with_spaces"),
        ),
        (
            "conf-key-with-dashes converts obj to snake_case",
            "key-with-dashes",
            KeyInfo(False, "str", "key-with-dashes", "key_with_dashes"),
        ),
        (
            "key with multiple spaces and dashes is correctly converted to object",
            "key - with multiple   dashes --",
            KeyInfo(False, "str", "key - with multiple   dashes --", "key___with_multiple___dashes___"),
        ),
        (
            "object key can't have spaces",
            "key->s p a c e s",
            KeyError,
        ),
        (
            "object key can't have dashes",
            "key->d-a-s-h-e-s",
            KeyError,
        ),
        (
            "object key can have snake_case",
            "key->snake_case",
            KeyInfo(False, "str", "key", "snake_case"),
        ),
    ],
)
def test_from_key(name: str, key: str, expected: Any) -> None:
    print(name)

    if expected == KeyError:
        with pytest.raises(KeyError):
            KeyInfo.from_key(key)
    else:
        key_info = KeyInfo.from_key(key)
        assert expected == key_info
