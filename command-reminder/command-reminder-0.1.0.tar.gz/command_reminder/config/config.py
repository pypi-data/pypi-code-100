import os
from dataclasses import dataclass

from command_reminder.common import InvalidArgumentException

COMMAND_REMINDER_DIR_ENV = "COMMAND_REMINDER_DIR"
HOME_DIR_ENV = "HOME"
DEFAULT_REPOSITORY_DIR = '.command-reminder/repository'


@dataclass
class Configuration:
    path: str

    @staticmethod
    def load_config():
        path = os.getenv(COMMAND_REMINDER_DIR_ENV)
        home = os.getenv(HOME_DIR_ENV)
        Configuration._validate(home)
        if not path:
            path = os.path.join(home, DEFAULT_REPOSITORY_DIR)

        return Configuration(path)

    @staticmethod
    def _validate(home: str):
        if not home:
            raise InvalidArgumentException("$HOME environment variable must be set")
