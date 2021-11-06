"""A Unit graph object"""
import importlib
from itertools import combinations
from pathlib import Path
import pickle
from typing import List
import networkx as nx
from networkx.algorithms.shortest_paths.generic import shortest_path

# =================================================================================================
class UnitNotFound(Exception):
    """An exception to raise when the unit is not found"""

    def __init__(self, unit):
        """Initializes the exception"""
        super().__init__()
        self.message = f"Unit {unit} not found"


# =================================================================================================
class UnitGraph(nx.DiGraph):
    """A unit graph for holding the unit table information"""

    unit_type: str
    is_constructed: bool

    def __init__(self, unit_type: str):
        """Initializes the unit graph"""
        super().__init__()
        self.unit_type = unit_type
        self.is_constructed = False

    # ===========================================
    def add_unit(
        self,
        abbreviation: str,
        name: str = None,
        latex: str = None,
        comment: str = None,
    ):
        """Adds a unit to the graph"""
        self.add_node(abbreviation, name=name, latex=latex, comment=comment)

    # ===========================================
    def add_conversion(
        self,
        unit1: str,
        unit2: str,
        multiplier,
        is_force_add: bool = False,
        verbose: bool = False,
    ):
        """Adds a unit conversion"""

        if verbose is True:
            print(
                f"Adding conversion between {unit1} and {unit2} to type {self.unit_type}"
            )

        # Check units
        for unit in [unit1, unit2]:
            if not self.has_unit(unit):
                self.add_node(unit)
                if is_force_add:
                    self.add_node(unit)
                else:
                    raise UnitNotFound(unit)

        self.add_weighted_edges_from(
            [(unit1, unit2, multiplier), (unit2, unit1, 1 / multiplier)]
        )

    # ===========================================
    def has_unit(self, unit: str):
        """Check if the unit is added to the graph"""
        return self.has_node(unit)

    # ===========================================
    def get_units(self) -> List[str]:
        """returns the units in the graph"""
        return list(self.nodes)

    # ===========================================
    def construct_full_graph(self):
        """Constructs the full unit graph"""

        units = self.get_units()
        units_combination = combinations(units, 2)

        # Initialize the unit convertor used in calculation
        for unit_pair in units_combination:

            if self.has_edge(unit_pair[0], unit_pair[1]):
                continue
            path = shortest_path(self, unit_pair[0], unit_pair[1])
            multiplier = 1
            for i in range(len(path) - 1):
                multiplier = multiplier * self[path[i]][path[i + 1]]["weight"]
            self.add_conversion(unit_pair[0], unit_pair[1], multiplier)

        self.is_constructed = True

    # ===========================================
    def visualize(self):
        """Visualizes the unit graph"""
        matplotlib_specs = importlib.util.find_spec("matplotlib")
        if matplotlib_specs is None:
            print(
                "matplotlib is not installed. Please install this optional "
                + "package to visualize unit graphs"
            )
            return

    # ===========================================
    def save(self, filename: Path) -> None:
        """Saves the unit graph"""
        with open(filename, "wb") as file_handler:
            pickle.dump(self, file_handler)


# =================================================================================================
def load_unit_graph(filename: Path) -> UnitGraph:
    """Loads teh unit graph"""
    with open(filename, "rb") as file_handler:
        unit_graph = pickle.load(file_handler)
    return unit_graph


# =================================================================================================
