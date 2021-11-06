"""Converts CSV file(s) to a JSON format"""
import json
from typing import Any, Dict, List

from file_converter.utils import process_input_path


def csv2json(
    input_path: str,
    output_path: str = ".",
    separator: str = ",",
    prefix: str = "",
) -> List[List[Dict[str, Any]]]:
    """Converts file(s) from CSV format to JSON
    The converted files will be saved with the same file name, with a possible
    prefix if desired.
    In case of a directory, all files must have the CSV extension and the same
    separator.

    Parameters
    ----------
    input_path
        A string with the path of the file or directory.
        Examples:
        - "./sample_file.csv"
        - "/home/username/csv_dir/"
        - "."

    output_path
        Output path to save the converted files

    separator
        Character used to separate the data in the CSV file. Possibilities are
        {",", ":", ";", "\t"}

    prefix
        String to prepend the converted files

    Returns
    -------
    A list of dictionaries. The list size is the same as the number of files to
    be converted.
    Moreover, new files are created in the desired directory.
    """

    file_names = process_input_path(input_path, "csv")

    json_lists = [
        _convert_file(file_name, separator=separator)
        for file_name in file_names
    ]

    for file_name, json_list in zip(file_names, json_lists):
        json_file_name = f"{output_path}/{prefix}{file_name.stem}.json"
        with open(json_file_name, "w", encoding="utf-8") as f:
            json.dump(json_list, f, indent=4)

    return json_lists


def _convert_file(
    file_name: str, separator: str = ","
) -> List[Dict[str, Any]]:
    """Converts file from CSV format to JSON"""

    def _process_line(line: str) -> Dict[str, Any]:
        line_values = line.strip().split(separator)
        d_json = {}
        for key, value in zip(keys, line_values):
            d_json[key] = _parse_value(value)

        return d_json

    with open(file_name, "r", encoding="utf-8") as f:
        header = next(f)
        keys = header.strip().split(separator)
        json_list = [_process_line(line) for line in f]

    return json_list


def _parse_value(value: str) -> Any:
    """Parse an incoming value into a number, string or None
    Here are the possibilities:
        - An empty string: set to None to be converted to a null later;
        - All digits: convert into an integer;
        - Digits and a decimal point: convert into a float;
        - Otherwise, return the original string.
    """
    if not value:
        return None

    if value.isdigit():
        return int(value)

    # Finally, we are left with a floating point or a regular string
    try:
        return float(value)
    except ValueError:
        return value
