# -*- coding: utf-8 -*-

from starlette.types import Receive, Scope, Send
from fastapi.responses import UJSONResponse

from hagworm.extend.struct import Result


class Response(UJSONResponse):

    def render(self, content):

        return super().render(
            Result(data=content)
        )

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

        if r'request_id' in scope:
            self.raw_headers.append((b'x-request-id', scope[r'request_id'].encode(r'latin-1')))

        await super().__call__(scope, receive, send)


class ErrorResponse(Response, Exception):

    def __init__(self, error_code, content=None, status_code=200, **kwargs):

        self._error_code = error_code

        Response.__init__(self, content, status_code, **kwargs)
        Exception.__init__(self, self.body.decode())

    def render(self, content):

        return UJSONResponse.render(
            self,
            Result(code=self._error_code, data=content)
        )
