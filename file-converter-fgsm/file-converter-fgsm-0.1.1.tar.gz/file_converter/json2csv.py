"""Converts CSV file(s) to a JSON format"""
import json
from typing import Any, Dict, List


from file_converter.utils import process_input_path


def json2csv(
    input_path: str,
    output_path: str = ".",
    separator: str = ",",
    prefix: str = "",
) -> List[List[str]]:
    """Converts file(s) from CSV format to JSON
    In case of a directory, all files must have the CSV extension and the same
    separator.

    Parameters
    ----------
    input_path
        A string with the path of the file or directory.
        Examples:
        - "./sample_file.json"
        - "/home/username/json_dir/"
        - "."

    output_path
        Output path to save the converted files

    separator
        Character used to separate the data in the converted CSV file.
        Possibilities are {",", ":", ";", "\t"}

    prefix
        String to prepend the converted files

    Returns
    -------
    A list of lists, each one with the rows of the converted CSV file.
    Moreover, new files are created in the desired directory.
    """

    file_names = process_input_path(input_path, "json")
    csv_lists = [
        _convert_file(file_name, separator=separator)
        for file_name in file_names
    ]

    for file_name, csv_list in zip(file_names, csv_lists):
        csv_file_name = f"{output_path}/{prefix}{file_name.stem}.csv"
        with open(csv_file_name, "w", encoding="utf-8") as f:
            f.writelines(csv_list)

    return csv_lists


def _convert_file(file_name: str, separator: str = ",") -> List[str]:
    """Converts file from CSV format to JSON"""

    with open(file_name, "r", encoding="utf-8") as f:
        json_list = json.load(f)

    csv_list = []

    # Header
    # We assume all json elements have the same keys, so we can use any of them
    keys = list(json_list[0].keys())  # convert to list to ensure ordering
    header_line = separator.join(key for key in keys)
    header_line += "\n"
    csv_list.append(header_line)

    # Data lines
    def write_data_line(json_dict: Dict[str, Any]) -> str:
        # We explicitly use `json_dict[key]` instead of iterating in the values
        # to ensure the same order
        data_line = separator.join(
            _parse_value(json_dict[key]) for key in keys
        )
        data_line += "\n"
        return data_line

    data_lines = [write_data_line(json_dict) for json_dict in json_list]
    csv_list.extend(data_lines)

    return csv_list


def _parse_value(value: Any) -> str:
    """Parse a value to string
    Differently from the CSV -> JSON case, all we need here is to replace
    `None` with an empty string.
    """

    if value is None:
        return ""

    return str(value)
