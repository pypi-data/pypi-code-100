"""A unit convertor"""
import sys
from typing import Any, Dict, List
from networkx.algorithms.shortest_paths.generic import shortest_path
from varname import argname
from qiyas.construction.graph import UnitGraph

# =================================================================================================
class MinimumPythonVersionNotMet(Exception):
    """Exception for when Python version is not compatible with the function"""

    def __init__(self, min_minor_version_required=8) -> None:
        self.message = (
            f"Minimum Python minor version {min_minor_version_required} "
            + "is required for this function"
        )
        super().__init__(self.message)


# =================================================================================================
class UnitsTypeMismatch(Exception):
    """Exception for when units are not found in the type defined"""

    def __init__(self, units: List[str], unit_type: str):
        """Initializes the exception"""
        self.message = f"Some or all of units {units} not found in type {unit_type}"
        super().__init__(self.message)


# =================================================================================================
class TypeNotFound(Exception):
    """Exception for when type is not found"""

    def __init__(self, unit_type: str):
        """Initializes the exception"""
        super().__init__()
        self.message = f"Type {unit_type} is not defined."


# =================================================================================================
class TypeDetectionNotPossible(Exception):
    """An exception to raise when multiple possible types are found"""

    def __init__(self, units: List[str], possible_types: List[str] = None):
        """Initializes the exception"""
        super().__init__()
        if possible_types is not None:
            self.message = (
                f"Multiple types {possible_types} for input units {units}. "
                + "Please define the type_name explictly."
            )
        else:
            self.message = f"No type detected for input for input units {units}."


# =================================================================================================
class UnitConvertor:
    """A unit convertor object"""

    def __init__(self, convertor_dictionary: Dict[str, UnitGraph]):
        """Initializes teh unit convertor"""
        self.convertor_dictionary = convertor_dictionary
        if sys.version_info.minor >= 8:
            self.is_quick_convert_possible: bool = False

    # ===========================================
    def get_unit_types(self):
        """Returns all the type names"""
        return list(self.convertor_dictionary.keys())

    # ===========================================
    def get_possible_types(self, units: List[str]) -> List[str]:
        """Returns the possible types"""
        possible_types: List[str] = []
        for unit_type in self.convertor_dictionary:
            current_unit_graph = self.convertor_dictionary[unit_type]
            is_node = [x in current_unit_graph for x in units]
            if all(is_node):
                possible_types.append(unit_type)

        return possible_types

    # ===========================================
    def validate_possible_type(
        self, units: List[str], possible_types: List[str]
    ) -> str:
        """Validates the possible type and returns the one type if available"""
        if len(possible_types) == 0:
            raise TypeDetectionNotPossible(units, None)
        elif len(possible_types) == 1:
            unit_type = possible_types[0]
        else:
            raise TypeDetectionNotPossible(units, possible_types)
        return unit_type

    # ===========================================
    def validate_units(self, units: List[str], unit_type: str) -> None:
        """Validates the units based a given unit type"""
        unit_graph = self.convertor_dictionary[unit_type]
        is_valid_unit_type = all([x in unit_graph for x in units])
        if not is_valid_unit_type:
            raise UnitsTypeMismatch(units, unit_type)

    # ===========================================
    def get_multiplier(self, unit1: str, unit2: str, unit_type: str = None):
        """retrieves the multiplier to convert unit1 to unit2"""

        # Get used type name
        used_unit_type: str
        if unit_type is not None:
            if unit_type in self.convertor_dictionary:
                used_unit_type = unit_type
                self.validate_units([unit1, unit2], unit_type)
            else:
                raise TypeNotFound(unit_type)
        else:
            units = [unit1, unit2]
            possible_types = self.get_possible_types(units)
            used_unit_type = self.validate_possible_type(units, possible_types)

        # Get the unit graph
        unit_graph = self.convertor_dictionary[used_unit_type]

        # If it is fully constructed, it is a simple lookup
        if unit_graph.is_constructed:
            multiplier = unit_graph[unit1][unit2]["weight"]
            return ((unit1, unit2), used_unit_type, multiplier)

        # If it is not fully constructed, we calculate it manually
        path: List[str] = shortest_path(unit_graph, unit1, unit2, weight="weight")
        multiplier = 1
        for i in range(len(path) - 1):
            multiplier = multiplier * unit_graph[path[i]][path[i + 1]]["weight"]
            return ((unit1, unit2), used_unit_type, multiplier)

    # ===========================================
    def convert(self, value: Any, unit1: str, unit2: str, unit_type: str = None) -> Any:
        """Converts a value to a new unit"""
        multiplier_info = self.get_multiplier(unit1, unit2, unit_type)
        multiplier = multiplier_info[2]
        converted_value = value * multiplier
        return converted_value

    # ===========================================
    def to(self, value, unit2: str, unit_type: str = None):
        """Quickly convert based on variable name"""

        # Stopping condition
        if not self.is_quick_convert_possible:
            raise MinimumPythonVersionNotMet(8)

        unit1 = argname("value").split("_")[-1]
        converted_value = self.convert(value, unit1, unit2, unit_type)
        return converted_value


# =================================================================================================
