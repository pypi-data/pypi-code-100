"Configuration class and decorator"
import configparser
import pathlib

import click

from .get_root import get_root

class _ConfigGroup:
    "Internal class for a config group"
    def __init__(self, section, writer):
        self._section = section
        self._writer = writer

    def __getitem__(self, key):
        return self._section[key]


    def __setitem__(self, key, value):
        self._section[key] = value
        self._writer()

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            pass
        raise AttributeError(f"{self} has no attribute {name!r}")

    def __setattr__(self, name, value):
        if name in ["_section", "_writer"]:
            object.__setattr__(self, name, value)
            return
        self[name] = value

    def __delitem__(self, key):
        del self._section[key]
        self._writer()

    def __delattr__(self, name):
        del self[name]

    def __str__(self):
        return "config." + self._section.name

    def __contains__(self, value):
        return value in self._section


class _SlashListConfigGroup(_ConfigGroup):
    "Internal class for a config group where items are slash separated lists"
    def __getitem__(self, key):
        return self._section[key].split("/")

    def __setitem__(self, key, value):
        self._section[key] = "/".join(value)
        self._writer()


class Config:
    """Config Class

    Assume this is our config file

    ```
    [bells]
    version = 1.0

    [autocomplete]
    foo/bar = eggs/spam/lorem/ipsum
    foo/baz = dolor/sit
    ```

    Usage:

    ```
    >>> config.root
    PosixPath('/home/user/voice')

    >>> config.config_file_path
    PosixPath('/home/user/voice/.bells/config.ini')

    >>> config.bells.version
    '1.0'

    >>> config['bells']['version']
    '1.0'

    >>> config.autocomplete['foo/bar']
    ['eggs', 'spam', 'lorem', 'ipsum']

    >>> config.autocomplete['foo/baz']
    ['dolor', 'sit']

    >>> config.autocomplete['foo/baz'] = ['new', 'content']

    >>> del config.autocomplete['foo/bar']
    ```

    The config file is modified whenever the object is modified. The config file
    at the end of running above lines would be

    ```
    [bells]
    version = 1.0

    [autocomplete]
    foo/baz = new/content
    ```

    """
    list_sections = ['autocomplete']

    def __init__(self):
        self.root = get_root()
        if isinstance(self.root, pathlib.Path):
            self.config_file_path = self.root / ".bells" / "config.ini"
            self._read_config_file()

    def _read_config_file(self):
        "Reads config file into a config parser"
        config = configparser.ConfigParser()
        config.read(self.config_file_path)
        self.config = config

    def _write_config_file(self):
        "Writes config back into the config file"
        with open(self.config_file_path, "w", encoding="utf-8") as config_file:
            self.config.write(config_file)

    def __getitem__(self, key):
        if key not in self.config:
            self.config[key] = {}
        if key in self.list_sections:
            return _SlashListConfigGroup(self.config[key], self._write_config_file)
        return _ConfigGroup(self.config[key], self._write_config_file)

    def __getattr__(self, name):
        return self[name]

pass_config = click.make_pass_decorator(Config, ensure=True)
