import logging
from pathlib import Path

import click

from .converter import (
    read_csv_file,
    read_json_file,
    save_to_csv_files,
    save_to_json_files,
)


logging.basicConfig(
    level="DEBUG",
    format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'",
)
logger = logging.getLogger(__name__)


@click.command()
@click.argument("type-module", type=click.Choice(['csv', 'json']))
@click.option(
    "--input",
    "-i",
    help="Path where the files will be loaded for conversion.",
    type=str,
)
@click.option(
    "--output",
    "-o",
    default="./",
    help="Path where the converted files will be saved.",
    type=str,
)
@click.option(
    "--delimiter",
    "-d",
    default=",",
    type=click.Choice([',', ';', ':', '\t']),
    help="Separator used to split the files.",
)
@click.option(
    "--prefix",
    "-p",
    prompt=True,
    prompt_required=False,
    default="file",
    help=(
        "Prefix used to prepend to the name of the converted file saved on disk."
        " The suffix will be a number starting from 0. ge: file_0.json."
    ),
)
def converter(
    type_module: str,
    input: str,
    output: str = "./",
    delimiter: str = ",",
    prefix: str = 'file',
) -> None:
    """
    Convert Single file or list of CSV files to json
    or json to convert json files to csv.
    """

    input_path = Path(input)
    output_path = Path(output)
    logger.info(f"Input path {input_path}")
    logger.info(f"Output path {output_path}")

    for p in [input_path, output_path]:
        if not (p.is_file() or p.is_dir()):
            raise TypeError(f"Not a valid path or file name. {p}")

    if type_module == 'csv':
        data = read_csv_file(source=input_path, delimiter=delimiter)
        save_to_json_files(data, output_path, prefix)
    elif type_module == 'json':
        data = read_json_file(source=input_path)
        save_to_csv_files(data, output_path, prefix, delimiter)

    logger.info("Finishing processing")
