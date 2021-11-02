import os
from dataclasses import dataclass
from typing import Iterator, Union

import pandas as pd

from mesiqi.core import connector_factory, get_logger, get_sqlalchemy_engine

logger = get_logger()

import snowflake.connector
import sqlalchemy


@dataclass
class Snowflake:

    name: str
    config: dict

    def __str__(self) -> str:
        return self.name

    def read(self, query: str) -> Union[Iterator, pd.DataFrame, None]:
        """Get iterator for Snowflake results

        Args:
            query (str): SQL string

        Returns:
            Iterator
        """

        engine = _create_engine(self.config)
        chunksize = self.config.get("chunksize", 10000)
        iterator = pd.read_sql(query, engine, chunksize=chunksize)
        engine.dispose()
        return iterator

    def write(self, df: pd.DataFrame, index: int = 0):
        """Writes pandas dataframe to snowflake table

        Args:
            df (pd.DataFrame): [description]
            index (int): chunk number

        Returns:
            str: 'DONE' or 'FAILED'
        """
        result = "FAILED"

        engine = get_sqlalchemy_engine(self.config)
        schema = config.get("schema", None)
        mode = "replace" if index == 0 else "append"
        temp_table = config.get("table", "test") + "_new"

        try:
            connection = engine.connect()
            df.to_sql(temp_table, con=engine, index=False, if_exists=mode)
            result = "DONE"
        finally:
            connection.close()
            engine.dispose()

        return result

    def get_version(self):
        """Query snowflake for current version number

        Returns:
            The version number
        """
        try:
            engine = _create_engine(self.config)
            connection = engine.connect()
            results = connection.execute("select current_version()").fetchone()
            return results[0]
        finally:
            connection.close()
            engine.dispose()


def register() -> None:
    """Register connector"""
    connector_factory.register("snowflake", Snowflake)


def _create_engine(config: dict):
    """Create SQLAlchemy engine

    Args:
        config (dict): credentials and config values

    Returns:
        engine: sqlalchemy engine
    """
    conn_string = config.get("connection_string", None)

    if conn_string:
        return sqlalchemy.create_engine(conn_string)

    return None
