import logging

from marshmallow import Schema, validate
from marshmallow.fields import Email, String
from ruteni.api import WebApi
from ruteni.plugins.auth import AuthPair, register_identity_provider
from ruteni.plugins.groups import get_user_groups
from ruteni.plugins.passwords import PASSWORD_MAX_LENGTH, check_password
from ruteni.plugins.session import UserType, del_session_user, set_session_user
from ruteni.plugins.token import MAX_CLIENT_ID_LENGTH
from ruteni.plugins.users import get_user_by_id
from ruteni.utils.form import get_form
from starlette import status
from starlette.authentication import AuthCredentials, BaseUser
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse, Response

logger = logging.getLogger(__name__)


# same code as in auth/token.py
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

    if password_info is None:  # TODO: not clear what status code should be used
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user_info = await get_user_by_id(password_info.user_id)
    assert user_info
    user = user_info.to_dict()
    user["provider"] = "ruteni"
    user["groups"] = await get_user_groups(user_info.id)

    response = JSONResponse(user)
    set_session_user(request, user)
    return response


async def signout(request: Request) -> Response:
    del_session_user(request)
    return RedirectResponse(url="/")


api = WebApi("auth", 1)
api.add_route("signin", signin, methods=["POST"], name="signin")
api.add_route("signout", signout, methods=["GET"], name="signout")

logger.info("loaded")
