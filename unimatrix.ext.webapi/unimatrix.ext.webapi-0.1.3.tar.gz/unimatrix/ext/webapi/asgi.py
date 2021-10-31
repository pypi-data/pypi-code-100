"""Declares :class:`Application`."""
import logging
import os

import fastapi
import unimatrix.runtime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi.responses import JSONResponse
from ioc.exc import UnsatisfiedDependency
from starlette.middleware.trustedhost import TrustedHostMiddleware
from unimatrix.conf import settings
from unimatrix.ext import crypto
from unimatrix.ext import jose
from unimatrix.ext.model.exc import CanonicalException
from unimatrix.ext.model.exc import FeatureNotSupported

from .exceptions import UpstreamServiceNotAvailable
from .exceptions import UpstreamConnectionFailure
from .healthcheck import live as liveness_handler
from .healthcheck import ready as readyness_handler


class Application(fastapi.FastAPI):
    """Provides the ASGI interface to handle requests."""
    cors_max_age: int = 600
    logger: logging.Logger = logging.getLogger('unimatrix.ext.webapi')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('redoc_url', getattr(settings, 'REDOC_URL', '/docs'))
        kwargs.setdefault('docs_url', getattr(settings, 'DOCS_URL', '/ui'))
        kwargs.setdefault('openapi_url',
            getattr(settings, 'OPENAPI_URL', '/openapi.json')
        )
        kwargs.setdefault('root_path', os.getenv('HTTP_MOUNT_PATH'))

        # Configure the default exception handlers for the errors specified by
        # the Unimatrix Framework.
        exception_handlers = kwargs.setdefault('exception_handlers', {})
        exception_handlers.update({
            CanonicalException: self.canonical_exception,
            ConnectionError: self.canonical_exception,
            UnsatisfiedDependency: self.canonical_exception
        })

        # Remove the additional variables that we added to prevent them from
        # being passed to the fastapi.FastAPI.
        allowed_hosts = kwargs.pop('allowed_hosts', None)

        # Check if debug endpoints are enabled
        enable_debug_endpoints = kwargs.pop('enable_debug_endpoints', False)

        super().__init__(*args, **kwargs)

        # Add standard health-check routes. The initial use case here was
        # Kubernetes.
        self.add_api_route(
            '/.well-known/health/live',
            liveness_handler,
            name='live',
            status_code=204,
            tags=['Health'],
            methods=['GET'],
            response_description = "The service is live.",
            responses={
                '503': {'description': "The service is not live."},
            }
        )
        self.add_api_route(
            '/.well-known/health/ready',
            readyness_handler,
            name='ready',
            tags=['Health'],
            methods=['GET'],
            status_code=204,
            response_description = "The service is ready.",
            responses={
                '503': {'description': "The service is not ready."},
            }
        )

        # Ensure that the Unimatrix startup and teardown functions are invoked
        # when spawning a new ASGI application.

        @self.on_event('startup')
        async def on_startup(): # pylint: disable=unused-variable
            await unimatrix.runtime.on('boot') # pragma: no cover

        @self.on_event('shutdown')
        async def on_shutdown(): # pylint: disable=unused-variable
            await unimatrix.runtime.on('shutdown') # pragma: no cover

        # Add mandatory middleware to the application.
        self.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=(
                allowed_hosts or getattr(settings, 'HTTP_ALLOWED_HOSTS', [])
            )
        )

        # Enable CORS based on the environment variables and/or settings
        # module.
        self.enable_cors(
            allow_origins=settings.HTTP_CORS_ALLOW_ORIGINS,
            allow_credentials=settings.HTTP_CORS_ALLOW_CREDENTIALS,
            allow_methods=settings.HTTP_CORS_ALLOW_METHODS,
            allow_headers=settings.HTTP_CORS_ALLOW_HEADERS,
            expose_headers=settings.HTTP_CORS_EXPOSE_HEADERS,
            max_age=settings.HTTP_CORS_TTL
        )

        # Add debug handlers if the debug endpoints are enabled.
        if enable_debug_endpoints:
            debug = fastapi.APIRouter()

            @debug.post('/token', response_class=PlainTextResponse)
            async def create_bearer_token(dto: dict) -> str:
                """Create a JWT with the claims provided in the request body.
                For development purposes only.
                """
                jwt = await jose.jwt(dto, signer=crypto.get_signer())
                return bytes.decode(bytes(jwt))

            self.include_router(debug, prefix='/debug', tags=['Debug'])

    async def canonical_exception(self, request, exception):
        """Handles a canonical exception to a standard error message format."""
        if isinstance(exception, ConnectionRefusedError):
            kwargs = {}
            return await self.canonical_exception(
                request,
                UpstreamServiceNotAvailable(**kwargs),
            )
        elif isinstance(
            exception,
            (BrokenPipeError, ConnectionResetError, ConnectionAbortedError)
        ):
            kwargs = {}
            return await self.canonical_exception(
                request,
                UpstreamConnectionFailure(**kwargs),
            )
        elif isinstance(exception, UnsatisfiedDependency):
            return await self.canonical_exception(
                request, FeatureNotSupported()
            )
        elif isinstance(exception, CanonicalException):
            if exception.http_status_code >= 500:
                exception.log(self.logger.exception)
            return JSONResponse(
                status_code=exception.http_status_code,
                content=exception.as_dict()
            )
        else:
            raise NotImplementedError

    async def create_access_token(self) -> str:
        """Create a JWT using the default secret key configured for the
        application.
        """

    def enable_cors(self,
        allow_origins: list = None,
        allow_credentials: bool = False,
        allow_methods: list = None,
        allow_headers: list = None,
        expose_headers: list = None,
        max_age: int = None
    ):
        """Enables and configures Cross-Origin Resource Sharing (CORS)."""
        self.add_middleware(
            CORSMiddleware,
            allow_origins=allow_origins or [],
            allow_credentials=allow_credentials,
            allow_methods=allow_methods or [],
            allow_headers=allow_headers or [],
            expose_headers=expose_headers or [],
            max_age=max_age or self.cors_max_age
        )
