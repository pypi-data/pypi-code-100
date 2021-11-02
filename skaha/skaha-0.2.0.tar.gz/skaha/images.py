"""Skaha Image Management."""
from typing import Optional

from attr import attrs

from skaha.client import SkahaClient
from skaha.utils.logs import get_logger

log = get_logger(__name__)


@attrs
class Images(SkahaClient):
    """Skaha Image Management.

    Args:
        SkahaClient (object): Skaha HTTP Client

    """

    def __attrs_post_init__(self):
        """Modify the attributes of the SkahaClient class."""
        self.server = self.server + "/image"

    def fetch(self, kind: Optional[str] = None, prune: bool = True) -> list:
        """Get images from Skaha Server.

        Args:
            kind (Optional[str], optional): Type of image. Defaults to None.
            prune (bool, optional): Provide only image name. Defaults to True.

        Returns:
            list: A list of images on the skaha server.

        """
        data: dict = {}
        if kind:
            data["type"] = kind
        response = self.get(url=self.server, params=data).json()
        if prune:
            for index, image in enumerate(response):
                response[index] = image["id"]
        return response
