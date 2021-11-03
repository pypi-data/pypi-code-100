from dataclasses import dataclass
from typing import List, Dict, Union

from axew import BASE_URL


@dataclass
class Profile:
    user: int = None
    slug: str = None
    times_viewed: int = None
    entry_set: List[Dict[str, Union[str, int]]] = None

    def resolve_url(self):
        return BASE_URL + "/profile/" + self.slug
