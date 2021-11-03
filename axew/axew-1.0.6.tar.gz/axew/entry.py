import datetime
from dataclasses import dataclass


BASE_URL = "https://beta.arcanebin.com"
MAX_SIZE = {"name": 200, "description": 2500, "code": 15000, "error": 5000}


@dataclass
class Entry:
    name: str = None
    slug: str = None
    code: str = None
    error: str = None
    language: str = None
    description: str = None
    times_viewed: int = None
    absolute_url: str = None
    created_at: datetime.datetime = None
    last_modified: datetime.datetime = None

    def resolve_url(self):
        return BASE_URL + "/view/" + self.slug
