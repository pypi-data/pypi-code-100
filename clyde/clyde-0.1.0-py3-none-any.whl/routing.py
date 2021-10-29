import starlette.routing
import attr
import parse
import pydantic

import functools
import types

from . import enums
from . import utils

from typing import Callable, List, Set, Optional, Sequence

class Route(pydantic.BaseModel):
    path:     str
    endpoint: Callable
    methods:  Set[str]
    name:     str

    @pydantic.root_validator(pre=True)
    def validate_name(cls, values):
        if values.get('name') is None:
            values['name'] = utils.get_name(values['endpoint'])

        return values

# @attr.s(auto_attribs = True, repr=False)
# @attr.s(auto_attribs = True)
# class Route(object):
#     path:     str
#     endpoint: Callable = attr.ib(repr=False)
#     methods:  Set[str] = {enums.Method.GET}
#     name:     Optional[str] = None
#
#     def __attrs_post_init__(self) -> None:
#         if self.name is None:
#             self.name = utils.get_name(self.endpoint)

    # def __repr__(self) -> str:
    #     return f'{self.__class__.__name__}({self.path!r}, methods={self.methods})'

    # def matches(self, path: str, method: Optional[str] = None) -> bool:
    #     return self.parse(path) is not None and (method is not None and method.lower() == self.method.lower())
    #
    # def parse(self, path: str):
    #     return (result := parse.parse(self.path, path)) and result.named
    #
    # def path_for(self, **kwargs):
    #     return self.path.format(**kwargs)

# class Mount(starlette.routing.Mount):
# class Mount()
#     def __repr__(self) -> str:
#         return f'{self.__class__.__name__}({self.path!r}, routes={self.routes})'

class RouterMeta(type):
    def __new__(metacls, name, bases, attrs):
        cls = super().__new__(metacls, name, bases, attrs)

        for method in enums.Method:
            def decorator(method):
                def wrapper(self, *args, **kwargs):
                    return self.route(*args, **kwargs, methods={method})

                return wrapper

            setattr(cls, method.lower(), decorator(method))

        return cls

class Router(object, metaclass = RouterMeta):
    routes: List[Route]
    # prefix: Optional[str]

    def __init__(self, routes: Sequence[Route] = None):
        self.routes = [] if routes is None else list(routes)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(routes={self.routes})'

    # def match(self, method: str, path: str):
    #     ...

    def route(self, path: str, **kwargs):
        def decorator(endpoint):
            route = Route \
            (
                path     = path,
                endpoint = endpoint,
                **kwargs,
            )

            self.routes.append(route)

            return endpoint

        return decorator

    def mount(self, prefix: Optional[str] = None):
        return self.__class__ \
        (
            routes = \
            [
                Route \
                (
                    path     = (prefix or '') + route.path,
                    endpoint = route.endpoint,
                    methods  = route.methods,
                    name     = route.name,
                )
                for route in self.routes
            ],
        )

    def include(self, router):
        self.routes.extend(router.routes)
