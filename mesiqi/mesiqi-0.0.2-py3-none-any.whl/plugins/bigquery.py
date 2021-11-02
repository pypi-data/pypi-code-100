from dataclasses import dataclass
from typing import Iterator, Union

import pandas as pd
import json
import sqlalchemy
from google.cloud import bigquery
from google.oauth2 import service_account

from mesiqi.core import connector_factory, get_logger, get_sqlalchemy_engine

logger = get_logger()


@dataclass
class BigQuery:

    name: str
    config: dict

    def __str__(self) -> str:
        return self.name

    def read(self) -> Union[Iterator, pd.DataFrame, None]:
        """Get iterator for BigQuery results

        Args:
            query (str): SQL string

        Returns:
            Iterator
        """

        engine = _create_engine(self.config)
        chunksize = self.config.get("chunksize", 10000)
        iterator = pd.read_sql(self.config["query"], engine, chunksize=chunksize)
        engine.dispose()
        return iterator

    def write(self, df: pd.DataFrame, idx: int = 0):
        client = _bigquery_get_client(self.config)
        temp_table = self.config.get("table", "test") + "_NEW"

        job_config = bigquery.LoadJobConfig(
            schema=self.config.get("schema", None),
            write_disposition="WRITE_TRUNCATE" if idx == 0 else "WRITE_APPEND",
        )
        job = client.load_table_from_dataframe(df, temp_table, job_config=job_config)
        return job.result().state

    def delete_table(self, table: str):
        """[summary]

        Args:
            table (str): [description]

        Returns:
            str: 'DONE' or 'FAILED'
        """
        client = _bigquery_get_client(self.config)
        try:
            res = client.delete_table(table, not_found_ok=True)
            logger.info(res)
            return "DONE"
        except:
            return "FAILED"


def register() -> None:
    """Register connector"""
    connector_factory.register("bigquery", BigQuery)


def _create_engine(config: dict):
    """Create Bigquery SQLAlchemy engine

    Args:
        config (dict): credentials and config values

    Returns:
        engine: sqlalchemy engine
    """
    token = config.get("token", None)
    project_id = config.get("project_id", None)
    client_email = config.get("client_email", None)
    private_key = config.get("private_key", None)

    if token:
        if type(token) == str:
            return sqlalchemy.create_engine("bigquery://", credentials_path=token)

        if type(token) == dict:
            return sqlalchemy.create_engine(
                "bigquery://", credentials_info=json.loads(token)
            )

    if private_key and client_email and project_id:
        account_info = {
            "type": "service_account",
            "client_email": client_email,
            "private_key": private_key,
            "token_uri": "https://oauth2.googleapis.com/token",
            "project_id": project_id,
        }

        credentials = service_account.Credentials.from_service_account_info(
            account_info
        )

        return sqlalchemy.create_engine("bigquery://", credentials_info=account_info)

    return sqlalchemy.create_engine("bigquery://", project=project_id)


def _bigquery_get_client(config: dict):
    token = config.get("token", None)
    project_id = config.get("project_id", None)
    client_email = config.get("client_email", None)
    private_key = config.get("private_key", None)

    if token:
        if type(token) == str:
            credentials = service_account.Credentials.from_service_account_file(token)
            return bigquery.Client(credentials=credentials, project=project_id)

        if type(token) == dict:
            credentials = service_account.Credentials.from_service_account_info(
                json.loads(token)
            )
            return bigquery.Client(credentials=credentials, project=project_id)

    if private_key and client_email and project_id:
        account_info = {
            "type": "service_account",
            "client_email": config["client_email"],
            "private_key": config["private_key"],
            "token_uri": "https://oauth2.googleapis.com/token",
        }
        credentials = service_account.Credentials.from_service_account_info(
            account_info
        )
        return bigquery.Client(credentials=credentials, project=project_id)

    return bigquery.Client()
