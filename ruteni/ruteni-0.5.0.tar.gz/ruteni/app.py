from __future__ import annotations

from pathlib import Path
from typing import Optional

from starlette.responses import FileResponse
from starlette.routing import Route
from urlobject.path import URLPath

from . import EndpointTransform, ROOTNS
from .api import WebApi
from .static import WebStatic
from .urlns import URLNamespace

APPNS = ROOTNS.add("app")


class WebApp(URLNamespace):
    """
    Manage a web app
    """

    url_format = "/app/{name}/"
    all_apps: list[WebApp] = []

    def __init__(
        self,
        name: str,
        version: int,
        *,
        transform: Optional[EndpointTransform] = None,
    ) -> None:
        ns = URLPath(WebApp.url_format.format(name=name, version=version))
        super().__init__(
            "app", name, version, ns, transform=transform, include_in_schema=False
        )
        self.api = WebApi(name, version, transform=transform)
        self.static = WebStatic(name, version, transform=transform)
        WebApp.all_apps.append(self)

    def add_static_file_route(self, path: URLPath, filename: Path) -> Route:
        return self.static.add_route(path, lambda request: FileResponse(filename))
