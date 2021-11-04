# -*- coding: utf-8 -*-

from contextvars import ContextVar

from fastapi.responses import UJSONResponse
from fastapi.responses import HTMLResponse as _HTMLResponse, PlainTextResponse as _PlainTextResponse,\
    StreamingResponse as _StreamingResponse, FileResponse as _FileResponse

from hagworm.extend.struct import Result


REQUEST_ID_CONTEXT = ContextVar(r'request_id')


class Response(UJSONResponse):

    def __init__(self, content=None, status_code=200, *args, **kwargs):

        self._request_id = REQUEST_ID_CONTEXT.get()

        super().__init__(content, status_code, *args, **kwargs)

        self.raw_headers.append((b'x-request-id', self._request_id.encode(r'latin-1')))

    def render(self, content):

        return super().render(
            Result(data=content, request_id=self._request_id)
        )


class ErrorResponse(Response, Exception):

    def __init__(self, error_code, content=None, status_code=200, **kwargs):

        self._error_code = error_code

        Response.__init__(self, content, status_code, **kwargs)
        Exception.__init__(self, self.body.decode())

    def render(self, content):

        return UJSONResponse.render(
            self,
            Result(code=self._error_code, data=content, request_id=self._request_id)
        )


class HTMLResponse(_HTMLResponse):

    def __init__(self, content=None, status_code=200, *args, **kwargs):

        self._request_id = REQUEST_ID_CONTEXT.get()

        super().__init__(content, status_code, *args, **kwargs)

        self.raw_headers.append((b'x-request-id', self._request_id.encode(r'latin-1')))


class PlainTextResponse(_PlainTextResponse):

    def __init__(self, content=None, status_code=200, *args, **kwargs):

        self._request_id = REQUEST_ID_CONTEXT.get()

        super().__init__(content, status_code, *args, **kwargs)

        self.raw_headers.append((b'x-request-id', self._request_id.encode(r'latin-1')))


class StreamingResponse(_StreamingResponse):

    def __init__(self, content=None, status_code=200, *args, **kwargs):

        self._request_id = REQUEST_ID_CONTEXT.get()

        super().__init__(content, status_code, *args, **kwargs)

        self.raw_headers.append((b'x-request-id', self._request_id.encode(r'latin-1')))


class FileResponse(_FileResponse):

    def __init__(self, content=None, status_code=200, *args, **kwargs):

        self._request_id = REQUEST_ID_CONTEXT.get()

        super().__init__(content, status_code, *args, **kwargs)

        self.raw_headers.append((b'x-request-id', self._request_id.encode(r'latin-1')))
