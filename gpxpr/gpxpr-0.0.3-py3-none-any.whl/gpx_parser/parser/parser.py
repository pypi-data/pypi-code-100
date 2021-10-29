import abc
from typing import Any


class Parser(abc.ABC):
    @abc.abstractmethod
    def parse(self) -> Any:
        raise NotImplementedError()
