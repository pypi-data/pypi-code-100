from typing import Type

from pymeet.core.game.character.idle.state import State


def get_character_state_type(data) -> Type[State]:
    type_ = data['type']
    if type_ == 'WALK':
        from .walk import WalkState
        return WalkState
    if type_ == 'IDLE':
        from pymeet.core.game.character.idle.state import IdleState
        return IdleState

    raise NotImplementedError()
