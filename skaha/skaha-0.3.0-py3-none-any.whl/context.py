"""Get available resources from the skaha server."""
from attr import attrs

from skaha.client import SkahaClient


@attrs
class Context(SkahaClient):
    """Get available resources from the skaha server."""

    def __attrs_post_init__(self):
        """Initialize the context server URL."""
        self.server = self.server + "/context"

    def resources(self) -> dict:
        """Get available resources from the skaha server.

        Returns:
            A dictionary of available resources.

        Examples:
            >>> from skaha.context import Context
                context = Context()
                context.resources()
            >>> {'defaultCores': 2,
                 'defaultCoresHeadless': 1,
                 ...}

        """
        return self.get(url=self.server).json()
