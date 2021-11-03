
from datetime import date, datetime, time
from typing import Optional
from pydantic import BaseModel, validator

from .base import BaseDataStructure
from ..helpers import combine_date_time_fields


"""
Contains data structure definitions for CAPTIF lap count data.

New data structures must be defined as a new class that derives from the
LapCountDataStructure class. These subclasses must be named with a random
8-digit hex (e.g. `uuid4().hex[:8]`) prepended with an underscore ("_").

The subclasses must define:
    1. data_structure class attribute (according to the "parse" package); and
    2. row_model class (Pydantic model) with field order that matches the table column
       order.

data_structure fields must match those in LapCountDataStructure.meta_model, which
can be updated with new fields provided it remains backward compatible.

row_model must be compatable with LapCountDataStructure.row_model, which is used
ensure consistency between all schema subclasses. Again
LapCountDataStructure.row_model can be updated with new fields provided it remains backward compatible.

"""


class LapCountDataStructure(BaseDataStructure):
    """
    CAPTIF lap count data structure parent class.

    All lap count data structure classes must be derived from this parent class.
    data_structure and row_model should be redefined in the subclasses.

    """

    class meta_model(BaseModel):
        """
        Meta data Pydantic model.

        Must be backward compatable i.e. do not modify the data types and either make any
        new parameters optional or specify default values.

        """
        pass

    class row_model(BaseModel):
        """
        Table row Pydantic model.

        Must be backward compatable i.e. do not modify the data types and either make any
        new parameters optional or specify default values.

        """
        lap_count: int
        datetime: datetime
        position_cm: Optional[int]
        speed_kph: Optional[int]


class _d26612dd(LapCountDataStructure):

    data_structure = (
        "lap_count\tdate\ttime\n"
        "{}"
        "\n"
    )

    class row_model(BaseModel):
        """
        Table row Pydantic model.
        """
        lap_count: int
        date: date
        time: time

        @validator("date", pre=True)
        def parse_date(cls, value):
            return datetime.strptime(
                value,
                "%d/%m/%Y"
            ).date()

        @validator("time", pre=True)
        def parse_time(cls, value):
            return datetime.strptime(
                value,
                "%I:%M %p"
            ).time()

    @staticmethod
    def row_preprocessor(row: dict):
        """
        Table row preprocessor.
        """
        return combine_date_time_fields(row, delete=True)


class _e7b769c1(LapCountDataStructure):

    data_structure = (
        "lap_count\tdate\ttime\tposition_cm\tspeed_kph\n"
        "{}"
        "\n"
    )

    class row_model(BaseModel):
        """
        Table row Pydantic model.
        """
        lap_count: int
        date: date
        time: time
        position_cm: int
        speed_kph: int

        @validator("date", pre=True)
        def parse_date(cls, value):
            return datetime.strptime(
                value,
                "%d/%m/%Y"
            ).date()

        @validator("time", pre=True)
        def parse_time(cls, value):
            return datetime.strptime(
                value,
                "%I:%M:%S %p"
            ).time()

    @staticmethod
    def row_preprocessor(row: dict):
        """
        Table row preprocessor.
        """
        return combine_date_time_fields(row, delete=True)