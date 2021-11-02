from typing import TypedDict

from cff.models.request import Request


class CloudFrontEvent(TypedDict):
    """A CloudFront event."""

    request: Request
    """The HTTP request that raised this event."""
