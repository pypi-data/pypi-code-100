import logging

from pkg_resources import resource_filename
from ruteni import configuration
from urlobject.path import URLPath

from socketio import ASGIApp, AsyncRedisManager, AsyncServer

logger = logging.getLogger(__name__)


USE_REDIS: bool = configuration.get(
    "RUTENI_SOCKETIO_USE_REDIS", cast=bool, default=False
)
PATH: URLPath = configuration.get(
    "RUTENI_SOCKETIO_PATH", cast=URLPath, default="/socket.io"
)

if USE_REDIS:
    from ruteni.plugins.redis import REDIS_URL

    client_manager = AsyncRedisManager(REDIS_URL)
else:
    client_manager = None

sio = AsyncServer(async_mode="asgi", client_manager=client_manager)
app = ASGIApp(sio, socketio_path="")
configuration.add_mount(PATH, app)

configuration.add_static_resource_mount("socketio", __name__)

logger.info("loaded")
