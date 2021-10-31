from typing import Optional

from .base import Singleton


class Registry(metaclass=Singleton):
    def __init__(self):
        from pymeet.core.game.character.repository import CharacterRepository
        from pymeet.core.game.server.message import GameMessageQueue
        from pymeet.core.messaging import MessageServer
        from pymeet.core.messaging import MessageClient
        from pymeet.core.game.server import GameServer
        from pymeet.core.game import Game

        self.character_repository: CharacterRepository = CharacterRepository()
        self.remote_message_queue: Optional[GameMessageQueue] = GameMessageQueue()
        self.local_message_queue: Optional[GameMessageQueue] = GameMessageQueue()
        self.message_server: Optional[MessageServer] = None
        self.message_client: Optional[MessageClient] = None
        self.game_server: Optional[GameServer] = None
        self.game: Optional[Game] = None
