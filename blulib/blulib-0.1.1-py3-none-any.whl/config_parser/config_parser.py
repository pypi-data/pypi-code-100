import configparser
from pathlib import Path
from shutil import copy
from site import getuserbase
from typing import Any, Callable, Tuple

from .key_info import KeyInfo


class SectionNotFoundError(Exception):
    def __init__(self, section: str) -> None:
        super().__init__(section)
        self.section = section


class ConfigParser(configparser.ConfigParser):
    """
    Extension of the config parser which adds some extra functionality.
    Namely the addition to easily convert a section into an object.
    """

    def to_object(self, object: Any, section_name: str, *keys: str) -> None:
        """Set an object from a config section by specifying the names for the correct type.

        Args:
            object (Any): The object to set the values in
            section_name (str): Section to convert into an object
            keys (*str) keys in the section and object. By default it parses the value as string.
                To parse as another value put "type:key". Example: "float:amount".
                Possible types: str, str_list, int, int_list, float, float_list, bool, bool_list
                If the key differ between section and you can specify "config_key->object_key".
                Example: "from->from_address". This is useful when the config has keys that are
                invalid in python (like 'from')

        Raises:
            SectionNotFoundError if the section is not found
        """
        if section_name not in self:
            raise SectionNotFoundError(section_name)
        section = self[section_name]

        for key in keys:
            info = KeyInfo.from_key(key)
            set_func: Callable
            if info.is_list:
                set_func = ConfigParser._set_list
            else:
                set_func = ConfigParser._set
            set_func(object, section, info)

    @staticmethod
    def _set(object: Any, section: configparser.SectionProxy, key_info: KeyInfo) -> None:
        default = getattr(object, key_info.object_key)
        get_func = getattr(section, key_info.function_name)
        value = get_func(key_info.config_key, fallback=default)
        if isinstance(value, str):
            value = ConfigParser._strip_quotes(value)
        setattr(object, key_info.object_key, value)

    @staticmethod
    def _set_list(object: Any, section: configparser.SectionProxy, key_info: KeyInfo) -> None:
        full_str = section.get(key_info.config_key, fallback="")
        if full_str != "":
            str_values = full_str.split("\n")
            values = []
            for str_value in str_values:
                if str_value != "":
                    str_value = ConfigParser._strip_quotes(str_value)
                    value = key_info.str_to_type(str_value)
                    values.append(value)

            setattr(object, key_info.object_key, values)

    @staticmethod
    def _strip_quotes(value: str) -> str:
        if len(value) >= 2:
            if (value[0] == '"' and value[-1] == '"') or (value[0] == "'" and value[-1] == "'"):
                value = value[1:-1]
        return value

    @staticmethod
    def _get_config_and_arg_names(varname: str) -> Tuple[str, str]:
        split = varname.split("->")
        if len(split) == 2:
            return (split[0], split[1])
        return (split[0], split[0])

    @staticmethod
    def copy_example_if_conf_not_exists(app_name: str) -> None:
        """If there is no configuration, copy the example to the configuration"""
        conf_path = Path.home().joinpath(f".{app_name}.cfg")

        if conf_path.exists():
            return

        # Copy file from config location to home
        example_name = f"{app_name}-example.cfg"
        example_path = Path(getuserbase()).joinpath("config", example_name)

        if not example_path.exists():
            return

        copy(example_path, conf_path)
