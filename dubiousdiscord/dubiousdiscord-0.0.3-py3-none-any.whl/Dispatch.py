
from dataclasses import dataclass
import traceback
from typing import Generic, Optional, TypeVar

from dubious.enums import events
from dubious.objects import Data, Guild, Interaction, Message, Payload, Ready, Snowflake, UnavailableGuild

t_d = TypeVar("t_d", bound=Data)
class Dispatch(Generic[t_d]):
    event: str
    data: t_d

    def __init__(self, event: str, data: t_d):
        self.event = event
        self.data = data

@dataclass
class MessageDelete(Data):
    id: Snowflake
    channel_id: Snowflake

    guild_id: Snowflake = None

@dataclass
class MessagesDelete(Data):
    id: list[Snowflake]
    channel_id: Snowflake

    guild_id: Snowflake

dispatchKeys: dict[str, type[Data]] = {
    events.onReady: Ready,

    events.onInteractionCreate: Interaction,

    events.onMessageCreate: Message,
    events.onMessageEdit: Message,
    events.onMessageDelete: MessageDelete,
    events.onMessageDeleteBulk: MessagesDelete,

    events.onGuildCreate: Guild,
    events.onGuildDelete: UnavailableGuild,
}

def createDispatch(payload: Payload):
    event: str = payload.t
    raw: dict = payload.d
    data: Optional[Data] = None
    if event in dispatchKeys:
        try:
            data = dispatchKeys[event].new(**raw)
        except Exception as e:
            print(traceback.format_exc())
            return None
        return Dispatch(event, data)
    else:
        #print(f"recieved an unimplemented event: {event}")
        return None
