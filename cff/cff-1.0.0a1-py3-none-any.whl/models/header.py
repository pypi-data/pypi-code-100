from typing import TypedDict


class Header(TypedDict):
    """An HTTP header."""

    key: str
    """
    Header key or name.

    Example:

        .. code-block:: text

            Location
    """

    value: str
    """
    Header value.

    Example:

        .. code-block:: text

            /foo/bar.html
    """
