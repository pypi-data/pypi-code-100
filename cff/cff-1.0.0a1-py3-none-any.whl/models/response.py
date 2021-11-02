from typing import TypedDict

from cff.models.response_headers import ResponseHeaders


class Response(TypedDict):
    """An HTTP response."""

    headers: ResponseHeaders
    """Headers."""

    status: int
    """
    Status code

    Example:

        .. code-block:: text

            301
    """
