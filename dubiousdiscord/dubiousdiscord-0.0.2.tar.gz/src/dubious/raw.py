
from dataclasses import asdict
from typing import TypedDict

from dubious.objects import Data


def asJson(data: Data):
    return asdict(data)

class CreateCommandOptionChoice(TypedDict):
    name: str
    value: str

class CreateCommandOption(TypedDict):
    name: str
    type: int
    description: str

    required: bool
    choices: list[CreateCommandOptionChoice]

class CreateCommand(TypedDict):
    name: str
    type: int
    description: str
    options: list[CreateCommandOption]
