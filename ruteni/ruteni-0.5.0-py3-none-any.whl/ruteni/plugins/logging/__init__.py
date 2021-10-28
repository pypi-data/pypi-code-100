import enum
import logging

import pyrfc3339
from ruteni import configuration
from ruteni.api import WebApi
from ruteni.plugins.database import database, metadata
from ruteni.plugins.users import users
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Table
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class Level(enum.Enum):
    trace = 1
    debug = 2
    info = 3
    warn = 4
    error = 5


logs = Table(
    "logs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(users.c.id)),
    Column("level", Enum(Level), nullable=False),
    Column("logger", String(255), nullable=False),
    Column("message", String, nullable=False),
    Column("timestamp", DateTime, nullable=False),
    Column("stacktrace", String),
)


async def log(request: Request) -> Response:
    """
    {
        "logs": [
            {
                "message": "name-update2",
                "level": <Level.warn: 4>,
                "logger": "registration-homepage",
                "timestamp": datetime.datetime(
                    2021, 10, 1, 21, 27, 55, 700000, tzinfo=datetime.timezone.utc
                ),
                "stacktrace": "    at HTMLInputElement.name-update (http://127.0.0.1:8000/static/components/registration-homepage/index.js:25:28)",
                "user_id": None,
            }
        ]
    }
    """
    body = await request.json()

    for log in body["logs"]:
        log["level"] = Level[log["level"]]
        log["timestamp"] = pyrfc3339.parse(log["timestamp"])
        if log["stacktrace"] == "":
            log["stacktrace"] = None
        log["user_id"] = request.user.id if request.user.is_authenticated else None

    await database.execute_many(logs.insert(), body["logs"])
    return Response()


api = WebApi("logging", 1)
api.add_route("log", log, methods=["POST"], name="log")

configuration.add_static_resource_mount("logging", __name__)

logger.info("loaded")
