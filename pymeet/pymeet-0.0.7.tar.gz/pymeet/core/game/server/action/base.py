from abc import ABC, abstractmethod


class GameAction(ABC):
    @abstractmethod
    def apply(self):
        pass
