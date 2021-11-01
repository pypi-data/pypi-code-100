from src.version import version
from src.base import Action
from src.logger import color_cyan, log

class Version(Action):
    def _act(self) -> None:
        log(f'Current version: {color_cyan(version)}')