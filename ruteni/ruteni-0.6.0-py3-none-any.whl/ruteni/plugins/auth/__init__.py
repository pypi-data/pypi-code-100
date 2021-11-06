import logging
from typing import Callable, Tuple

from pkg_resources import resource_filename
from ruteni import ROOTNS, configuration
from ruteni.plugins.security import ContentSecurityPolicy, add_html_file_route
from ruteni.plugins.session import UserType, get_session_user
from starlette.applications import Starlette
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    BaseUser,
    UnauthenticatedUser,
)
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import Request

logger = logging.getLogger(__name__)

AuthPair = Tuple[AuthCredentials, BaseUser]
AuthFunc = Callable[[UserType], AuthPair]

providers: dict[str, AuthFunc] = {}


def register_identity_provider(name: str, func: AuthFunc) -> None:
    providers[name] = func


class SessionAuthenticationBackend(AuthenticationBackend):
    async def authenticate(self, request: Request) -> AuthPair:
        user = get_session_user(request)
        if user:
            for provider, func in providers.items():
                if user["provider"] == provider:
                    return func(user)
            logger.warn(f'unknown identity provider: {user["provider"]}')
        return AuthCredentials(), UnauthenticatedUser()


async def startup(starlette: Starlette) -> None:
    if len(providers) == 0:
        logger.warn("no identity provider was added with register_identity_provider")
    logger.info("started")


async def shutdown(starlette: Starlette) -> None:
    logger.info("stopped")


content_security_policy = ContentSecurityPolicy(
    script=True, connect=True, style=True, img=True
)

add_html_file_route(
    "ap/signin",
    resource_filename(__name__, "/resources/index.html"),
    content_security_policy,
    ns=ROOTNS,
)

configuration.add_static_resource_mount("auth", __name__)

configuration.add_service("auth", startup, shutdown)

configuration.add_middleware(
    AuthenticationMiddleware, backend=SessionAuthenticationBackend()
)

logger.info("loaded")
