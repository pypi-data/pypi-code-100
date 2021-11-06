import logging

from databases import Database
from ruteni import configuration
from sqlalchemy import MetaData
from starlette.applications import Starlette

logger = logging.getLogger(__name__)

metadata = MetaData()

DATABASE_URL = configuration.get("RUTENI_DATABASE_URL")
database = Database(DATABASE_URL)


async def startup(starlette: Starlette) -> None:
    if configuration.is_devel:
        from sqlalchemy import create_engine

        engine = create_engine(DATABASE_URL)
        # if engine.dialect.name == "sqlite":
        metadata.create_all(engine)

    await database.connect()
    logger.info("started")


async def shutdown(starlette: Starlette) -> None:
    await database.disconnect()
    logger.info("stopped")


configuration.add_service("database", startup, shutdown)

logger.info("loaded")
