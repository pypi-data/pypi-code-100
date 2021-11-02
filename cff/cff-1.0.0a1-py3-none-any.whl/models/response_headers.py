from typing import List, TypedDict

from cff.models.header import Header


class ResponseHeaders(TypedDict):
    """HTTP response headers."""

    location: List[Header]
    """Location headers."""
