from fastapi import Response, status
from starlette.types import Message, Scope
from starlette.responses import JSONResponse, Response, StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from typing import Callable, Awaitable

from ..signatures.signature_validation import check_signature
import logging


logging.basicConfig(filename="MiddleWareLogs.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


urls_in_routers = set()

class RequestBody(Request):
    def __init__(self, scope: Scope, body: bytes) -> None:
        super().__init__(scope, self._receive)
        self._body = body
        self.request_completed = False

    async def _receive(self) -> Message:
        if self.request_completed:
            return {"type": "http.disconnect"}
        else:
            self.request_completed = True
            return {"type": "http.request", "body": self._body, "more_body": False}


class CustomMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.urls_in_router = urls_in_routers

    def add_router(router):
        for url in router.routes:
            urls_in_routers.add(url.path)

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[StreamingResponse]]):
        is_url_for_hmac = False
        body = await request.body()
        for url in urls_in_routers:
            if url in str(request.url.path):
                is_url_for_hmac = True
        client_signature = request.headers.get("signature")
        valid_signature = check_signature(client_signature, body)

        if (not is_url_for_hmac) or (valid_signature and is_url_for_hmac):
            # if valid_signature and is_url_for_hmac:
            request = RequestBody(request.scope, body)
            response = await call_next(request)
            return response
        else:
            response: Response
            response = JSONResponse(content={
                "error": "hmac_verification_failed",
                "message": "Invalid hmac header."
            },
                status_code=status.HTTP_401_UNAUTHORIZED
            )
            return response
