from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .base_activity import ActivityObject


@dataclass
class Verb(ActivityObject):
    actor: str = None
    object: ActivityObject = None


@dataclass_json
@dataclass
class Follow(Verb):
    object: str = None
    type: str = "Follow"
