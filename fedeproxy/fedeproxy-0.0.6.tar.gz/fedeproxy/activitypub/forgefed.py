from dataclasses import dataclass, field
from typing import List

from dataclasses_json import config, dataclass_json

from .base_activity import ActivityObject


@dataclass
class Description(object):
    mediaType: str
    content: str


@dataclass_json
@dataclass
class Commit(ActivityObject):
    # https://forgefed.peers.community/modeling.html#commit
    type: str = "Commit"
    jsonld_context: List[str] = field(metadata=config(field_name="@context"), default=None)
    context: str = None
    attributedTo: str = None
    created: str = None
    committedBy: str = None
    committed: str = None
    hash: str = None
    committed: str = None
    description: Description = None
