from src.base import Action
import webbrowser

from src.logger import log

class Open(Action):
    REQUIRED_CONFIG = True

    def _act(self) -> None:
        log(f'Openning {self.get_problem_url()}')
        webbrowser.open(self.get_problem_url())