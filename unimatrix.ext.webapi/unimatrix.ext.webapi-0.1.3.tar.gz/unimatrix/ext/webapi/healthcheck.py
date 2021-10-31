"""Declares request handlers for liveness and readyness
checks.
"""
from fastapi.responses import Response


async def ready(response: Response) -> Response:
    """Perform a readyness check and set status code ``204``
    on the HTTP response if the application is ready,
    else ``503``.
    """
    response.status_code = 204


async def live(response: Response) -> Response:
    """Perform a liveness check and set status code ``204``
    on the HTTP response if the application is live,
    else ``503``.
    """
    response.status_code = 204
