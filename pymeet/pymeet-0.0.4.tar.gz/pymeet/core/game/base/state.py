from typing import Dict, Optional
from abc import ABC, abstractmethod


class StateTransitionNotAllowedException(Exception):
    pass


class NextStateAlreadyScheduledException(Exception):
    pass


class State(ABC):
    @abstractmethod
    def to_dict(self) -> Dict:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict) -> 'State':
        pass

    @abstractmethod
    def update(self):
        pass

    def on_enter(self, context: 'StateContext', state_prev: 'State'):
        pass

    def on_exit(self, state_next: 'State'):
        pass


class StateContext:
    def __init__(self, state: State):
        self._state: State = state
        self._state_next: Optional[State] = None

    def update(self):
        if self._state_next:
            self.transit_state_to(self._state_next)
        self._state.update()

    def transit_state_to(self, state: State):
        self._state.on_exit(state_next=state)

        state_prev = self._state
        self._state = state
        self._state.on_enter(self, state_prev=state_prev)

        self._state_next = None

    def schedule_next_state(self, state: State):
        if self._state_next is not None:
            raise NextStateAlreadyScheduledException()
        self._state_next = state
