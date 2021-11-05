import time
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware


class TraceIdProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        request.state.trace_id = str(uuid4())
        request.state.time_started = start_time

        response = await call_next(request)

        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
