from typing import List, Optional

from starlette.middleware.base import RequestResponseEndpoint
from starlette.routing import Route
from starlette.staticfiles import PathLike
from urlobject.path import URLPath

from . import EndpointTransform, configuration


class URLNamespace:
    def __init__(
        self,
        type: str,
        name: str,
        version: int,
        ns: URLPath,
        *,
        transform: Optional[EndpointTransform] = None,
        include_in_schema: bool = True,
    ) -> None:
        """
        from starlette.authentication import requires
        transform = requires(scopes, status_code, redirect)
        """
        self.type = type
        self.name = name
        self.version = version
        self.ns = ns
        self.transform = transform
        self.include_in_schema = include_in_schema
        self.urls: dict[str, str] = {}

    def add_route(
        self,
        path: URLPath,
        endpoint: RequestResponseEndpoint,
        *,
        methods: List[str] = None,
        name: Optional[str] = None,
    ) -> Route:
        real_endpoint = self.transform(endpoint) if self.transform else endpoint
        real_path = self.ns.add(path)
        if name:
            self.urls[name] = real_path
        configuration.add_route(
            real_path,
            real_endpoint,
            methods=methods,
            name=f"{self.name}-{self.version}-{self.type}-{name}" if name else None,
            include_in_schema=self.include_in_schema,
        )

    def add_file_route(
        self,
        path: URLPath,
        filename: PathLike,
        *,
        media_type: str = None,
        name: str = None,
    ) -> Route:
        return configuration.add_file_route(
            path=path, filename=filename, ns=self.ns, media_type=media_type, name=name
        )

    def url_for(self, name: str) -> Optional[str]:
        return self.urls.get(name, None)
