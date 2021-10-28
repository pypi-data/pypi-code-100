from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Callable, List, Sequence, Set, Union

from pkg_resources import resource_filename
from starlette.applications import Starlette
from starlette.config import Config
from starlette.middleware import Middleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import FileResponse
from starlette.routing import BaseRoute, Mount, Route
from starlette.staticfiles import PathLike, StaticFiles
from starlette.types import ASGIApp
from urlobject.path import URLPath

from .types import Callback, Service

# @todo https://nuculabs.dev/2021/05/18/fastapi-uvicorn-logging-in-production/
# logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

EndpointTransform = Callable[[RequestResponseEndpoint], RequestResponseEndpoint]

ROOTNS = URLPath("/")
STATICNS = ROOTNS.add("static")


class Configuration(Config):
    def __init__(self) -> None:
        super().__init__(os.environ.get("RUTENI_CONFIG", ".env"))
        self.routes: list[Union[Route, Mount]] = []
        self.middleware: list[Middleware] = []
        self.services: list[Service] = []
        self.static_dir = Path("/var/www/ruteni/static")

    def set(self, key: str, value: Any) -> None:
        self.environ[key] = value

    @property
    def env(self) -> str:
        return self.get("RUTENI_ENV", default="production")

    @property
    def is_devel(self) -> bool:
        return self.env == "development"

    @property
    def is_debug(self) -> bool:
        return self.get("RUTENI_DEBUG", cast=bool, default=False)

    def set_static_dir(self, static_dir: PathLike) -> Mount:
        # TODO: raise exception if in production
        self.static_dir = Path(static_dir)
        return self.add_static_mount("static", static_dir)

    def add_service(self, name: str, startup: Callback, shutdown: Callback) -> Service:
        service = Service(name=name, startup=startup, shutdown=shutdown)
        self.services.append(service)
        return service

    def add_middleware(self, cls: type, **options: Any) -> Middleware:
        middleware = Middleware(cls, **options)
        self.middleware.append(middleware)
        return middleware

    def add_route(
        self,
        path: URLPath,
        endpoint: RequestResponseEndpoint,
        *,
        ns: URLPath = ROOTNS,
        methods: List[str] = None,
        name: str = None,
        include_in_schema: bool = True,
    ) -> Route:
        route = Route(
            str(ns.add(path)),
            endpoint,
            methods=methods,
            name=name,
            include_in_schema=include_in_schema,
        )
        self.routes.append(route)
        return route

    def add_file_route(
        self,
        path: URLPath,
        filename: PathLike,
        *,
        ns: URLPath = ROOTNS,
        media_type: str = None,
        name: str = None,
    ) -> Route:
        endpoint: RequestResponseEndpoint = lambda request: FileResponse(
            filename, media_type=media_type
        )
        return self.add_route(path, endpoint, ns=ns, name=name, include_in_schema=False)

    def add_mount(
        self,
        path: URLPath,
        app: ASGIApp = None,
        routes: Sequence[BaseRoute] = None,
        name: str = None,
    ) -> Mount:
        mount = Mount(path, app, routes, name)
        self.routes.append(mount)
        return mount

    def add_static_mount(
        self,
        path: URLPath,
        directory: PathLike = None,
        packages: List[str] = None,
        html: bool = False,
        check_dir: bool = True,
        *,
        ns: URLPath = ROOTNS,
    ) -> Mount:
        return self.add_mount(
            ns.add(path),
            app=StaticFiles(
                directory=directory, packages=packages, html=html, check_dir=check_dir
            ),
        )

    def add_static_resource_mount(
        self,
        path: URLPath,
        name: str,
        packages: List[str] = None,
        html: bool = False,
        check_dir: bool = True,
    ) -> Mount:
        if not self.static_dir:
            directory = resource_filename(name, "www")
            return self.add_static_mount(path, directory, ns=STATICNS)

    def get_route_paths(self) -> Set[str]:
        return set(route.path for route in self.routes)


configuration = Configuration()


class Ruteni(Starlette):
    def __init__(self) -> None:
        super().__init__(
            debug=configuration.is_debug,
            on_startup=[self._start_services],
            on_shutdown=[self._stop_services],
            routes=configuration.routes,
            middleware=configuration.middleware,
        )
        self.shutdown_callbacks: list[Service] = []

    async def _start_services(self) -> None:
        try:
            for service in configuration.services:
                await service.startup(self)
                self.shutdown_callbacks.append(service)
        except BaseException:
            logger.exception("start")
            await self._stop_services()
            raise

    async def _stop_services(self) -> None:
        while len(self.shutdown_callbacks):
            service = self.shutdown_callbacks.pop()
            try:
                await service.shutdown(self)
            except Exception:
                logger.exception("stop")
