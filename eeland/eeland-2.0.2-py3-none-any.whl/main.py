import argparse
import datetime
import logging
import os
import pathlib
from distutils.util import strtobool
from typing import Optional

import eland

from eeland import cli, utils


def setup_logging() -> None:
    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=os.environ.get(key="LOG_LEVEL", default="CRITICAL").upper(),
    )


def main(parser: Optional[argparse.ArgumentParser] = None) -> None:
    setup_logging()
    if parser:
        logging.debug("cli mode")
        args = parser.parse_args()
    else:
        logging.debug("env variable mode")
        parser = cli.setup_parser()
        args = parser.parse_args(
            [
                "--index",
                os.environ["ES_INDEX"],
                "--host",
                os.environ.get("ES_HOST", "localhost"),
                "--port",
                os.environ.get("ES_PORT", "9200"),
                "--user",
                os.environ.get("ES_USER", "elastic"),
                "--password",
                os.environ.get("ES_PASSWORD", "changeme"),
                "--range-start-epochs",
                os.environ.get("ES_RANGE_START", str(0)),
                "--range-end-epochs",
                os.environ.get(
                    "ES_RANGE_END", str(datetime.datetime.now().timestamp())
                ),
                "--range-field",
                os.environ.get("ES_RANGE_FIELD", "timestamp"),
                "--to-csv",
                os.environ.get("OUTPUT_CSV", "data.csv"),
                "--use-ssl",
                os.environ.get("ES_USE_SSL", "False"),
            ]
        )
    es_client = utils.bootstrap_elastic_client(
        es_host=args.host,
        es_port=args.port,
        es_user=args.user,
        es_password=args.password,
        use_ssl=strtobool(args.use_ssl),
    )
    dataframe = eland.DataFrame(es_client, args.index)
    if args.range_start_epochs or args.range_end_epochs:
        eland_dataframe = utils.range_query(
            dataframe=dataframe,
            range_field=args.range_field,
            start_range=args.range_start_epochs,
            end_range=args.range_end_epochs,
        )
        if eland_dataframe:
            sorted_dataframe = utils.sort_dataframe_by_timestamp(
                eland_df=eland_dataframe, range_field=args.range_field
            )
    logging.debug(sorted_dataframe)
    if args.to_csv:
        logging.debug("storing records in %s", pathlib.Path(args.to_csv).resolve())
        sorted_dataframe.to_csv(args.to_csv)


def run_cli() -> None:
    parser = cli.setup_parser()
    main(parser=parser)


if __name__ == "__main__":
    main()
