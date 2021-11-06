import logging

from ruteni.plugins.database import database, metadata
from ruteni.plugins.session import get_user_from_environ
from ruteni.plugins.socketio import sio
from ruteni.plugins.users import users
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, and_, func
from sqlalchemy_utils import IPAddressType

logger = logging.getLogger(__name__)

connections = Table(
    "connections",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("sid", String(28), nullable=False),
    Column("ip_address", IPAddressType, nullable=False),
    Column("user_id", Integer, ForeignKey(users.c.id), nullable=False),
    Column("opened_at", DateTime, nullable=False, server_default=func.now()),
    Column("closed_at", DateTime, default=None),
)


async def on_connect(sid: str, environ: dict[str, str]) -> bool:
    # async with sio.eio.session(sid) as session:
    #     session["username"] = username

    # get the current user
    user = get_user_from_environ(environ)
    if user is None:
        return False  # reject connection

    await database.execute(
        connections.insert().values(
            sid=sid, user_id=user["id"], ip_address=environ["REMOTE_ADDR"]
        )
    )
    logger.info(f"{user['name']} is connected")
    return True


async def on_disconnect(sid: str) -> None:
    # TODO: could there be identical sids for different connections over time?
    await database.execute(
        connections.update()
        .where(and_(connections.c.sid == sid, connections.c.closed_at.is_(None)))
        .values(closed_at=func.now())
    )
    logger.info(f"{sid}.disconnect")


sio.on("connect", on_connect)
sio.on("disconnect", on_disconnect)

logger.info("loaded")
