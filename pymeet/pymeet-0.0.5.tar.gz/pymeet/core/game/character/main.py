from typing import Tuple, Type

from pymeet.core.game.base import StateContext, State

from .id import CharacterId
from .position import CharacterPosition
from .direction import Direction


class Character(StateContext):
    def __init__(self, character_id: CharacterId, pos: CharacterPosition, heading: Direction,
                 state: State, *, timestamp: float = 0):
        super().__init__(state)

        self._pos: CharacterPosition = pos
        self._heading: Direction = heading
        self._id: CharacterId = character_id
        self._timestamp: float = timestamp

    def get_heading(self):
        return self._heading

    def heading_to(self, direction: Direction):
        self._heading = direction

    def move_to_position(self, position: CharacterPosition):
        self._pos = position

    def assign_id(self, character_id: CharacterId):
        self._id = character_id

    def get_id(self) -> CharacterId:
        return self._id

    def get_position(self) -> CharacterPosition:
        return self._pos

    def get_position_tuple(self) -> Tuple[float, float]:
        return self._pos.get_tuple()

    def in_state(self, state_type: Type[State]):
        return isinstance(self._state, state_type)
