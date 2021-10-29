import argparse

import compile_dcm2bids_config as cdc
from d2b.hookspecs import hookimpl


__version__ = "1.1.0"


@hookimpl
def register_commands(subparsers: argparse._SubParsersAction) -> None:
    _parser: argparse.ArgumentParser = subparsers.add_parser("compile")
    # configure the parser by going through compile-dcm2bids-config
    cdc._create_parser(_parser)
