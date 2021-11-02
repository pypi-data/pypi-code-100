import argparse
from datetime import datetime
from pathlib import Path


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--to-csv",
        help="outputs dataframe to csv at given path",
        type=Path,
        required=False,
    )
    parser.add_argument(
        "--host",
        help="elasticsearch host to get the data from",
        type=str,
        required=False,
        default="localhost",
    )
    parser.add_argument(
        "--port",
        help="elasticsearch port",
        type=str,
        required=False,
        default="9200",
    )
    parser.add_argument(
        "--user",
        help="elasticsearch username",
        type=str,
        required=False,
        default="elastic",
    )
    parser.add_argument(
        "--password",
        help="elasticsearch password",
        type=str,
        required=False,
        default="changeme",
    )
    parser.add_argument("--index", help="elasticsearch index", type=str, required=True)
    parser.add_argument(
        "--range-start-epochs",
        help="used in a time range query to select only netflows after this datetime.\
            uses elasticsearch 'gte'. Default = 0",
        type=int,
        required=False,
        default=0,
    )
    parser.add_argument(
        "--range-end-epochs",
        help="used in a time range query to select only netflows before this datetime.\
            uses elasticsearch 'lte'. Default: current timestamp",
        type=int,
        required=False,
        default=int(datetime.now().timestamp()),
    )
    parser.add_argument(
        "--range-field",
        help="field used for range queries",
        type=str,
        required=False,
        default="timestamp",
    )
    return parser
