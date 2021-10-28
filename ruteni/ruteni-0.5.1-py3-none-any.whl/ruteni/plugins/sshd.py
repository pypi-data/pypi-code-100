import logging

from ruteni import configuration
from starlette.applications import Starlette
from paramiko import common, ServerInterface, Channel, PKey

logger = logging.getLogger(__name__)

# TODO: implement…
raise NotImplementedError("FIXME")


class Server(ServerInterface):
    def __init__(self) -> None:
        pass

    def check_channel_request(self, kind: str, chanid: int) -> int:
        # if kind == "session":
        return common.OPEN_SUCCEEDED

    def check_auth_publickey(self, username: str, key: PKey) -> int:
        return common.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username: str) -> str:
        return "publickey"

    def check_channel_exec_request(self, channel: Channel, command: str) -> bool:
        logger.debug(command)
        return True


class SSHd:
    def __init__(self) -> None:
        pass

    async def startup(self, starlette: Starlette) -> None:
        logger.info("started")

    async def shutdown(self, starlette: Starlette) -> None:
        logger.info("stopped")


sshd = SSHd()
configuration.add_service("sshd", sshd.startup, sshd.shutdown)

logger.info("loaded")
