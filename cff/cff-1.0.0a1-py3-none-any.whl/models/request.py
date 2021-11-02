from typing import TypedDict


class Request(TypedDict):
    """An HTTP request."""

    method: str
    """
    HTTP method.

    Example:

        .. code-block:: text

            GET
    """

    uri: str
    """
    URI. Does not include the host name or protocol.

    Example:

        .. code-block:: text

            /foo/bar.html
    """
