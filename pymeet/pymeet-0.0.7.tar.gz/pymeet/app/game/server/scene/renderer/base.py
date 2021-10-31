from typing import Tuple
from abc import ABC, abstractmethod
from pygame import Surface

from pymeet.core.game.character.view import CharacterView


class Renderer(ABC):
    @abstractmethod
    def render(self, screen: Surface):
        pass


class CharacterRenderer(ABC):
    @abstractmethod
    def render_character(self, screen: Surface, character: CharacterView):
        pass


class GroundRenderer(ABC):
    @abstractmethod
    def render_ground(self, screen: Surface, character_position: Tuple[float, float]):
        pass
