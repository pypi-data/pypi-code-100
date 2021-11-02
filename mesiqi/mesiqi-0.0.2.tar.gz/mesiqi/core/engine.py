import logging
from typing import Callable

import sqlalchemy

from .logger import get_logger

logger = get_logger()


def get_sqlalchemy_engine(config: dict) -> Callable:
    conn_type = config["type"]
    logger.info(f"conn_type: {conn_type}")

    options = {"bigquery": create_bigquery_engine}

    return options.get(conn_type, create_default_engine)(config)


def create_default_engine(config: dict):
    return sqlalchemy.create_engine(config["connection_string"])


def create_bigquery_engine(config: dict):
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
            "client_email": config["client_email"],
            "private_key": config["private_key"],
            "token_uri": "https://oauth2.googleapis.com/token",
            "project_id": config["project_id"],
        }

        return sqlalchemy.create_engine("bigquery://", credentials_info=account_info)

    return sqlalchemy.create_engine("bigquery://", project=project_id)
