import logging
from dataclasses import dataclass
from typing import Callable
from uuid import UUID, uuid4

from starlette.datastructures import Headers
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from asgi_correlation_id.context import correlation_id, full_correlation_id

logger = logging.getLogger('asgi_correlation_id')


def is_valid_uuid(uuid_: str) -> bool:
    """
    Check whether a string is a uuid.
    """
    try:
        return bool(UUID(uuid_, version=4))
    except ValueError:
        return False


@dataclass()
class CorrelationIdMiddleware:
    app: ASGIApp
    uuid_length: int = 32
    validate_guid: bool = True
    header_name: str = 'Correlation-ID'

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)

        header_value = Headers(scope=scope).get(self.header_name.lower())

        if not header_value:
            id_value = uuid4().hex
        elif self.validate_guid and not is_valid_uuid(header_value):
            logger.warning('Generating new UUID after receiving invalid header value: %s', header_value)
            id_value = uuid4().hex
        else:
            id_value = header_value

        correlation_id.set(id_value[: self.uuid_length])
        full_correlation_id.set(id_value)
        self.sentry_extension(id_value)

        async def handle_outgoing_request(message: Message) -> None:
            if message['type'] == 'http.response.start':
                headers = {k.decode(): v.decode() for (k, v) in message['headers']}
                headers[self.header_name] = full_correlation_id.get()
                headers['Access-Control-Expose-Headers'] = self.header_name
                response_headers = Headers(headers=headers)
                message['headers'] = response_headers.raw

            await send(message)

        return await self.app(scope, receive, handle_outgoing_request)

    def __post_init__(self) -> None:
        """
        Load extensions on initialization.

        If Sentry is installed we want to propagate correlation IDs
        to Sentry events, and if Celery is installed we want to
        propagate correlation IDs into spawned tasks.
        """
        # Load Sentry extension if Sentry is installed
        self.sentry_extension: Callable[[str], None]
        try:
            import sentry_sdk  # noqa: F401

            from asgi_correlation_id.extensions.sentry import set_transaction_id

            self.sentry_extension = set_transaction_id
        except ImportError:
            self.sentry_extension = lambda correlation_id: None

        # Load Celery extension if Celery is installed
        try:
            import celery  # noqa: F401

            from asgi_correlation_id.extensions.celery import configure_correlation_ids_for_celery

            configure_correlation_ids_for_celery(self.sentry_extension, self.uuid_length)
        except ImportError:
            pass
