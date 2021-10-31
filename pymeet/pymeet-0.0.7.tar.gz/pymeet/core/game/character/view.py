from typing import Dict

from pymeet.core.game.base import State
from .id import CharacterId
from .position import CharacterPosition
from .direction import Direction
from .main import Character
from .state_mapper import get_character_state_type


class CharacterView:
    def __init__(self, id_: CharacterId, state: State, position: CharacterPosition, heading: Direction):
        self.id_: CharacterId = id_
        self.state: State = state
        self.position: CharacterPosition = position
        self.heading: Direction = heading

    @classmethod
    def from_character(cls, character: Character) -> 'CharacterView':
        return cls(
            id_=character.get_id(),
            state=character._state,
            position=character.get_position(),
            heading=character.get_heading(),
        )

    def to_dict(self) -> Dict:
        return {
            'id': str(self.id_),
            'state': self.state.to_dict(),
            'position': self.position.get_tuple(),
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'CharacterView':
        state_type = get_character_state_type(data)

        return cls(
            id_=CharacterId(data['id']),
            state=state_type.from_dict(data['state']),
            position=CharacterPosition(*data['position']),
            heading=Direction(data['heading'])
        )
