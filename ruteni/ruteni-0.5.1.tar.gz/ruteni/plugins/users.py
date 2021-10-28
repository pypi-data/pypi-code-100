import logging
from typing import Callable, NamedTuple, Optional

from ruteni import configuration
from ruteni.api import WebApi
from ruteni.plugins.database import database, metadata
from ruteni.plugins.locale import locales
from ruteni.plugins.session import get_session_user
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    and_,
    event,
    func,
    text,
)
from sqlalchemy.engine.base import Connection
from sqlalchemy.sql import select
from sqlalchemy_utils import EmailType
from starlette.authentication import requires
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from urlobject.path import URLPath

logger = logging.getLogger(__name__)

ADMIN_USERNAME: str = configuration.get("RUTENI_ADMIN_USERNAME", default="admin")
ADMIN_EMAIL: str = configuration.get("RUTENI_ADMIN_EMAIL", default="admin")

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("display_name", String(32), nullable=False),
    Column("email", EmailType, nullable=False, unique=True),
    Column("locale_id", Integer, ForeignKey(locales.c.id), nullable=False),
    Column("added_at", DateTime, nullable=False, server_default=func.now()),
    Column("disabled_at", DateTime, default=None),
)

Index(
    "ix_users_email_not_disabled",
    users.c.email,
    unique=True,
    sqlite_where=users.c.disabled_at.is_(None),
    postgresql_where=users.c.disabled_at.is_(None),
)


def after_create(target: Table, connection: Connection, **kwargs):  # type: ignore
    connection.execute(
        text(
            "INSERT INTO %s (display_name,email,locale_id) VALUES ('%s','%s',1)"
            % (target.name, ADMIN_USERNAME, ADMIN_EMAIL)
        )
    )


event.listen(users, "after_create", after_create)


class UserInfo(NamedTuple):
    id: int
    display_name: str
    email: str
    locale: str

    def to_dict(self) -> dict:
        return dict(
            id=self.id,
            display_name=self.display_name,
            email=self.email,
            locale=self.locale,
        )


async def get_user_by_id(user_id: int) -> Optional[UserInfo]:
    row = await database.fetch_one(
        select([users, locales.c.code])
        .select_from(users.join(locales))
        .where(and_(users.c.id == user_id, users.c.disabled_at.is_(None)))
    )
    return (
        UserInfo(row["id"], row["display_name"], row["email"], row["code"])
        if row
        else None
    )


async def get_user_by_email(email: str) -> Optional[UserInfo]:
    row = await database.fetch_one(
        select([users, locales.c.code])
        .select_from(users.join(locales))
        .where(and_(users.c.email == email, users.c.disabled_at.is_(None)))
    )
    return (
        UserInfo(row["id"], row["display_name"], row["email"], row["code"])
        if row
        else None
    )


async def add_user(display_name: str, email: str, locale: str) -> UserInfo:
    locale_id = await database.fetch_val(
        select([locales.c.id]).where(locales.c.code == locale)
    )
    if locale_id is None:
        raise Exception(f"unknown locale {locale}")
    user_id = await database.execute(
        users.insert().values(
            display_name=display_name,
            email=email,
            locale_id=locale_id,
        )
    )
    return UserInfo(user_id, display_name, email, locale)


class UnknownUserException(Exception):
    def __init__(self, user_id: int) -> None:
        super().__init__(f"unknown user ID {user_id}")
        self.user_id = user_id


async def assert_user_exists(user_id: int) -> None:
    if await get_user_by_id(user_id) is None:
        raise UnknownUserException(user_id)


@requires("authenticated")
async def user_info(request: Request) -> Response:
    return JSONResponse(get_session_user(request))


UserTest = Callable[[int], bool]


class UserAccessMixin:
    "# TODO: abstract class?"

    def __init__(self, accessible_to: UserTest) -> None:
        self.accessible_to = accessible_to


api = WebApi("user", 1)
api.add_route(URLPath("info"), user_info, methods=["GET"], name="info")

logger.info("loaded")
