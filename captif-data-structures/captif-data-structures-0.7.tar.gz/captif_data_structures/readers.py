
from parse import parse
from pathlib import Path
from pydantic import ValidationError
from typing import Union

from . import structure


class DataStructureError(Exception):
    pass


class BaseReader:
    parent_structure = structure.BaseDataStructure

    @staticmethod
    def _read_data_from_file(path: Union[str, Path]):
        with open(path, "r") as f:
            data = f.read()
        return data

    @classmethod
    def load(cls, path: Union[str, Path], parallel: bool = True):
        data = cls._read_data_from_file(path)

        # Loop over all data structure subclasses and attempt to parse data:
        for structure in cls.parent_structure.children:
            meta = structure.extract_meta(data)
            if meta is None:
                continue
            meta = cls.parent_structure.validate_meta(meta)
            table_rows = structure.extract_table(data, meta, parallel)
            if table_rows is not None:
                table_rows = cls.parent_structure.validate_table(table_rows, parallel)
                break

        # Raise DataStructureError if unable to parse:
        if (meta is None) or (table_rows is None):
            raise DataStructureError(
                f"Unable to parse data using an existing data structure definition. You "
                f"may need to add a new data structure definition if one does not exist "
                f"(see 'captif_data_structure.structure')"
            )

        return (meta, table_rows, structure.id)


class DemoReader(BaseReader):
    parent_structure = structure.DemoDataStructure


class DeflectionBeamReader(BaseReader):
    parent_structure = structure.DeflectionBeamDataStructure


class LapCountReader(BaseReader):
    parent_structure = structure.LapCountDataStructure


class TextureReader(BaseReader):
    parent_structure = structure.TextureDataStructure
