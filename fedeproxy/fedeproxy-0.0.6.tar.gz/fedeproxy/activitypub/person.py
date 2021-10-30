from dataclasses import dataclass, field
from typing import Dict

from dataclasses_json import config, dataclass_json

from .base_activity import ActivityObject


@dataclass
class PublicKey(ActivityObject):
    owner: str = None
    publicKeyPem: str = None
    type: str = "PublicKey"


@dataclass_json
@dataclass
class Person(ActivityObject):
    preferredUsername: str = None
    inbox: str = None
    publicKey: PublicKey = None
    jsonld_context: list = field(metadata=config(field_name="@context"), default=None)
    followers: str = None
    following: str = None
    outbox: str = None
    endpoints: Dict = None
    name: str = None
    summary: str = None
    manuallyApprovesFollowers: str = False
    discoverable: str = False
    type: str = "Person"
