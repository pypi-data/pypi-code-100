from datetime import datetime
from typing import List, Literal

from pydantic import BaseModel


class SearchResultCount(BaseModel):
    """Represents number of matches in search results.

    Attributes:
        value: nNmber of matches
        relation: Clarifies meaning of value. If "eq" - `value` contains an exact number of matches,
            "gte" - there are more than `value` matches
    """

    value: int
    relation: Literal["eq", "gte"]


class SearchUtterance(BaseModel):
    """Single utterance match object for search results.
    Used as child objects of `SearchMatch`.

    Attributes:
        id: Utterance id
        snippet: List of highlighted utterance fragments to show to users
        speaker: Speaker name for the utterance
        start: Utterance start time
    """

    id: int
    snippet: List[str]
    speaker: str
    start: float


class SearchMatch(BaseModel):
    """Session match object for search results.

    Attributes:
        hits_total: Number of matched utterances in the session
        hits: A list of matched utterances
        snippet: A list of highlighted session fragments to show to users

        id: Session id
        caller_id: Caller id
        created_at: Creation date of the session
        duration: Duration of the session in seconds
        silence_percent: Percent of silence in the session. Range 0-100, 0 - no silence, 100 - only silence
        language_code: Language code of the session

        start_dt: Date and time of session start
        end_dt: Date and time of session end
        source: Data source of the session
    """

    hits_total: SearchResultCount
    hits: List[SearchUtterance]
    snippet: List[str]

    id: str
    caller_id: str
    duration: float
    silence_percent: float
    language_code: str

    start_dt: datetime
    end_dt: datetime

    created_at: datetime
    source: str


class SearchResponse(BaseModel):
    """Search response object

    Attributes:
        total: Number of matched sessions
        matches: A list of matched sessions
    """

    total: SearchResultCount
    matches: List[SearchMatch]
