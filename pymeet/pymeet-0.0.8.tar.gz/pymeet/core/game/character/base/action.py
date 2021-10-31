from abc import ABC, abstractmethod

from pymeet.core.game.character import Character


class CharacterAction(ABC):
    @abstractmethod
    def apply(self, character: Character):
        pass
