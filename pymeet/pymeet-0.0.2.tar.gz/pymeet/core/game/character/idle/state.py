from typing import Dict

from pymeet.core.game.base import State


_STATE_TYPE_KEY = 'IDLE'


class IdleState(State):
    def update(self):
        pass

    def to_dict(self) -> Dict:
        return {
            'type': _STATE_TYPE_KEY,
            'payload': {},
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'IdleState':
        assert data['type'] == _STATE_TYPE_KEY
        return cls()
