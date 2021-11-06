"""A reader for the tables"""
import csv
from pathlib import Path
from typing import Dict, Set

from qiyas.construction.graph import UnitGraph

# =================================================================================================
def get_unit_types(unit_directory: Path) -> Set[str]:
    """Returns the unit types found in a directory"""

    unit_filenames = unit_directory.glob("*")
    unit_types = set([Path(filename).stem.split("_")[0] for filename in unit_filenames])
    return unit_types


# =================================================================================================
def read_unit_table(
    unit_type: str,
    unit_table_directory: Path,
    is_force_add: bool = False,
    is_construct: bool = True,
) -> UnitGraph:
    """Construct a unit graph from the csv file"""

    # Construct the file names
    unit_names_table_filename = unit_table_directory / (unit_type + "_names.csv")
    unit_converson_table_filename = unit_table_directory / (
        unit_type + "_conversions.csv"
    )

    # Read the conversion table
    unit_graph = UnitGraph(unit_type)

    # Create the nodes
    with open(unit_names_table_filename, mode="r", encoding="utf-8") as file:
        csv_file = csv.reader(file)
        next(csv_file)
        for line in csv_file:
            unit_graph.add_unit(line[0], line[1], line[2], line[3])

    # Create the nodes
    with open(unit_converson_table_filename, mode="r", encoding="utf-8") as file:
        csv_file = csv.reader(file)
        next(csv_file)
        for line in csv_file:
            unit_graph.add_conversion(line[0], line[1], float(line[2]), is_force_add)

    # Build full graph
    if is_construct:
        unit_graph.construct_full_graph()

    return unit_graph


# =================================================================================================
def read_unit_tables(
    unit_directory: Path, is_force_add: bool = False, is_construct: bool = False
) -> Dict[str, UnitGraph]:
    """Read the unit table in a dictionary"""

    unit_types = get_unit_types(unit_directory)

    unit_graphs = {}
    for unit_type in unit_types:
        unit_graphs[unit_type] = read_unit_table(
            unit_type, unit_directory, is_force_add, is_construct
        )

    return unit_graphs


# =================================================================================================
def generate_graphs(
    unit_tables_directory: Path,
    unit_graphs_directory: Path,
    is_force_add: bool = False,
    is_construct: bool = True,
):
    """Generates the graphs"""

    unit_types = get_unit_types(unit_tables_directory)
    for unit_type in unit_types:
        unit_graph = read_unit_table(
            unit_type, unit_tables_directory, is_force_add, is_construct
        )
        graph_filename = unit_graphs_directory / (unit_type + ".qs")
        unit_graph.save(graph_filename)


# =================================================================================================
