from configparser import ConfigParser
from pathlib import Path
from typing import Optional, Union

from . import Handler, Environ


class Config:
    def __init__(self, root_dir: Path):
        # get configuration values from scriptz.ini file
        self.ini_path = root_dir / "scriptz.ini"
        ini = self._read_ini_file(self.ini_path)
        cfg = "config"

        # maximum number of characters to keep when creating a file name
        self.file_length = max(ini.getint(cfg, "file_length", fallback=20), 6)

        # length of prefix used by str.zfill() to pad name with zeroes
        self.prefix_size = max(ini.getint(cfg, "prefix_size", fallback=2), 1)

        # handlers
        self.handlers = Handler.create_handlers(ini)
        self.file_types = list(h.display for h in self.handlers.values())
        self.default_type = self.file_types[0] if self.file_types else None
        self.file_types = list(dict.fromkeys(self.file_types))

        # secrets/environment variables
        self.env_path = root_dir / "secretz.ini"
        env_ini = self._read_ini_file(self.env_path, env=True)
        self.environs = Environ(env_ini=env_ini)

    def get_handler(self, key: Union[Path, str]) -> Optional[Handler]:
        if isinstance(key, Path):
            key = key.suffix
        return self.handlers.get(key)

    def get_environ(self, path: Union[Path, str]) -> dict:
        return self.environs.get(path=path)

    def zfill(self, number):
        if number == -1:
            return "9" * self.prefix_size
        return str(number).zfill(self.prefix_size)

    @property
    def is_valid(self):
        return self.handlers

    # private methods

    @classmethod
    def _read_ini_file(cls, ini_path: Path, env: bool = False) -> ConfigParser:
        ini = ConfigParser()
        if env:
            ini.optionxform = str

        if ini_path.is_file():
            ini.read_file(ini_path.open("r"))
        return ini
