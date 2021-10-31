import datetime

from pymeet.core.registry import Registry
from pymeet.core.game.character.id import CharacterId
from pymeet.core.game.character.direction import Direction
from pymeet.core.game.server.action.walk import WalkAction
from pymeet.core.game.server.message import GameActionMessage


def walk(character_id: str, direction: str):
    action: WalkAction = WalkAction(target=CharacterId(character_id), direction=Direction[direction])
    message = GameActionMessage(datetime.datetime.now().timestamp(), action)
    Registry().local_message_queue.push(message)
