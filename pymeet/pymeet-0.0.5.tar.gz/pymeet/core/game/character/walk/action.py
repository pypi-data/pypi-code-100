from pymeet.core.game.base import StateTransitionNotAllowedException
from pymeet.core.game.character.base import CharacterAction
from pymeet.core.game.character import Character
from pymeet.core.game.character.direction import Direction

from .state import WalkState


class CharacterWalkAction(CharacterAction):
    def __init__(self, direction: Direction):
        self.direction: Direction = direction

    def apply(self, character: Character):
        from pymeet.core.game.character.idle import IdleState

        if character.in_state(IdleState) or character.in_state(WalkState):
            character.heading_to(self.direction)
            character.transit_state_to(WalkState())
        else:
            raise StateTransitionNotAllowedException(
                'CharacterWalkAction can be applied only when the Character is in IdleState.'
            )
