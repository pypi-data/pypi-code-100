import logging

from aiosmtpd.controller import Controller
from ruteni import configuration
from starlette.applications import Starlette

logger = logging.getLogger(__name__)

# TODO: implement…
raise NotImplementedError("FIXME")


class SMTPd:
    def __init__(self) -> None:
        self.controller = Controller()

    async def startup(self, starlette: Starlette) -> None:
        logger.info("started")

    async def shutdown(self, starlette: Starlette) -> None:
        logger.info("stopped")


smtpd = SMTPd()
configuration.add_service("smtpd", smtpd.startup, smtpd.shutdown)

logger.info("loaded")
