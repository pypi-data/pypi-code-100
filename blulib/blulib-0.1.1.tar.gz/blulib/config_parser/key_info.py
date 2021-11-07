from __future__ import annotations

import re
from typing import Any, Dict, List


class KeyError(Exception):
    def __init__(self, type: str) -> None:
        super().__init__(type)
        self.type = type


class KeyInfo:
    _key_regex = re.compile(r"^(?:([a-z_]+):)?([\w\d\-_ ]+)(?:->([\w\d_]+))?$")
    _valid_key_types: List[str] = [
        "str",
        "str_list",
        "int",
        "int_list",
        "float",
        "float_list",
        "bool",
        "bool_list",
    ]
    _func_name: Dict[str, str] = {
        "str": "get",
        "int": "getint",
        "float": "getfloat",
        "bool": "getboolean",
    }
    _bool_map: Dict[str, bool] = {
        "yes": True,
        "no": False,
        "1": True,
        "0": False,
        "true": True,
        "false": False,
    }

    def __init__(self, is_list: bool, type: str, config: str, object: str) -> None:
        self.type = type
        self.is_list = is_list
        self.config_key = config
        self.object_key = object

    @property
    def function_name(self) -> str:
        return KeyInfo._func_name[self.type]

    def str_to_type(self, value: str) -> Any:
        if self.type == "str":
            return value
        if self.type == "int":
            return int(value)
        if self.type == "float":
            return float(value)
        if self.type == "bool":
            value = value.lower()
            if value in KeyInfo._bool_map:
                return KeyInfo._bool_map[value]
            return False

    @staticmethod
    def from_key(key: str) -> KeyInfo:
        match = KeyInfo._key_regex.match(key)
        if not match:
            raise KeyError(key)

        key_type, config, object = match.groups()
        is_list = False
        if not key_type:
            key_type = "str"
        else:
            if not key_type in KeyInfo._valid_key_types:
                raise KeyError(key)
            if "list" in key_type:
                is_list = True
                key_type = key_type.replace("_list", "")

        if not object:
            object = config.replace("-", "_").replace(" ", "_")

        return KeyInfo(
            is_list,
            key_type,
            config,
            object,
        )

    def __members(self):
        return [
            self.type,
            self.is_list,
            self.config_key,
            self.object_key,
        ]

    def __eq__(self, other) -> bool:
        if type(other) is type(self):
            return self.__members() == other.__members()
        return False

    def __hash__(self) -> int:
        return hash(self.__members())
