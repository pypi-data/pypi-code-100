
from datetime import date, datetime, time
from pydantic import BaseModel

from .base import BaseDataStructure


"""
Contains data structure definitions for deflection beam data.

New data structures must be defined as a new class that derives from the
DeflectionBeamDataStructure class. These subclasses must be named with a random
8-digit hex (e.g. `uuid4().hex[:8]`) prepended with an underscore ("_").

The subclasses must define:
    1. data_structure class attribute (according to the "parse" package); and
    2. row_model class (Pydantic model) with field order that matches the table column
       order.

data_structure fields must match those in DeflectionBeamDataStructure.meta_model, which
can be updated with new fields provided it remains backward compatible.

row_model must be compatable with DeflectionBeamDataStructure.row_model, which is used
ensure consistency between all schema subclasses. Again
DeflectionBeamDataStructure.row_model can be updated with new fields provided it remains backward compatible.

"""


class DeflectionBeamDataStructure(BaseDataStructure):
    """
    Deflection beam data structure parent class.

    All deflection beam data structure classes must be derived from this parent class.
    data_structure and row_model should be redefined in the subclasses.

    """

    class meta_model(BaseModel):
        """
        Meta data Pydantic model.

        Must be backward compatable i.e. do not modify the data types and either make any
        new parameters optional or specify default values.

        """
        datetime: datetime
        station_no: int
        max_raw_deflection_mm: float

    class row_model(BaseModel):
        """
        Table row Pydantic model.

        Must be backward compatable i.e. do not modify the data types and either make any
        new parameters optional or specify default values.

        """
        distance_m: float
        raw_deflection_mm: float


class _cb379c14(DeflectionBeamDataStructure):

    data_structure = (
        "Date:\t{date:tg}\n"
        "Time:\t{time:tt}\n"
        "Location:\t{station_no:d}\n"
        "Operator:\t{}\n"
        "Latitude\t{}\n"
        "Longitude\t{}\n"
        "Max Deflection Measured\t{max_raw_deflection_mm:f}\n"
        "Max Deflection Corrected\t{}\n"
        "Bowl Corrected\t{}\n"
        "CF [Dpk-D200]\t{}\n"
        "Distance (m)\tDeflection  (mm)\n"
        "{}"
    )

    @staticmethod
    def meta_preprocessor(meta):
        """
        Meta data preprocessor.
        """
        meta["datetime"] = datetime.combine(meta["date"].date(), meta["time"])
        del(meta["date"], meta["time"])
        return meta

    class row_model(BaseModel):
        """
        Table row Pydantic model.
        """
        distance_m: float
        raw_deflection_mm: float
