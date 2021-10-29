import dataclasses
import typing
import inspect
import types

import case
import sentinel

from . import errors

# TODO: Make abstract base route class?
# TODO: Implement state? Just let them define custom Router classes instead?

# Paths can be anything (e.g. str, int, float)
# Targets can also be anything
# ^ This is fine, however decorators only work for functions/classes

@dataclasses.dataclass
class Context:
    args:   tuple
    kwargs: dict

@dataclasses.dataclass
class Request:
    path:   typing.Any
    context: Context

@dataclasses.dataclass
class Route:
    path:   typing.Any
    target: typing.Any

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.path!r})'

    def matches(self, path) -> bool:
        return self.path == path # Crude check for now

@dataclasses.dataclass
class Middleware:
    handler: typing.Callable

@dataclasses.dataclass
class Router:
    routes: typing.List[Route] = dataclasses.field(default_factory = list)
    middlewares: typing.List[typing.Callable] = dataclasses.field(default_factory = list)

    def __call__(self, path):
        return self.resolve(path).target

    def __getitem__(self, path):
        return self.resolve(path)

    def __setitem__(self, path, target):
        self.routes.append \
        (
            Route \
            (
                path   = path,
                target = target,
            ),
        )

    def resolve(self, path):
        for route in self.routes:
            if route.matches(path):
                return route

        raise errors.NotFound

    def route(self, *paths, **state):
        routes = \
        [
            Route \
            (
                path   = path,
                target = sentinel.Missing,
            )
            for path in paths
        ]

        self.routes += routes

        def wrapper(target):
            if not hasattr(target, '_router'):
                target._router = self

            for route in routes:
                route.target = target

                target._router.routes.append(route)

            return target

        return wrapper

    def middleware(self, func):
        print('router middleware:', func)

        self.middlewares.append(func)

        return func

def route(*paths, **state):
    frame = inspect.currentframe()

    try:
        in_class = '__qualname__' in frame.f_back.f_locals
    finally:
        del frame

    if in_class:
        r = Router()
    else:
        r = get_router()

    return r.route(*paths, **state)

def router(cls):
    if not isinstance(cls, type):
        raise Exception

    cls._router = Router \
    (
        routes = \
        [
            route
            for value in cls.__dict__.values()
            if hasattr(value, '_router')
            for route in value._router.routes
        ],
    )

    return cls

def join(a, b):
    return f'{a}{b}'

def mount(path):
    def wrapper(target):
        if not hasattr(target, '_router'):
            raise Exception('Cant mount non-routified target')

        for route in target._router.routes:
            route.path = join(path, route.path)

        return target

    return wrapper

def middleware(func):
    print('middleware:', func)

    m = Middleware(handler = func)

    func._middleware = m

    print(m)

    frame = inspect.currentframe()

    try:
        in_class = '__qualname__' in frame.f_back.f_locals
    finally:
        del frame

    if in_class:
        r = Router()
    else:
        r = get_router()

    return r.middleware(func)

root = Router()

routers: typing.Dict[str, 'Router'] = dict \
(
    root = root,
)

def get_router(name = None):
    if name is None or name == 'root':
        return root

    routers.setdefault(name, Router())

    return routers[module]
