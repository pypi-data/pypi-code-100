from pymeet.core.registry import Registry
from pymeet.core.game.server import GameServer
from pymeet.core.game.character import Character
from pymeet.core.game.character.id import CharacterId
from pymeet.core.game.character.position import CharacterPosition
from pymeet.core.game.character.direction import Direction
from pymeet.core.game.character.idle.state import IdleState


def start_server():
    reg = Registry()
    reg.game_server = GameServer()

    character = Character(CharacterId('000'), CharacterPosition(0, 0), Direction.DOWN, IdleState())
    reg.character_repository.add(character)


def update_server():
    reg = Registry()
    reg.game_server.update()
