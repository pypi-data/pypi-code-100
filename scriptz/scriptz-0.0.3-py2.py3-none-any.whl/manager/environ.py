from pathlib import PurePath
from configparser import ConfigParser


class Environ:
    def __init__(self, env_ini: ConfigParser):
        self.env_ini = env_ini

    def get(self, path):
        path = PurePath(path)
        environ = dict(self.env_ini.defaults()).copy()
        for section in self.env_ini.sections():
            if path.match(section):
                for option in self.env_ini.options(section):
                    environ[option] = self.env_ini.get(section, option)
        return environ
