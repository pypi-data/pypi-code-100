import logging
from datetime import datetime
from typing import Optional

import eland
import pandas as pd
from elasticsearch import Elasticsearch


def bootstrap_elastic_client(
    es_host: str,
    es_port: int = 9200,
    use_ssl: bool = False,
    es_user: str = "",
    es_password: str = "",
) -> Elasticsearch:
    if use_ssl:
        return Elasticsearch(
            f"https://{es_user}:{es_password}@{es_host}:{es_port}",
            use_ssl=True,
            verify_certs=False,
            ssl_show_warn=False,
        )
    elif es_user and es_password:
        return Elasticsearch(f"http://{es_user}:{es_password}@{es_host}:{es_port}")
    else:
        return Elasticsearch(f"http://{es_host}:{es_port}")


def range_query(
    dataframe: eland.DataFrame,
    range_field: str = "timestamp",
    start_range: float = 0.0,
    end_range: float = datetime.now().timestamp(),
) -> Optional[eland.DataFrame]:
    if range_field in dataframe.columns:
        start_time_isoformat = convert_epochs_to_local_isoformat(start_range)
        end_time_isoformat = convert_epochs_to_local_isoformat(end_range)
        dataframe = dataframe.es_query(
            {
                "range": {
                    range_field: {
                        "gte": start_time_isoformat,
                        "lte": end_time_isoformat,
                    }
                }
            }
        )
        logging.critical(
            "from %s to %s: %s records"
            % (start_time_isoformat, end_time_isoformat, len(dataframe))
        )
        return dataframe
    else:
        return None


def convert_epochs_to_local_isoformat(epochs: float) -> str:
    return datetime.fromtimestamp(epochs).astimezone().isoformat()


def sort_dataframe_by_timestamp(
    eland_df: eland.DataFrame, range_field: str = "timestamp"
) -> pd.DataFrame:
    pandas_df = eland.eland_to_pandas(eland_df)
    pandas_df[range_field] = pd.to_datetime(pandas_df[range_field])
    pandas_df.sort_values(by=range_field, inplace=True)
    return pandas_df
