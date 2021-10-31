from typing import List
from threading import Lock

from pymeet.core.game.character.view import CharacterView
from pymeet.core.game.server.action import GameAction


class GameMessage:
    def __init__(self, timestamp: float):
        self.timestamp: float = timestamp

    def __lt__(self, other: 'GameMessage'):
        return self.timestamp < other.timestamp


class GameStateMessage(GameMessage):
    def __init__(self, timestamp: float, characters: List[CharacterView]):
        super().__init__(timestamp)

        self.characters: List[CharacterView] = characters


class GameActionMessage(GameMessage):
    def __init__(self, timestamp: float, action: GameAction):
        super().__init__(timestamp)

        self.action: GameAction = action


class GameMessageQueue:
    def __init__(self):
        self._lock = Lock()
        self._queue: List[GameMessage] = []

    def push(self, message: GameMessage):
        with self._lock:
            self._queue.append(message)

    def pop_all(self) -> List[GameMessage]:
        with self._lock:
            out = self._queue
            self._queue = []
            return sorted(out)
