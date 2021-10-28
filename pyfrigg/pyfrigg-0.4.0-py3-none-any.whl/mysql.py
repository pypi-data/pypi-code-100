import mysql.connector
import pandas as pd
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel("WARNING")


class Client:
    """
    MySQL client
    """

    def __init__(self, host: str, user: str, password: str) -> None:
        self._host = host
        self._user = user
        self._password = password

    def query(self, query: str, database: str) -> pd.DataFrame:
        """
        Return pandas.DataFrame from query at database

        :param query: query to execute
        :database: database to execute query at
        """
        try:
            with mysql.connector.connect(
                host=self._host,
                user=self._user,
                passwd=self._password,
                database=database,
            ) as connect:
                return pd.read_sql_query(query, connect)
        except mysql.connector.Error as error:
            LOGGER.warning(
                f"Got error while executing query\n{query}\nat database {database}:\n{error}."
            )
