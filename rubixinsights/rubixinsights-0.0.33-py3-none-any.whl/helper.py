from typing import Callable
import datetime
import yaml
import boto3
import pandas as pd
from sqlalchemy import create_engine


def get_value_from_ssm(name: str, client: boto3.client) -> str:
    """Get secret value from AWS parameter store

    :param secret_name: [description]
    :type secret_name: str
    :param client: [description]
    :type client: boto3.client
    :return: [description]
    :rtype: str
    """
    response = client.get_parameter(
        Name=name,
        WithDecryption=True
    )

    value = response['Parameter']['Value']
    return value


def read_yaml(path: str) -> dict:
    """Read in configuration from yaml file

    :param path: path to yaml file
    :type path: str
    :return: config
    :rtype: dict
    """
    try:
        with open(path, 'r') as metadata:
            conf = yaml.safe_load(metadata)
    except yaml.YAMLError as e:
        print(e)
        raise
    except FileNotFoundError as e:
        print(f"File Not Found: {e}")
        raise
    return conf


def get_execution_dates(execution_date: datetime.date, attribution_window: int):
    """Generator function taking one execution_date and yielding a list of execution_dates with attribution in consideration

    :param execution_date: the specific date when data is pulled
    :type execution_date: str
    :param attribution_window: number of days of attribution
    :type attribution_window: int
    :yield: execution_date up to the beginning of the attribution window
    :rtype: datetime.date
    """
    # TODO. logic needs to be refined if the granularity is hourly not daily
    # if it is older than attribution_window, then no attribution run has to be considered
    beginning_of_attribution_window = datetime.date.today() - datetime.timedelta(attribution_window)

    if execution_date < beginning_of_attribution_window:
        yield execution_date
    else:
        for n in range(attribution_window):
            yield execution_date - datetime.timedelta(days=n)


def attribution_window(num_of_days: int):
    """Decorator to handle data source attribution window 

    :param pull_data_func: function to pull data from source
    :type pull_data_func: Callable[[datetime.date, str, dict], None]
    :return: a wrapper of pull_data_func
    :rtype: Callable[[datetime.date, str, dict], None]
    """
    def decorator(pull_data_func):
        def wrapper(execution_date, *args, **kwargs):
            for ed in get_execution_dates(execution_date, num_of_days):
                print(f"execution_date: {ed}")
                pull_data_func(ed, *args, **kwargs)
        return wrapper
    return decorator


def extract_components_from_execution_date(execution_date: datetime.date):
    year = execution_date.strftime("%Y")
    month = execution_date.strftime("%m")
    day = execution_date.strftime("%d")
    return year, month, day


def migrate_table(
    source_conn: str,
    target_conn: str,
    source_schema: str,
    source_table_name: str,
    target_schema: str,
    target_table_name: str,
    table_definition: dict
):
    """Copy postgres table from 

    :param source_conn: connection string of source postgres
    :type source_conn: str
    :param target_conn: connection string of target postgres
    :type target_conn: str
    :param source_schema: schema name of source postgres db
    :type source_schema: str
    :param source_table_name: table name of source postgres db
    :type source_table_name: str
    :param target_schema: schema name of target postgres db
    :type target_schema: str
    :param target_table_name: table name of target postgres db
    :type target_table_name: str
    :param table_definition: a mapping which key is the column name and value is the column type in sqlalchemy language
    :type schema: dict
    """
    data = pd.read_sql(
        sql=f"select * from {source_schema}.{source_table_name}",
        con=create_engine(source_conn.get_uri())
    )
    dtypes = table_definition
    # define data type
    data.to_sql(
        target_table_name,
        schema=target_schema,
        con=create_engine(target_conn.get_uri()),
        if_exists='replace',
        dtype=dtypes,
        index=False
    )
