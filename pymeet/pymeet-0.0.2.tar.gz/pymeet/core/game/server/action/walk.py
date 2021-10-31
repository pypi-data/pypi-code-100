from contextlib import suppress

from pymeet.core.game.base import StateTransitionNotAllowedException
from pymeet.core.game.character import CharacterId
from pymeet.core.game.character.direction import Direction
from pymeet.core.game.character.walk import CharacterWalkAction

from pymeet.core.registry import Registry

from .base import GameAction


class WalkAction(GameAction):
    def __init__(self, target: CharacterId, direction: Direction):
        self.target: CharacterId = target
        self.direction: Direction = direction

    def apply(self):
        reg = Registry()
        character = reg.character_repository.from_id(self.target)
        character_action = CharacterWalkAction(self.direction)

        with suppress(StateTransitionNotAllowedException):
            character_action.apply(character)
