import pydantic
import requests

import functools
import typing

from . import models
from . import client
from . import enums
from . import routing
from . import sessions
from . import datastructures

class SalientMeta(type):
    def __new__(metacls, name, bases, attrs):
        cls = super().__new__(metacls, name, bases, attrs)

        for method in enums.Method:
            def decorator(method):
                def wrapper(self, *args, **kwargs):
                    return self.route(method, *args, **kwargs)

                return wrapper

            setattr(cls, method.lower(), decorator(method))

        return cls

class Salient(object, metaclass=SalientMeta):
    def __init__(self, routes=None, response=lambda response: response.json()):
        self.middleware = []
        self.router = routing.Router(routes=routes)
        self.state = datastructures.State()
        self.response = response

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(router={self.router})'

    def middleware(self, func):
        self.middleware.append(func)

        return func

    def route(self, method: str, path: str, name: typing.Optional[str] = None, response = None):
    # def route(self, *args, **kwargs):
        def decorator(func):
            @pydantic.validate_arguments
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                request = func(*args, **kwargs)

                if request is None:
                    request = models.Request()

                request.method   = method
                request.url      = path
                # request.app      = self
                # request.response = response

                return request

            route = routing.Route \
            (
                path     = path,
                endpoint = wrapper,
                method   = method,
                name     = name or func.__name__,
            )

            self.router.routes.append(route)

            return wrapper

        return decorator

    def client(self, base_url: str, **kwargs):
        session = sessions.BaseUrlSession()

        session.base_url = base_url

        return client.Client \
        (
            self,
            session,
        )

    def include(self, *args, **kwargs):
        self.router.include(*args, **kwargs)
