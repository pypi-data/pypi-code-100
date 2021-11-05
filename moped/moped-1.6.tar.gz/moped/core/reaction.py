"""The main reaction file."""
from __future__ import annotations

import reprlib
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict, List, Set, Tuple


@dataclass
class Reaction:
    id: str
    compartment: str | Tuple[str, ...] | None = None
    stoichiometries: Dict[str, float] = field(default_factory=dict)
    bounds: Tuple[float, float] | None = None
    reversible: bool | None = None
    gibbs0: float | None = None
    ec: str | None = None
    types: List[str] = field(default_factory=list)
    pathways: Set[str] = field(default_factory=set)
    sequences: Dict[str, str] = field(default_factory=dict)
    monomers: Dict[str, Set[str]] = field(default_factory=dict)
    enzrxns: Dict[str, Dict[str, Dict[str, float]]] = field(default_factory=dict)
    database_links: Dict[str, Set[str]] = field(default_factory=dict)
    transmembrane: bool | None = None
    name: str | None = None
    base_id: str | None = None
    _var: int | None = None

    def __post_init__(self) -> None:
        if self.base_id is None:
            self.base_id = self.id

        if self.reversible is None:
            bounds = self.bounds
            if bounds is not None:
                if bounds[0] < 0 and bounds[1] > 0:
                    self.reversible = True
                else:
                    self.reversible = False
            else:
                self.reversible = False

        if self.transmembrane is None:
            compound_compartments = set()
            for i in self.stoichiometries:
                try:
                    compartment = i.rsplit("_", maxsplit=1)[1]
                except IndexError:
                    pass
                else:
                    compound_compartments.add(compartment)
            if len(compound_compartments) > 1:
                self.transmembrane = True
            else:
                self.transmembrane = False

    def __hash__(self) -> int:
        """Hash the compound id."""
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        """Compare compound id with another compound id."""
        if not isinstance(other, Reaction):
            return False
        if self.id is None or other.id is None:
            return False
        return self.id == other.id

    def __lt__(self, other: "Reaction") -> bool:
        """Compare compound id with another compound id."""
        if self.id is None or other.id is None:
            return False
        return self.id < other.id

    def __le__(self, other: "Reaction") -> bool:
        """Compare compound id with another compound id."""
        if self.id is None or other.id is None:
            return False
        return self.id <= other.id

    def __gt__(self, other: "Reaction") -> bool:
        """Compare compound id with another compound id."""
        if self.id is None or other.id is None:
            return False
        return self.id > other.id

    def __ge__(self, other: "Reaction") -> bool:
        """Compare compound id with another compound id."""
        if self.id is None or other.id is None:
            return False
        return self.id >= other.id

    def __iter__(self) -> Any:
        """Iterate over select attributes."""
        return (
            (i, getattr(self, i))
            for i in (
                "id",
                "base_id",
                "name",
                "stoichiometries",
                "transmembrane",
                "compartment",
                "bounds",
                "reversible",
                "gibbs0",
                "ec",
                "types",
                "pathways",
                "sequences",
                "monomers",
                "enzrxns",
                "database_links",
            )
            if bool(getattr(self, i))
        )

    def __str__(self) -> str:
        """Create a string representation of the reaction attributes."""
        s = f"Reaction <{self.id}>"
        for k, v in dict(self).items():
            s += f"\n    {k}: {v}"
        return s

    def __repr__(self) -> str:
        """Create a string representation of the reaction."""
        args = ", ".join(f"{k}={reprlib.repr(v)}" for k, v in dict(self).items())
        return f"Reaction({args})"

    def copy(self) -> "Reaction":
        """Create a deepcopy of the reaction.

        While this is more costly than shallow copies, it takes away
        the hassle of always keeping track if a shallow copy is what
        you want at the moment. So it's mostly for me not getting
        confused ;)

        Returns
        -------
        rxn: Reaction
        """
        return deepcopy(self)

    def _split_stoichiometries(self) -> Tuple[Dict[str, float], Dict[str, float]]:
        """Split the reaction stoichiometries into substrates and products.

        This is mostly used in structural analyses, such as the scope algorithm.

        Returns
        -------
        substrates: dict(str: float)
        products: dict(str: float)
        """
        substrates, products = {}, {}
        for k, v in self.stoichiometries.items():
            if v < 0:
                substrates[k] = v
            else:
                products[k] = v
        return substrates, products

    def replace_compound(self, old_compound: str, new_compound: str) -> None:
        """Replace a compound with another, keeping the stoichiometries.

        Parameters
        ----------
        old_compound : str
            Id of the compound to be replaced
        new_compound : str
            Id of the replacing compound
        """
        stoich = self.stoichiometries.pop(old_compound)
        self.stoichiometries[new_compound] = stoich

    def reverse_stoichiometry(self) -> None:
        """Reverses the stoichiometry of the reaction.

        This also reverses the bounds and gibbs0
        """
        self.stoichiometries = {k: -v for k, v in self.stoichiometries.items()}
        if self.gibbs0 is not None:
            self.gibbs0 = -self.gibbs0
        if self.bounds is not None:
            self.bounds = (-self.bounds[1], -self.bounds[0])

    def make_reversible(self) -> None:
        """Make the reaction reversible."""
        if self.bounds is None:
            raise ValueError("Reaction doesn't have bounds set")
        lb, ub = self.bounds
        # Check if it is not really irreversible in the first place
        if lb < 0 and ub > 0:
            pass
        elif lb < 0:
            self.bounds = (lb, -lb)
        else:
            self.bounds = (-ub, ub)
        self.reversible = True

    def make_irreversible(self) -> None:
        """Make the reaction irreversible."""
        if self.bounds is None:
            raise ValueError("Reaction doesn't have bounds set")
        lb, ub = self.bounds
        if lb < 0 and ub > 0:
            self.bounds = (0, ub)
        # Maybe it was annotated wrong
        elif ub > 0:
            self.bounds = (0, ub)
        else:
            self.bounds = (lb, 0)
        self.reversible = False
