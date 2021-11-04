from dependency_injector.providers import Provider
from flask import Flask

from .command_handler.command_handler import CommandHandler
from .container import Container
from .routes.index import Index


class RouteRegistry:
    def __init__(self, container: Container):
        self.__routes = {
            "/pithos/v1/projects/get": container.Route_GetProjects,
            "/pithos/v1/project_meta/get": container.Route_GetProjectMeta,
            "/pithos/v1/solutions/get": container.Route_GetSolutions,
            # Pass all other routes to dashboard to let react handle the routing
            "/<path:text>": Index.as_view(name="/catch"),
            "/": Index.as_view(name="/"),
        }

        self.__request_handler = container.RequestHandler()

    def register_routes(self, app: Flask):
        for route_key in self.__routes.keys():
            route = self.__routes[route_key]

            if isinstance(route, Provider):
                route = route()

            if isinstance(route, CommandHandler):
                view_function = self.__request_handler.get_view_function(route)
            else:
                view_function = route

            app.add_url_rule(route_key, view_func=view_function)
