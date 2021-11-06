"""Read for the convertor"""
from pathlib import Path
from qiyas.construction.graph import load_unit_graph
from qiyas.construction.reader import get_unit_types, read_unit_table
from qiyas.conversion.convertor import UnitConvertor

# =================================================================================================
def load_from_tables(
    unit_tables_directory: Path, is_force_add: bool = False, is_construct: bool = False
) -> UnitConvertor:
    """Read the unit table in a dictionary"""

    type_names = get_unit_types(unit_tables_directory)

    unit_graphs = {}
    for type_name in type_names:
        unit_graphs[type_name] = read_unit_table(
            type_name, unit_tables_directory, is_force_add, is_construct
        )

    unit_convertor = UnitConvertor(unit_graphs)

    return unit_convertor


# =================================================================================================
def load_from_qs_files(unit_graphs_directory: Path):
    """Loads a convertor from qs files"""
    type_names = get_unit_types(unit_graphs_directory)
    unit_graphs = {}
    for type_name in type_names:
        qs_filename = unit_graphs_directory / (type_name + ".qs")
        unit_graphs[type_name] = load_unit_graph(qs_filename)

    unit_convertor = UnitConvertor(unit_graphs)

    return unit_convertor


# =================================================================================================
