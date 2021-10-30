import datetime as dt
from dataclasses import dataclass, field
from typing import Any

from dateutil import parser


class EntityParser:
    """
    Main class for entity parsing. Can be safely extended.

    Parameters
    ----------
    `entity` : str
        name of the entity. (actual name not the slot name)
    `value` : dict
        the value key from slots.
    """

    def __init__(self, entity: str, value: dict) -> None:
        self.value_ = value
        self.entity = entity

        self.MAPPINGS = {
            "snips/datetime": self.datetimeParser,
            "snips/duration": self.durationParser,
        }

    @property
    def value(self) -> Any:
        parsed = self.MAPPINGS.get(self.entity)

        if parsed:
            return parsed()
        return self.value_["value"]

    def datetimeParser(self) -> dt.datetime:
        return parser.parse(self.value_["value"])

    def durationParser(self) -> dt.datetime:
        val = self.value_
        now = dt.datetime.now()
        future = now + dt.timedelta(
            days=val["days"],
            seconds=val["seconds"],
            minutes=val["minutes"],
            hours=val["hours"],
            weeks=val["weeks"],
        )
        return future


@dataclass
class Slot:
    rawSlot: dict

    entity: str = field(init=False)
    rawValue: str = field(init=False)
    name: str = field(init=False)

    def __post_init__(self) -> None:
        self.entity = self.rawSlot["entity"]
        self.rawValue = self.rawSlot["rawValue"]
        self.name = self.rawSlot["slotName"]
    
    @property
    def value(self):
        return EntityParser(self.entity, self.rawSlot["value"]).value


@dataclass
class Context:
    """
    Main context object that is returned from API.process when a request succeeds.
    """

    api: Any # Can't cyclic import but this is the API object from api.py
    parsed: dict
    origin: str
    situation: str
    logging: object

    slots: list = field(init=False)
    probability: float = field(init=False)
    intent: str = field(init=False)
    inp: str = field(init=False)

    def __post_init__(self) -> None:
        self.slots = self.parsed["slots"]
        self.probability = self.parsed["intent"]["probability"]
        self.intent = self.parsed["intent"]["intentName"]
        self.inp = self.parsed["input"]
    
    async def slot(self, names: list, **kwargs) -> Slot:
        """
        Used for retrieving a slot.

        Parameters
        ----------
        `names` : List[str]
            List of names to look for. Searching is done by `key`.
        `slots` : List[dict]
            List of raw slots that the function will look names for. By default this is self.slots
        `key` : str
            What key to use for looking slot names. By default this is 'slotName'
        """

        slots = kwargs.get("slots", self.slots)
        key = kwargs.get("key", "slotName")

        slot_ = [i for i in slots if i[key] in names]
        if not slot_:
            self.logging.debug(f"Slot object value for nmames {names} is None.")
            return None

        slotObj = Slot(slot_[0])
        self.logging.debug(f"Slot object value for names {names} is {slotObj.value}")
        return slotObj
