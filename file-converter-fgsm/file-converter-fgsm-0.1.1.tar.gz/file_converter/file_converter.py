"""Main module for the command line interface"""
import logging

import click

from file_converter.csv2json import csv2json
from file_converter.json2csv import json2csv


CONVERSION_HELP = (
    "'csv2json' to convert CSV files to JSON and "
    "'json2csv' for the other way around. Defaults to 'csv2json'."
)
INPUT_PATH_HELP = (
    "Path with the file (or folder with files) to be converted. "
    "Defaults to the current one."
)
OUTPUT_PATH_HELP = (
    "Output path to store the converted file(s). Defaults to the current one."
)
SEPARATOR_HELP = (
    "The separator used in the CSV file (when reading or writing) ."
    "When reading a folder, all files must have the same separator."
    r"Defaults to ',' (comma). In case of tab, write '\t'."
)
PREFIX_HELP = "Prefix added to the converted files. Defaults to empty string."


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format=("%(levelname)s: " "%(message)s"),
)


@click.command()
@click.option("--conversion", default="csv2json", help=CONVERSION_HELP)
@click.option("--input_path", default=".", help=INPUT_PATH_HELP)
@click.option("--output_path", default=".", help=OUTPUT_PATH_HELP)
@click.option("--separator", default=",", help=SEPARATOR_HELP)
@click.option("--prefix", default="", help=PREFIX_HELP)
def file_converter(
    conversion: str,
    input_path: str,
    output_path: str,
    separator: str,
    prefix: str,
) -> None:
    """Converts files from CSV to JSON and vice-versa"""
    if conversion == "csv2json":
        csv2json(
            input_path,
            output_path=output_path,
            separator=separator,
            prefix=prefix,
        )
    elif conversion == "json2csv":
        json2csv(
            input_path,
            output_path=output_path,
            separator=separator,
            prefix=prefix,
        )
    else:
        click.echo("Unknown conversion type. Try 'csv2json' or 'json2csv'.")
