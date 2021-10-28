import logging
from datetime import datetime, timezone

from marshmallow import Schema, validate
from marshmallow.fields import Email, String
from ruteni import configuration
from ruteni.api import WebApi
from ruteni.plugins.auth import AuthPair, register_identity_provider
from ruteni.plugins.cookie import set_cookie
from ruteni.plugins.groups import get_user_groups
from ruteni.plugins.passwords import PASSWORD_MAX_LENGTH, check_password
from ruteni.plugins.session import UserType
from ruteni.plugins.site import SITE_NAME
from ruteni.plugins.token import (
    MAX_CLIENT_ID_LENGTH,
    REFRESH_TOKEN_LENGTH,
    create_access_token,
    create_refresh_token,
    get_user_id_from_access_token,
    revoke_refresh_token,
    select_refresh_token,
)
from ruteni.utils.form import get_form
from starlette import status
from starlette.authentication import AuthCredentials, BaseUser
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

logger = logging.getLogger(__name__)

JWT_ISSUER: str = configuration.get("RUTENI_AUTH_JWT_ISSUER", default=SITE_NAME)
ACCESS_TOKEN_COOKIE_NAME: str = configuration.get(
    "RUTENI_AUTH_ACCESS_TOKEN_COOKIE_NAME", default="access_token"
)


# same code as in auth/session.py
class RuteniUser(BaseUser):
    def __init__(self, user: UserType) -> None:
        self.id = user["id"]
        self.email = user["email"]
        self.name = user["display_name"]
        self.locale = user["locale"]
        self.groups = user["groups"]

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.name


def authenticate(user: UserType) -> AuthPair:
    scopes = user["groups"] + ["authenticated"]
    return AuthCredentials(scopes), RuteniUser(user)


register_identity_provider("ruteni", authenticate)


class SignInSchema(Schema):
    email = Email(required=True)  # type: ignore
    password = String(required=True, validate=validate.Length(max=PASSWORD_MAX_LENGTH))
    client_id = String(
        required=True, validate=validate.Length(max=MAX_CLIENT_ID_LENGTH)
    )


async def signin(request: Request) -> Response:
    form = await get_form(request, SignInSchema)
    password_info = await check_password(form["email"], form["password"])

    if password_info is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user_info, access_token, refresh_token = await create_refresh_token(
        password_info.user_id, JWT_ISSUER, form["client_id"]
    )

    user = user_info.to_dict()
    user["provider"] = "ruteni"
    user["groups"] = await get_user_groups(user_info.id)

    result = {
        "access_token": access_token.claims,
        "refresh_token": refresh_token,
        "user": user,
    }
    logger.debug(f"signin response: {result}")

    response = JSONResponse(result)
    set_cookie(response, ACCESS_TOKEN_COOKIE_NAME, access_token.token)
    return response


class RefreshTokenSchema(Schema):
    refresh_token = String(
        required=True, validate=validate.Length(equal=2 * REFRESH_TOKEN_LENGTH)
    )


async def signout(request: Request) -> Response:
    form = await get_form(request, RefreshTokenSchema)

    access_token = request.cookies.get(ACCESS_TOKEN_COOKIE_NAME)
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # TODO: if the access token is expired, this will fail
    user_id = get_user_id_from_access_token(access_token, JWT_ISSUER)
    success = await revoke_refresh_token(user_id, form["refresh_token"])

    response = JSONResponse(success)
    response.delete_cookie(ACCESS_TOKEN_COOKIE_NAME)
    return response


async def refresh(request: Request) -> Response:
    form = await get_form(request, RefreshTokenSchema)

    # TODO: implement…
    raise NotImplementedError("FIXME")

    row = await select_refresh_token(form["refresh_token"])

    if row is None:
        # raise ServiceUserException("invalid-token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if row["disabled_reason"] is not None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        # raise ServiceUserException(
        #     "account-disabled",
        #     public=dict(reason=row["disabled_reason"]),
        #     private=dict(id=row["id"], info=disabled),
        # )

    if row["revoked_at"] is not None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        # raise ServiceUserException(
        #     "revoked-token",
        #     public=dict(at=row["revoked_at"]),
        #     private=dict(id=row["id"]),
        # )

    if row["expires_at"] < datetime.now(timezone.utc).astimezone():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        # raise ServiceUserException(
        #     "expired-token",
        #     public=dict(at=expires_at),
        #     private=dict(id=row["id"]),
        # )

    access_token = await create_access_token(
        row["id"],
        row["expires_at"],
        row["user_id"],
        JWT_ISSUER,
        row["client_id"],
    )

    response = JSONResponse({"access_token": access_token.claims})
    set_cookie(response, ACCESS_TOKEN_COOKIE_NAME, access_token.token)
    return response


api = WebApi("jauthn", 1)
api.add_route("signin", signin, methods=["POST"])
api.add_route("signout", signout, methods=["POST"])
api.add_route("refresh", refresh, methods=["POST"])

logger.info("loaded")
