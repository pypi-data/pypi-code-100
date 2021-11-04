
from datetime import date, time
from pydantic import BaseModel

from .base import BaseDataStructure


"""
Contains demo data structure definitions.

New data structures must be defined as a new class that derives from the
DemoDataStructure class. These subclasses must be named with a random
8-digit hex (e.g. `uuid4().hex[:8]`) prepended with an underscore ("_").

The subclasses must define:
    1. data_structure class attribute (according to the "parse" package); and
    2. row_model class (Pydantic model) with field order that matches the table column
       order.

data_structure fields must match those in DemoDataStructure.meta_model, which
can be updated with new fields provided it remains backward compatible.

row_model must be compatable with DemoDataStructure.row_model, which is used
ensure consistency between all schema subclasses. Again
DemoDataStructure.row_model can be updated with new fields provided it remains backward compatible.

"""


class DemoDataStructure(BaseDataStructure):
    """
    Demo data structure parent class.

    All demo data structure classes must be derived from this parent class.
    data_structure and row_model should be redefined in the subclasses.

    """

    class meta_model(BaseModel):
        """
        Meta data Pydantic model.

        Must be backward compatable i.e. do not modify the data types and either make any
        new parameters optional or specify default values.

        """
        param_1: str
        param_2: float

    class row_model(BaseModel):
        """
        Table row Pydantic model.

        Must be backward compatable i.e. do not modify the data types and either make any
        new parameters optional or specify default values.

        """
        column_1: str
        column_2: int


class _abcd1234(DemoDataStructure):

    data_structure = (
        "param1\t{param_1}\n"
        "param2\t{param_2:f}\n"
        "param3\t{}\n"
        "\n"
        "column B\tcolumn A\n"
        "{}"
    )

    class row_model(BaseModel):
        """
        Table row Pydantic model.
        """
        column_1: str
        column_2: int

    @staticmethod
    def meta_preprocessor(meta: dict):
        """
        Meta data preprocessor.
        """
        meta["param_2"] += 10
        return meta

    @staticmethod
    def row_preprocessor(row: dict):
        """
        Table row preprocessor.
        """
        row["column_1"] = row["column_1"] + "_"
        row["column_2"] = row["column_2"] - 1
        return row
