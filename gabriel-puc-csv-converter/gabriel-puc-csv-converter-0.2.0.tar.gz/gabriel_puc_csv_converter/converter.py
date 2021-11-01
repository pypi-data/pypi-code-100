import csv
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Tuple


logger = logging.getLogger(__name__)


def _load_csv_file(filepath: Path, delimiter: str) -> List[Dict[str, Any]]:
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        return list(reader)


def read_csv_file(
    source: Path, delimiter: str
) -> Tuple[List[Dict[str, Any]], ...]:
    """Load csv files from disk.

    Args:
        source (Path): Path of a single csv file or a directory containing csv files.
        delimiter (str): Separator for columns in csv.

    Return:
        tuple: tuple of list of dicts.
    """
    if source.is_file():
        logger.info("Reading single file %s", source)
        return (_load_csv_file(filepath=source, delimiter=delimiter),)

    logger.info("Reading all files within subdirectory %s", source)
    data = tuple(
        [
            _load_csv_file(filepath=name, delimiter=delimiter)
            for name in source.iterdir()
        ]
    )
    return data


def read_json_file(source: Path) -> Tuple[List[Dict[str, Any]], ...]:
    """Load json files from disk.

    Args:
        source (Path): Path of a single json file or a directory containing json files.

    Return:
        tuple: tuple of list of dicts.
    """
    if source.is_file():
        logger.info("Reading single file %s", source)
        return (json.load(open(source)),)

    logger.info("Reading all files within subdirectory %s", source)
    data = tuple([json.load(open(name)) for name in source.iterdir()])
    return data


def save_to_json_files(
    csvs: Tuple[List[Dict[str, Any]], ...],
    output_path: Path,
    prefix: str = 'file',
) -> None:
    """Save datas to Disk.

    Args:
        csvs (tuple): Tuple with list of dicts that will be converted
        output_path (Path): Path where to save the json files
        file_names (str): Name of files. If nothing is given it will
    """
    i = 0
    while i < len(csvs):
        file_name = f"{prefix}_{i}.json"
        logger.info("Saving file %s in folder %s", file_name, output_path)

        data: List[Dict[str, Any]] = csvs[i]
        json.dump(data, open(output_path.joinpath(file_name), 'w'), indent=4)
        i += 1


def save_to_csv_files(
    jsons: Tuple[List[Dict[str, Any]], ...],
    output_path: Path,
    prefix: str = 'file',
    delimiter: str = ',',
) -> None:
    """Save datas to Disk.

    Args:
        jsons (tuple): Tuple with list of dicts that will be converted
        output_path (Path): Path where to save the json files
        file_names (str): Name of files. If nothing is given it will
    """
    i = 0
    while i < len(jsons):
        file_name = f"{prefix}_{i}.csv"
        logger.info("Saving file %s in folder %s", file_name, output_path)

        data: List[Dict[str, Any]] = jsons[i]
        with open(output_path.joinpath(file_name), 'w') as csvfile:
            fieldnames = data[0].keys()
            writer: csv.DictWriter = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=delimiter)  # type: ignore
            writer.writeheader()
            for item in data:
                writer.writerow(item)

        i += 1
