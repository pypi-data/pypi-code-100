from __future__ import annotations

from typing import Optional

from urlobject.path import URLPath

from . import EndpointTransform, ROOTNS
from .urlns import URLNamespace

APINS = ROOTNS.add("api")


class WebApi(URLNamespace):
    """
    Manage a web API
    """

    url_format = "/api/{name}/v{version}"

    def __init__(
        self,
        name: str,
        version: int,
        *,
        transform: Optional[EndpointTransform] = None,
    ) -> None:
        ns = URLPath(WebApi.url_format.format(name=name, version=version))
        super().__init__("api", name, version, ns, transform=transform)
