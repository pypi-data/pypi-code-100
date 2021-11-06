from typing import Optional

from ruteni import configuration
from starlette.responses import Response

COOKIE_SECURE: bool = configuration.get(
    "RUTENI_COOKIE_SECURE",
    cast=bool,
    default=(not configuration.is_devel),
)
COOKIE_HTTPONLY: bool = configuration.get(
    "RUTENI_COOKIE_HTTPONLY", cast=bool, default=True
)
COOKIE_PATH: str = configuration.get("RUTENI_COOKIE_PATH", default="/")
COOKIE_DOMAIN: Optional[str] = configuration.get("RUTENI_COOKIE_DOMAIN", default=None)
COOKIE_SAMESITE: str = configuration.get("RUTENI_COOKIE_SAMESITE", default="lax")


def set_cookie(response: Response, name: str, value: str) -> None:
    response.set_cookie(
        name,
        value,
        path=COOKIE_PATH,
        domain=COOKIE_DOMAIN,
        secure=COOKIE_SECURE,
        httponly=COOKIE_HTTPONLY,
        samesite=COOKIE_SAMESITE,
    )
