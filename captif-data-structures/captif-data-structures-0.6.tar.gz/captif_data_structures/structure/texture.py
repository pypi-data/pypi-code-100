
from datetime import date, datetime, time
from typing import Any, List, Optional
from pydantic import BaseModel, validator

from .base import BaseDataStructure
from ..helpers import combine_date_time_fields


"""
Contains data structure definitions for CAPTIF texture data.

New data structures must be defined as a new class that derives from the
TextureDataStructure class. These subclasses must be named with a random
8-digit hex (e.g. `uuid4().hex[:8]`) prepended with an underscore ("_").

The subclasses must define:
    1. data_structure class attribute (according to the "parse" package); and
    2. row_model class (Pydantic model) with field order that matches the table column
       order.

data_structure fields must match those in TextureDataStructure.meta_model, which
can be updated with new fields provided it remains backward compatible.

row_model must be compatable with TextureDataStructure.row_model, which is used to
ensure consistency between all schema subclasses. Again TextureDataStructure.row_model
can be updated with new fields provided it remains backward compatible.

"""


class TextureDataStructure(BaseDataStructure):
    """
    CAPTIF texture data structure parent class.

    All texture data structure classes must be derived from this parent class.
    data_structure and row_model should be redefined in the subclasses.

    """

    class meta_model(BaseModel):
        """
        Meta data Pydantic model.

        Must be backward compatable i.e. do not modify the data types and either make any
        new parameters optional or specify default values.

        """
        date: Optional[date]
        file_number: Optional[int]
        sample_spacing_mm: Optional[float]

        @validator("date", pre=True)
        def parse_date(cls, value):
            return datetime.strptime(
                value,
                "%d/%m/%Y"
            ).date()

    class row_model(BaseModel):
        """
        Table row Pydantic model.

        Must be backward compatable i.e. do not modify the data types and either make any
        new parameters optional or specify default values.

        """
        distance_mm: float
        relative_height_mm: Optional[float]


class _4102a5dd(TextureDataStructure):

    data_structure = (
        "Road Name\tCAPTIF\n"
        "Ref Station\t{}\n"
        "Start Pos (m)\t{}\n"
        "End Pos (m)\t{}\n"
        "Direction\t{}\n"
        "Wheel Path\tLeft\n"
        "Date\t{date}\n"
        "File No.\t{file_number}\n"
        "Current Pos\t{}\n"
        "*****DATA*****\t\n"
        "{}"
        "\n"
    )

    class row_model(BaseModel):
        """
        Table row Pydantic model.
        """
        point_no: Any
        distance_mm: float
        relative_height_mm: Optional[float]

        @validator("relative_height_mm", pre=True)
        def parse_relative_height_mm(cls, value):
            return None if value == "NaN" else value

    @staticmethod
    def row_preprocessor(row: dict) -> dict:
        del(row["point_no"])
        return row


class _245ff223(TextureDataStructure):

    data_structure = (
        "Road Name\tCAPTIF\t\n"
        "Ref Station\t{}\t\n"
        "Start Pos (m)\t{}\t\n"
        "End Pos (m)\t{}\t\n"
        "Direction\t{}\t\n"
        "Wheel Path\tLeft\t\n"
        "Date\t{date}\t\n"
        "File No.\t{file_number}\t\n"
        "Current Pos\t{}\t\n"
        "*****DATA*****\t\t\n"
        "Data Point No:\tDistance (mm)\tDepth (mm)\n"
        "{}"
        "\n"
    )

    class row_model(BaseModel):
        """
        Table row Pydantic model.
        """
        point_no: Any
        distance_mm: float
        relative_height_mm: Optional[float]

        @validator("relative_height_mm", pre=True)
        def parse_relative_height_mm(cls, value):
            return None if value == "NaN" else value


class _7cd12dee(TextureDataStructure):
    data_structure = (
        "profile_name: {}\n"
        "sample_spacing_mm: {sample_spacing_mm}\n"
        "{}"
        "\n"
    )

    class row_model(BaseModel):
        """
        Table row Pydantic model.
        """
        relative_height_mm: Optional[float]

        @validator("relative_height_mm", pre=True)
        def parse_relative_height_mm(cls, value):
            return None if value == "NaN" else value

    @staticmethod
    def table_preprocessor(table_rows: List[dict], meta: dict = {}) -> List[dict]:
        for ii, _ in enumerate(table_rows):
            table_rows[ii]["distance_mm"] = ii * meta.get("sample_spacing_mm")
        return table_rows
