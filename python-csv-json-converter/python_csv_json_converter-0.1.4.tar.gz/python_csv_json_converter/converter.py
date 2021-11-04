import logging

from pathlib import Path

import click

logging.basicConfig(
  level="DEBUG", format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
)

logger = logging.getLogger(__name__)


@click.command()
@click.option(
  "--input", 
  "-i", 
  default="./", 
  help="Path where to find the CSV files to be converter to JSON.", 
  type=str
)
@click.option(
  "--output", 
  "-o", 
  default="./", 
  help="Path where the converted files will be saved.", 
  type=str
)
@click.option(
  "--prefix", 
  "-p",
  prompt=True,
  prompt_required=False,
  default="file", 
  help=(
    "Prefix used to prepend to the name of the converted file saved on disk. " 
    "The suffix will be a number starting from 0. ge: file_0.json"
  )
)
def converter(input: str = "./", output: str = "./", delimiter: str = ",", prefix: str = None):
    input_path = Path(input)
    output_path = Path(output)
    logger.info("input Path %s", input_path)
    logger.info("output Path %s", output_path)
    for p in [input_path, output_path]:
      if not (p.is_file() or p.is_dir()):
        raise TypeError("Not a valid path of file name.")
    data = read_csv_file(source=input_path, delimiter=delimiter)
    save_to_json_file(csvs=data, output_path=output_path, prefix=prefix)

def read_csv_file(source: Path, delimiter: str = ",") -> tuple:
    """Load a single csv file or all files withing a directory.

    Args:
        source (Path): Path for a single file or directory .
        delimiter (str, optional): Separator for collumns int the csv's. Defaults to ",".
    
    Returns:
        tuple: All dataframes loaded from the given source path.
    """
    if source.is_file():
        logger.info("Reading csv file %s",source)

def save_to_json_file(csvs: list, output_path: Path, prefix: str = None):
    """Save dataframes to Disk.

    Args:
        csvs (tuple): Tuple with dataframes that will be converted.
        output_path (Path): Path where to save the json files.
        prefix (str, optional): Name of files. If nothing is given it will have a number starting from 0. eg: file_0.json.
    """
    for key, content in enumerate(csvs):
        file_name = output_path.joinpath(f"{prefix}_{key}.json")
        logger.info("Saving file %s in folder %s", file_name, output_path)
        with open(file_name, "w") as file:
            file.write("[\n")
            for rows in content:
                tab = "".ljust(4, " ")

                begin_of_json = "{\n"
                file.write(f"{tab}{begin_of_json}")
                for row in rows:
                    file.write(format_json_row(row, (row != rows[-1])))

                # Is the last row?
                if rows != content[-1]:
                    end_of_json = "},\n"
                else:
                    end_of_json = "}\n"

                file.write(f"{tab}{end_of_json}")

            file.write("]")

def read_csv_file(source: Path, delimiter: str) -> list:
    """Load csv files from disk.

    Args:
        source (Path): Path of a single csv file or directory containing csvs to be parsed.
        delimiter (str): Separator for columns in csv.

    Returns:
        List: List of Lists.
    """

    if source.is_file():
        logger.info("Reading Single File %s", source)
        return [read_csv(source=source, delimiter=delimiter)]

    logger.info("Reading all files for given path %s", source)
    data = list()
    for name in source.iterdir():
        data.append(read_csv(source=name, delimiter=delimiter))

    return data


def read_csv(source: Path, delimiter: str) -> list:
    """Load a file from disk.

    Args:
        source (Path): Path of a single csv file to be parsed.
        delimiter (str): Separator for columns in csv.

    Returns:
        list: List of Tuples.
    """
    return_list = list()

    with open(source, "r") as file:
        rows = [row.split(delimiter) for row in file]
        first_line, content = rows[0], rows[1:]

        for key, row in enumerate(content):
            if len(row) == len(first_line):
                """Checks if all lines have values.
                Some files have special character in last lines."""

                aux_list = list()
                for index, column in enumerate(first_line):
                    aux_list.append((column.strip(), row[index].strip()))
                return_list.append(aux_list)

    return return_list


def isfloat(value: str) -> bool:
    """Checks if a value is floating.

    Args:
        value (str): A word.

    Returns:
        bool: A boolean value to show if the value is floating.
    """
    try:
        a = float(value)
    except (TypeError, ValueError):
        return False
    else:
        return True


def isint(value: str) -> bool:
    """Checks if a value is integer.

    Args:
        value (str): A word.

    Returns:
        bool: A boolean value to show if the value is integer.
    """
    try:
        a = float(value)
        b = int(a)
    except (TypeError, ValueError):
        return False
    else:
        return a == b


def format_json_row(row: tuple, has_comma: bool) -> str:
    """Transform a tuple in a formatted string.

    Args:
        row (tuple): A tuple containing the json name and value.
        has_comma (bool): A boolean that indicates the use of a comma.
    Returns:
        bool: A formatted string.
    """
    name, value = row

    tab = "".ljust(8, " ")
    end_line = "," if has_comma else ""

    if not value:
        return f'{tab}"{name}": null{end_line}\n'
    elif isint(value):
        return f'{tab}"{name}": {int(value)}{end_line}\n'
    elif isfloat(value):
        return f'{tab}"{name}": {float(value)}{end_line}\n'

    return f'{tab}"{name}": "{value}"{end_line}\n'


