import json
import logging
from base64 import b64decode
from typing import Any, Optional

import itsdangerous
from itsdangerous.exc import BadTimeSignature, SignatureExpired
from ruteni import configuration
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request, cookie_parser

logger = logging.getLogger(__name__)

USER_SESSION_NAME: str = configuration.get("RUTENI_USER_SESSION_NAME", default="user")
SECRET_KEY = configuration.get("RUTENI_SESSION_SECRET_KEY")
MAX_AGE = configuration.get(
    "RUTENI_SESSION_MAX_AGE", cast=int, default=2 * 7 * 24 * 60 * 60  # 2 weeks
)
COOKIE_NAME = configuration.get("RUTENI_SESSION_COOKIE_NAME", default="session")
SAME_SITE = configuration.get("RUTENI_SESSION_SAME_SITE", default="lax")

session_middleware = configuration.add_middleware(
    SessionMiddleware,
    https_only=not configuration.is_devel,
    max_age=MAX_AGE,
    same_site=SAME_SITE,
    secret_key=SECRET_KEY,
    session_cookie=COOKIE_NAME,
)

UserType = dict[str, Any]

signer = itsdangerous.TimestampSigner(SECRET_KEY)


def set_session_user(request: Request, user: UserType) -> None:
    request.session[USER_SESSION_NAME] = user


def del_session_user(request: Request) -> None:
    request.session.pop(USER_SESSION_NAME, None)


def get_session_user(request: Request) -> Optional[UserType]:
    return request.session.get(USER_SESSION_NAME, None)


def verify_and_decode_cookie(cookie: str) -> Optional[dict]:
    try:
        data = signer.unsign(cookie, max_age=MAX_AGE)
    except (BadTimeSignature, SignatureExpired):
        return None
    else:
        return json.loads(b64decode(data))


def get_user_from_cookie(cookie: str) -> Optional[UserType]:
    session = verify_and_decode_cookie(cookie)
    return (
        session[USER_SESSION_NAME]
        if session is not None and USER_SESSION_NAME in session
        else None
    )


def get_user_from_environ(environ: dict[str, str]) -> Optional[UserType]:
    if "HTTP_COOKIE" in environ:
        cookies = cookie_parser(environ["HTTP_COOKIE"])
        if COOKIE_NAME in cookies:
            return get_user_from_cookie(cookies[COOKIE_NAME])

    # in all other cases, no user was found
    return None


logger.info("loaded")
