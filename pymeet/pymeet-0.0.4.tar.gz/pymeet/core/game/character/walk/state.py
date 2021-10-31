from typing import Optional, Dict

from pymeet.core.game.base import State
from pymeet.core.game.character.main import Character
from pymeet.core.game.character.idle import IdleState
from pymeet.core.game.character.direction import Direction


_UNITS_PER_FRAME = 1.0
_FRAMES_COUNT = 1
_STATE_TYPE_KEY = 'WALK'


class WalkState(State):
    MAX_FRAMES_COUNT = _FRAMES_COUNT

    def __init__(self, *, frames_count: int = 0):
        self._frames_count: int = frames_count
        self._character: Optional[Character] = None

    @property
    def frames_count(self):
        return self._frames_count

    def on_enter(self, context: Character, state_prev: State):
        self._frames_count = 0
        self._character = context

    def update(self):
        dir_unit = Direction.to_unit_vector(self._character.get_heading())
        pos = self._character.get_position() + dir_unit * _UNITS_PER_FRAME
        self._character.move_to_position(pos)

        self._frames_count += 1
        if self._frames_count == WalkState.MAX_FRAMES_COUNT:
            self._character.schedule_next_state(IdleState())

    def to_dict(self) -> Dict:
        return {
            'type': _STATE_TYPE_KEY,
            'payload': {
                'direction': self._character.get_heading().value,
                'frames_count': self._frames_count,
            },
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'WalkState':
        assert data['type'] == _STATE_TYPE_KEY
        payload = data['payload']
        return cls(frames_count=int(payload['frames_count']))
