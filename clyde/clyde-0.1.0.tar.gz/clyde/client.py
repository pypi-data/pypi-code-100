import attr

import functools

from . import models
from . import datastructures

class Client(object):
    def __init__(self, app, session):
        self.app     = app
        self.session = session
        self.operations = []

        self.state = datastructures.State()

        for route in self.app.router.routes:
            for method in route.methods:
                name = f'{method.lower()}_{route.name}' if len(route.methods) > 1 else route.name

                # scope = models.Scope \
                # (
                #     method = method,
                #     # name   = name,
                # )

                operation = models.Operation \
                (
                    method = method,
                    name   = name,
                    route  = route,
                )

                self.operations.append(operation)

                endpoint = functools.wraps(route.endpoint)(functools.partial(self.__call__, method, route))

                setattr(self, name, endpoint)

    def __call__(self, method, route, *args, **kwargs):
        request = route.endpoint(*args, **kwargs)

        if request is None:
            request = models.Request()

        # request.method   = scope.method
        request.method   = method
        request.url      = route.path
        request.app      = self.app
        request.client   = self
        # request.response = self.app.response / response should be on APIRoute

        # print(request, type(request))

        # prepared_request = self.session.prepare_request(request)

        # prepared_request.url = prepared_request.url.format(request.path_params)

        call_next = lambda request, self=self: self.session.send(self.session.prepare_request(request))

        # def container(session):
        #     def call_next(request):
        #         request.url = request.url.format(request.path_params)
        #
        #         prepared_request = session.prepare_request(request)
        #
        #         print(prepared_request, prepared_request.url, request.path_params)
        #
        #         return session.send(prepared_request)
        #
        #     return call_next

        # call_next = container(self.session)

        for middleware in reversed(self.app.middleware):
            call_next = functools.partial(middleware, call_next = call_next)

        response = call_next(request)

        if (parser := request.response or self.app.response):
            response = parser(response)

        return response

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}({repr(str(self.session.base_url))})>'
