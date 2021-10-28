from __future__ import annotations

from typing import Optional

from urlobject.path import URLPath

from . import EndpointTransform
from .urlns import URLNamespace


class WebStatic(URLNamespace):
    """
    Manage static resources
    """

    # url_format = "/static/{name}/v{version}"
    url_format = "/static/{name}"

    def __init__(
        self,
        name: str,
        version: int,
        *,
        transform: Optional[EndpointTransform] = None,
    ) -> None:
        ns = URLPath(WebStatic.url_format.format(name=name, version=version))
        super().__init__(
            "static", name, version, ns, transform=transform, include_in_schema=False
        )
