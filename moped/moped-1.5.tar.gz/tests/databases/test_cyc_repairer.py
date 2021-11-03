from __future__ import annotations

from typing import Dict, List

from moped.databases.cyc import ParseCompound, ParseReaction, Repairer

import pytest

COMPARTMENT_MAP = {
    "CYTOSOL": "CYTOSOL",
    "IN": "CYTOSOL",
    "UNKNOWN-SPACE": "CYTOSOL",
    "SIDE-1": "CYTOSOL",
    "SIDE-2": "PERIPLASM",
    "EXTRACELLULAR": "EXTRACELLULAR",
    "CHL-THY-MEM": "PERIPLASM",
    "CHLOR-STR": "PERIPLASM",
    "CHROM-STR": "PERIPLASM",
    "GOLGI-LUM": "CYTOSOL",
    "LYS-LUM": "CYTOSOL",
    "MIT-IM-SPC": "PERIPLASM",
    "MIT-IMEM": "PERIPLASM",
    "MIT-LUM": "CYTOSOL",
    "OUTER-MEM": "PERIPLASM",
    "PERI-BAC": "PERIPLASM",
    "PERI-BAC-GN": "PERIPLASM",
    "PERIPLASM": "PERIPLASM",
    "PEROX-LUM": "CYTOSOL",
    "PLASMA-MEM": "PERIPLASM",
    "PLAST-IMEM": "PERIPLASM",
    "PLASTID-STR": "PERIPLASM",
    "PM-ANIMAL": "PERIPLASM",
    "PM-BAC-ACT": "PERIPLASM",
    "PM-BAC-NEG": "PERIPLASM",
    "PM-BAC-POS": "PERIPLASM",
    "RGH-ER-LUM": "CYTOSOL",
    "RGH-ER-MEM": "PERIPLASM",
    "THY-LUM-CYA": "CYTOSOL",
    "VAC-LUM": "CYTOSOL",
    "VAC-MEM": "PERIPLASM",
    "VESICLE": "PERIPLASM",
    "OUT": "EXTRACELLULAR",
}


def test_reverse_stoichiometry() -> None:
    rxn = ParseReaction(
        id="RXN1",
        base_id="RXN1",
        substrates={"cpd1_c": -1},
        substrate_compartments={"cpd1_c": "CCO-IN"},
        products={"cpd2_c": 1},
        product_compartments={"cpd2_c": "CCO-IN"},
        gibbs0=-10,
    )
    Repairer.reverse_stoichiometry(rxn)
    assert rxn.substrates == {"cpd2_c": -1}
    assert rxn.substrate_compartments == {"cpd2_c": "CCO-IN"}
    assert rxn.products == {"cpd1_c": 1}
    assert rxn.product_compartments == {"cpd1_c": "CCO-IN"}
    assert rxn.gibbs0 == 10


def test_unify_direction_left_to_right() -> None:
    compounds: Dict[str, ParseCompound] = {}
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="LEFT-TO-RIGHT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.unify_reaction_direction(reactions["RXN1"])
    rxn = r.reactions["RXN1"]
    assert rxn.substrates == {"cpd1_c": -1}
    assert rxn.substrate_compartments == {"cpd1_c": "CCO-IN"}
    assert rxn.products == {"cpd2_c": 1}
    assert rxn.product_compartments == {"cpd2_c": "CCO-IN"}
    assert rxn.gibbs0 == -10
    assert rxn.reversible is False
    assert rxn.bounds == (0, 1000)


def test_unify_direction_physiol_left_to_right() -> None:
    compounds: Dict[str, ParseCompound] = {}
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="PHYSIOL-LEFT-TO-RIGHT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.unify_reaction_direction(reactions["RXN1"])
    rxn = r.reactions["RXN1"]
    assert rxn.substrates == {"cpd1_c": -1}
    assert rxn.substrate_compartments == {"cpd1_c": "CCO-IN"}
    assert rxn.products == {"cpd2_c": 1}
    assert rxn.product_compartments == {"cpd2_c": "CCO-IN"}
    assert rxn.gibbs0 == -10
    assert rxn.reversible is False
    assert rxn.bounds == (0, 1000)


def test_unify_direction_irrev_left_to_right() -> None:
    compounds: Dict[str, ParseCompound] = {}
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="IRREVERSIBLE-LEFT-TO-RIGHT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.unify_reaction_direction(reactions["RXN1"])
    rxn = r.reactions["RXN1"]
    assert rxn.substrates == {"cpd1_c": -1}
    assert rxn.substrate_compartments == {"cpd1_c": "CCO-IN"}
    assert rxn.products == {"cpd2_c": 1}
    assert rxn.product_compartments == {"cpd2_c": "CCO-IN"}
    assert rxn.gibbs0 == -10
    assert rxn.reversible is False
    assert rxn.bounds == (0, 1000)


def test_unify_direction_reversible() -> None:
    compounds: Dict[str, ParseCompound] = {}
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="REVERSIBLE",
            reversible=True,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.unify_reaction_direction(reactions["RXN1"])
    rxn = r.reactions["RXN1"]
    assert rxn.substrates == {"cpd1_c": -1}
    assert rxn.substrate_compartments == {"cpd1_c": "CCO-IN"}
    assert rxn.products == {"cpd2_c": 1}
    assert rxn.product_compartments == {"cpd2_c": "CCO-IN"}
    assert rxn.gibbs0 == -10
    assert rxn.reversible is True
    assert rxn.bounds == (-1000, 1000)


def test_unify_direction_right_to_left() -> None:
    compounds: Dict[str, ParseCompound] = {}
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="RIGHT-TO-LEFT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.unify_reaction_direction(reactions["RXN1"])
    rxn = r.reactions["RXN1"]
    assert rxn.substrates == {"cpd2_c": -1}
    assert rxn.substrate_compartments == {"cpd2_c": "CCO-IN"}
    assert rxn.products == {"cpd1_c": 1}
    assert rxn.product_compartments == {"cpd1_c": "CCO-IN"}
    assert rxn.gibbs0 == 10
    assert rxn.reversible is False
    assert rxn.bounds == (0, 1000)


def test_unify_direction_physiol_right_to_left() -> None:
    compounds: Dict[str, ParseCompound] = {}
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="PHYSIOL-RIGHT-TO-LEFT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.unify_reaction_direction(reactions["RXN1"])
    rxn = r.reactions["RXN1"]
    assert rxn.substrates == {"cpd2_c": -1}
    assert rxn.substrate_compartments == {"cpd2_c": "CCO-IN"}
    assert rxn.products == {"cpd1_c": 1}
    assert rxn.product_compartments == {"cpd1_c": "CCO-IN"}
    assert rxn.gibbs0 == 10
    assert rxn.reversible is False
    assert rxn.bounds == (0, 1000)


def test_unify_direction_irrev_right_to_left() -> None:
    compounds: Dict[str, ParseCompound] = {}
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="IRREVERSIBLE-RIGHT-TO-LEFT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.unify_reaction_direction(reactions["RXN1"])
    rxn = r.reactions["RXN1"]
    assert rxn.substrates == {"cpd2_c": -1}
    assert rxn.substrate_compartments == {"cpd2_c": "CCO-IN"}
    assert rxn.products == {"cpd1_c": 1}
    assert rxn.product_compartments == {"cpd1_c": "CCO-IN"}
    assert rxn.gibbs0 == 10
    assert rxn.reversible is False
    assert rxn.bounds == (0, 1000)


def test_unify_direction_garbage() -> None:
    compounds: Dict[str, ParseCompound] = {}
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="GARBAGE",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    with pytest.warns(UserWarning):
        r.unify_reaction_direction(reactions["RXN1"])
    rxn = r.reactions["RXN1"]
    assert rxn.substrates == {"cpd1_c": -1}
    assert rxn.substrate_compartments == {"cpd1_c": "CCO-IN"}
    assert rxn.products == {"cpd2_c": 1}
    assert rxn.product_compartments == {"cpd2_c": "CCO-IN"}
    assert rxn.gibbs0 == -10
    assert rxn.reversible is False
    assert rxn.bounds == (0, 1000)


def test_compound_existence() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(id="cpd2_c", base_id="cpd2", compartment="CYTOSOL"),
        "cpd2_c": ParseCompound(id="cpd2_c", base_id="cpd2", compartment="CYTOSOL"),
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="IRREVERSIBLE-RIGHT-TO-LEFT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    assert r.check_compound_existence(r.reactions["RXN1"])


def test_missing_substrate() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd2_c": ParseCompound(id="cpd2_c", base_id="cpd2", compartment="CYTOSOL")
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="IRREVERSIBLE-RIGHT-TO-LEFT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    assert not r.check_compound_existence(r.reactions["RXN1"])


def test_missing_product() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(id="cpd2_c", base_id="cpd2", compartment="CYTOSOL")
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="IRREVERSIBLE-RIGHT-TO-LEFT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    assert not r.check_compound_existence(r.reactions["RXN1"])


def test_charge_balance_both_zero() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(id="cpd1_c", base_id="cpd1", compartment="CYTOSOL"),
        "cpd2_c": ParseCompound(id="cpd2_c", base_id="cpd2", compartment="CYTOSOL"),
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="IRREVERSIBLE-RIGHT-TO-LEFT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    assert r.check_charge_balance(r.reactions["RXN1"])


def test_charge_balance_both_one() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(id="cpd1_c", base_id="cpd1", charge=1, compartment="CYTOSOL"),
        "cpd2_c": ParseCompound(id="cpd2_c", base_id="cpd2", charge=1, compartment="CYTOSOL"),
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="IRREVERSIBLE-RIGHT-TO-LEFT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    assert r.check_charge_balance(r.reactions["RXN1"])


def test_charge_balance_substrate_stoichiometry() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(id="cpd1_c", base_id="cpd1", charge=1, compartment="CYTOSOL"),
        "cpd2_c": ParseCompound(id="cpd2_c", base_id="cpd2", charge=2, compartment="CYTOSOL"),
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -2},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="IRREVERSIBLE-RIGHT-TO-LEFT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    assert r.check_charge_balance(r.reactions["RXN1"])


def test_charge_balance_product_stoichiometry() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(id="cpd1_c", base_id="cpd1", charge=2, compartment="CYTOSOL"),
        "cpd2_c": ParseCompound(id="cpd2_c", base_id="cpd2", charge=1, compartment="CYTOSOL"),
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 2},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="IRREVERSIBLE-RIGHT-TO-LEFT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    assert r.check_charge_balance(r.reactions["RXN1"])


def test_charge_balance_opposite_signs() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(id="cpd1_c", base_id="cpd1", charge=-1, compartment="CYTOSOL"),
        "cpd2_c": ParseCompound(id="cpd2_c", base_id="cpd2", charge=1, compartment="CYTOSOL"),
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="IRREVERSIBLE-RIGHT-TO-LEFT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    assert not r.check_charge_balance(r.reactions["RXN1"])


def test_mass_balance_single_atom() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(id="cpd1_c", base_id="cpd1", formula={"C": 1}),
        "cpd2_c": ParseCompound(id="cpd2_c", base_id="cpd2", formula={"C": 1}),
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="IRREVERSIBLE-RIGHT-TO-LEFT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    assert r.check_mass_balance(r.reactions["RXN1"])


def test_mass_balance_multiple_atoms() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(
            id="cpd1_c",
            base_id="cpd1",
            formula={"C": 6, "H": 12, "O": 6},
        ),
        "cpd2_c": ParseCompound(
            id="cpd2_c",
            base_id="cpd2",
            formula={"C": 6, "H": 12, "O": 6},
        ),
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="IRREVERSIBLE-RIGHT-TO-LEFT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    assert r.check_mass_balance(r.reactions["RXN1"])


def test_mass_balance_multiple_compounds() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(
            id="cpd1_c",
            base_id="cpd1",
            formula={"C": 6, "H": 12, "O": 6},
        ),
        "cpd2_c": ParseCompound(
            id="cpd2_c",
            base_id="cpd2",
            formula={"C": 6, "H": 12, "O": 6},
        ),
        "A_c": ParseCompound(
            id="A_c",
            base_id="A",
            formula={"C": 6},
        ),
        "B_c": ParseCompound(
            id="B_c",
            base_id="B",
            formula={"C": 6},
        ),
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1, "A_c": -2},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1, "B_c": 2},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="IRREVERSIBLE-RIGHT-TO-LEFT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    assert r.check_mass_balance(r.reactions["RXN1"])


def test_mass_balance_multiple_atoms_substrate_stoichiometry() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(
            id="cpd1_c",
            base_id="cpd1",
            formula={"C": 3, "H": 6, "O": 3},
        ),
        "cpd2_c": ParseCompound(
            id="cpd2_c",
            base_id="cpd2",
            formula={"C": 6, "H": 12, "O": 6},
        ),
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -2},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="IRREVERSIBLE-RIGHT-TO-LEFT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    assert r.check_mass_balance(r.reactions["RXN1"])


def test_mass_balance_multiple_atoms_product_stoichiometry() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(
            id="cpd1_c",
            base_id="cpd1",
            formula={"C": 6, "H": 12, "O": 6},
        ),
        "cpd2_c": ParseCompound(
            id="cpd2_c",
            base_id="cpd2",
            formula={"C": 3, "H": 6, "O": 3},
        ),
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 2},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="IRREVERSIBLE-RIGHT-TO-LEFT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    assert r.check_mass_balance(r.reactions["RXN1"])


def test_mass_balance_missing_substrate_formula() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(
            id="cpd1_c",
            base_id="cpd1",
            formula={},
        ),
        "cpd2_c": ParseCompound(
            id="cpd2_c",
            base_id="cpd2",
            formula={
                "C": 1,
            },
        ),
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="IRREVERSIBLE-RIGHT-TO-LEFT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    assert not r.check_mass_balance(r.reactions["RXN1"])


def test_mass_balance_missing_product_formula() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(
            id="cpd1_c",
            base_id="cpd1",
            formula={"C": 1},
        ),
        "cpd2_c": ParseCompound(
            id="cpd2_c",
            base_id="cpd2",
            formula={},
        ),
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="IRREVERSIBLE-RIGHT-TO-LEFT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    assert not r.check_mass_balance(r.reactions["RXN1"])


def test_mass_balance_missing_substrate_atom() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(
            id="cpd1_c",
            base_id="cpd1",
            formula={"C": 1},
        ),
        "cpd2_c": ParseCompound(
            id="cpd2_c",
            base_id="cpd2",
            formula={"C": 1, "H": 1},
        ),
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="IRREVERSIBLE-RIGHT-TO-LEFT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    assert not r.check_mass_balance(r.reactions["RXN1"])


def test_mass_balance_missing_product_atom() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(
            id="cpd1_c",
            base_id="cpd1",
            formula={"C": 1, "H": 1},
        ),
        "cpd2_c": ParseCompound(
            id="cpd2_c",
            base_id="cpd2",
            formula={"C": 1},
        ),
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            gibbs0=-10,
            direction="IRREVERSIBLE-RIGHT-TO-LEFT",
            reversible=False,
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    assert not r.check_mass_balance(r.reactions["RXN1"])


def test_variants_no_variants() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(
            id="cpd1_c",
            base_id="cpd1",
            charge=1,
            formula={"C": 1},
        ),
        "cpd2_c": ParseCompound(
            id="cpd2_c",
            base_id="cpd2",
            charge=1,
            formula={"C": 1},
        ),
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.create_reaction_variants("RXN1", r.reactions["RXN1"])
    rxn = r.reactions["RXN1"]
    assert rxn.id == "RXN1"
    assert rxn.substrates == {"cpd1_c": -1}
    assert rxn.substrate_compartments == {"cpd1_c": "CCO-IN"}
    assert rxn.products == {"cpd2_c": 1}
    assert rxn.product_compartments == {"cpd2_c": "CCO-IN"}


def test_variants_empty() -> None:
    compounds: Dict[str, ParseCompound] = {
        "A1": ParseCompound(id="A1_c", base_id="A1", formula={"C": 1}, charge=1),
        "A2": ParseCompound(id="A2_c", base_id="A2", formula={"C": 1}, charge=1),
        "B1": ParseCompound(id="B1_c", base_id="B1", formula={"C": 1}, charge=1),
        "B2": ParseCompound(id="B2_c", base_id="B2", formula={"C": 1}, charge=1),
    }
    compound_types: Dict[str, List[str]] = {"T1": [], "T2": []}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"T1": -1},
            substrate_compartments={"T1": "CCO-IN"},
            products={"T2": 1},
            product_compartments={"T2": "CCO-IN"},
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.create_reaction_variants("RXN1", r.reactions["RXN1"])
    assert r.reactions == {}


def test_variants_one_substrate() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(
            id="cpd1_c",
            base_id="cpd1",
            charge=1,
            formula={"C": 1},
        ),
        "cpd2_c": ParseCompound(
            id="cpd2_c",
            base_id="cpd2",
            charge=1,
            formula={"C": 1},
        ),
    }
    compound_types: Dict[str, List[str]] = {"T1": ["cpd1_c"]}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"T1": -1},
            substrate_compartments={"T1": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.create_reaction_variants("RXN1", r.reactions["RXN1"])
    rxn = r.reactions["RXN1__var__0"]

    assert rxn.id == "RXN1__var__0"
    assert rxn.substrates == {"cpd1_c": -1}
    assert rxn.substrate_compartments == {"cpd1_c": "CCO-IN"}
    assert rxn.products == {"cpd2_c": 1}
    assert rxn.product_compartments == {"cpd2_c": "CCO-IN"}


def test_variants_two_substrates() -> None:
    compounds: Dict[str, ParseCompound] = {
        "X1": ParseCompound(id="X1", base_id="X1_c", formula={"C": 1}, charge=1),
        "X2": ParseCompound(id="X2", base_id="X2_c", formula={"C": 1}, charge=1),
        "cpd2_c": ParseCompound(id="cpd2_c", base_id="cpd2", charge=1, formula={"C": 1}),
    }
    compound_types: Dict[str, List[str]] = {"T1": ["X1", "X2"]}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"T1": -1},
            substrate_compartments={"T1": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.create_reaction_variants("RXN1", r.reactions["RXN1"])
    rxn = r.reactions["RXN1__var__0"]
    assert rxn.id == "RXN1__var__0"
    assert rxn.substrates == {"X1": -1}
    assert rxn.substrate_compartments == {"X1": "CCO-IN"}
    assert rxn.products == {"cpd2_c": 1}
    assert rxn.product_compartments == {"cpd2_c": "CCO-IN"}

    rxn = r.reactions["RXN1__var__1"]
    assert rxn.id == "RXN1__var__1"
    assert rxn.substrates == {"X2": -1}
    assert rxn.substrate_compartments == {"X2": "CCO-IN"}
    assert rxn.products == {"cpd2_c": 1}
    assert rxn.product_compartments == {"cpd2_c": "CCO-IN"}


def test_variants_one_product() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(
            id="cpd1_c",
            base_id="cpd1",
            charge=1,
            formula={"C": 1},
        ),
        "cpd2_c": ParseCompound(
            id="cpd2_c",
            base_id="cpd2",
            charge=1,
            formula={"C": 1},
        ),
    }
    compound_types: Dict[str, List[str]] = {"T2": ["cpd2_c"]}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"T2": 1},
            product_compartments={"T2": "CCO-IN"},
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.create_reaction_variants("RXN1", r.reactions["RXN1"])
    rxn = r.reactions["RXN1__var__0"]
    assert rxn.id == "RXN1__var__0"
    assert rxn.substrates == {"cpd1_c": -1}
    assert rxn.substrate_compartments == {"cpd1_c": "CCO-IN"}
    assert rxn.products == {"cpd2_c": 1}
    assert rxn.product_compartments == {"cpd2_c": "CCO-IN"}


def test_variants_two_products() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(
            id="cpd1_c",
            base_id="cpd1",
            charge=1,
            formula={"C": 1},
        ),
        "Y1": ParseCompound(base_id="Y1", id="Y1_c", formula={"C": 1}, charge=1),
        "Y2": ParseCompound(base_id="Y2", id="Y2_c", formula={"C": 1}, charge=1),
    }
    compound_types: Dict[str, List[str]] = {"T2": ["Y1", "Y2"]}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"T2": 1},
            product_compartments={"T2": "CCO-IN"},
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.create_reaction_variants("RXN1", r.reactions["RXN1"])
    rxn = r.reactions["RXN1__var__0"]
    assert rxn.id == "RXN1__var__0"
    assert rxn.substrates == {"cpd1_c": -1}
    assert rxn.substrate_compartments == {"cpd1_c": "CCO-IN"}
    assert rxn.products == {"Y1": 1}
    assert rxn.product_compartments == {"Y1": "CCO-IN"}
    rxn = r.reactions["RXN1__var__1"]
    assert rxn.id == "RXN1__var__1"
    assert rxn.substrates == {"cpd1_c": -1}
    assert rxn.substrate_compartments == {"cpd1_c": "CCO-IN"}
    assert rxn.products == {"Y2": 1}
    assert rxn.product_compartments == {"Y2": "CCO-IN"}


def test_variants_one_substrate_one_product() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(id="cpd1_c", base_id="cpd1", charge=1, formula={"C": 1}),
        "cpd2_c": ParseCompound(id="cpd2_c", base_id="cpd2", charge=1, formula={"C": 1}),
    }
    compound_types: Dict[str, List[str]] = {"T1": ["cpd1_c"], "T2": ["cpd2_c"]}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"T1": -1},
            substrate_compartments={"T1": "CCO-IN"},
            products={"T2": 1},
            product_compartments={"T2": "CCO-IN"},
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.create_reaction_variants("RXN1", r.reactions["RXN1"])
    rxn = r.reactions["RXN1__var__0"]
    assert rxn.id == "RXN1__var__0"
    assert rxn.substrates == {"cpd1_c": -1}
    assert rxn.substrate_compartments == {"cpd1_c": "CCO-IN"}
    assert rxn.products == {"cpd2_c": 1}
    assert rxn.product_compartments == {"cpd2_c": "CCO-IN"}


def test_variants_two_substrates_two_products() -> None:
    compounds: Dict[str, ParseCompound] = {
        "X1": ParseCompound(base_id="X1", id="X1", formula={"C": 1}, charge=1),
        "X2": ParseCompound(base_id="X2", id="X2", formula={"C": 1}, charge=1),
        "Y1": ParseCompound(base_id="Y1", id="Y1", formula={"C": 1}, charge=1),
        "Y2": ParseCompound(base_id="Y2", id="Y2", formula={"C": 1}, charge=1),
    }
    compound_types: Dict[str, List[str]] = {"T1": ["X1", "X2"], "T2": ["Y1", "Y2"]}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"T1": -1},
            substrate_compartments={"T1": "CCO-IN"},
            products={"T2": 1},
            product_compartments={"T2": "CCO-IN"},
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.create_reaction_variants("RXN1", r.reactions["RXN1"])
    rxn = r.reactions["RXN1__var__0"]
    assert rxn.id == "RXN1__var__0"
    assert rxn.substrates == {"X1": -1}
    assert rxn.substrate_compartments == {"X1": "CCO-IN"}
    assert rxn.products == {"Y1": 1}
    assert rxn.product_compartments == {"Y1": "CCO-IN"}

    rxn = r.reactions["RXN1__var__1"]
    assert rxn.id == "RXN1__var__1"
    assert rxn.substrates == {"X1": -1}
    assert rxn.substrate_compartments == {"X1": "CCO-IN"}
    assert rxn.products == {"Y2": 1}
    assert rxn.product_compartments == {"Y2": "CCO-IN"}

    rxn = r.reactions["RXN1__var__2"]
    assert rxn.id == "RXN1__var__2"
    assert rxn.substrates == {"X2": -1}
    assert rxn.substrate_compartments == {"X2": "CCO-IN"}
    assert rxn.products == {"Y1": 1}
    assert rxn.product_compartments == {"Y1": "CCO-IN"}

    rxn = r.reactions["RXN1__var__3"]
    assert rxn.id == "RXN1__var__3"
    assert rxn.substrates == {"X2": -1}
    assert rxn.substrate_compartments == {"X2": "CCO-IN"}
    assert rxn.products == {"Y2": 1}
    assert rxn.product_compartments == {"Y2": "CCO-IN"}


def test_variants_two_substrates_two_products_one_normal() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(id="cpd1_c", base_id="cpd1", charge=1, formula={"C": 1}),
        "cpd2_c": ParseCompound(id="cpd2_c", base_id="cpd2", charge=1, formula={"C": 1}),
        "A1": ParseCompound(base_id="A1", id="A1", formula={"C": 1}, charge=1),
        "A2": ParseCompound(base_id="A2", id="A2", formula={"C": 1}, charge=1),
        "B1": ParseCompound(base_id="B1", id="B1", formula={"C": 1}, charge=1),
        "B2": ParseCompound(base_id="B2", id="B2", formula={"C": 1}, charge=1),
    }
    compound_types: Dict[str, List[str]] = {"T1": ["A1", "A2"], "T2": ["B1", "B2"]}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1, "T1": -1},
            substrate_compartments={"cpd1_c": "CCO-IN", "T1": "CCO-IN"},
            products={"cpd2_c": 1, "T2": 1},
            product_compartments={"cpd2_c": "CCO-IN", "T2": "CCO-IN"},
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.create_reaction_variants("RXN1", r.reactions["RXN1"])
    rxn = r.reactions["RXN1__var__0"]
    assert rxn.id == "RXN1__var__0"
    assert rxn.substrates == {"cpd1_c": -1, "A1": -1}
    assert rxn.substrate_compartments == {"cpd1_c": "CCO-IN", "A1": "CCO-IN"}
    assert rxn.products == {"cpd2_c": 1, "B1": 1}
    assert rxn.product_compartments == {"cpd2_c": "CCO-IN", "B1": "CCO-IN"}
    rxn = r.reactions["RXN1__var__1"]
    assert rxn.id == "RXN1__var__1"
    assert rxn.substrates == {"cpd1_c": -1, "A1": -1}
    assert rxn.substrate_compartments == {"cpd1_c": "CCO-IN", "A1": "CCO-IN"}
    assert rxn.products == {"cpd2_c": 1, "B2": 1}
    assert rxn.product_compartments == {"cpd2_c": "CCO-IN", "B2": "CCO-IN"}
    rxn = r.reactions["RXN1__var__2"]
    assert rxn.id == "RXN1__var__2"
    assert rxn.substrates == {"cpd1_c": -1, "A2": -1}
    assert rxn.substrate_compartments == {"cpd1_c": "CCO-IN", "A2": "CCO-IN"}
    assert rxn.products == {"cpd2_c": 1, "B1": 1}
    assert rxn.product_compartments == {"cpd2_c": "CCO-IN", "B1": "CCO-IN"}
    rxn = r.reactions["RXN1__var__3"]
    assert rxn.id == "RXN1__var__3"
    assert rxn.substrates == {"cpd1_c": -1, "A2": -1}
    assert rxn.substrate_compartments == {"cpd1_c": "CCO-IN", "A2": "CCO-IN"}
    assert rxn.products == {"cpd2_c": 1, "B2": 1}
    assert rxn.product_compartments == {"cpd2_c": "CCO-IN", "B2": "CCO-IN"}


def test_variants_charge_matching() -> None:
    compounds: Dict[str, ParseCompound] = {
        "A1": ParseCompound(base_id="A1", id="A1", formula={"C": 1}, charge=1),
        "A2": ParseCompound(base_id="A2", id="A2", formula={"C": 1}, charge=0),
        "B1": ParseCompound(base_id="B1", id="B1", formula={"C": 1}, charge=1),
        "B2": ParseCompound(base_id="B2", id="B2", formula={"C": 1}, charge=0),
    }
    compound_types: Dict[str, List[str]] = {"T1": ["A1", "A2"], "T2": ["B1", "B2"]}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"T1": -1},
            substrate_compartments={"T1": "CCO-IN"},
            products={"T2": 1},
            product_compartments={"T2": "CCO-IN"},
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.create_reaction_variants("RXN1", r.reactions["RXN1"])
    rxn = r.reactions["RXN1__var__0"]
    assert rxn.id == "RXN1__var__0"
    assert rxn.substrates == {"A1": -1}
    assert rxn.substrate_compartments == {"A1": "CCO-IN"}
    assert rxn.products == {"B1": 1}
    assert rxn.product_compartments == {"B1": "CCO-IN"}
    rxn = r.reactions["RXN1__var__1"]
    assert rxn.id == "RXN1__var__1"
    assert rxn.substrates == {"A2": -1}
    assert rxn.substrate_compartments == {"A2": "CCO-IN"}
    assert rxn.products == {"B2": 1}
    assert rxn.product_compartments == {"B2": "CCO-IN"}


def test_variants_formula_matching() -> None:
    compounds: Dict[str, ParseCompound] = {
        "A1": ParseCompound(base_id="A1", id="A1", formula={"C": 1, "H": 1}, charge=1),
        "A2": ParseCompound(base_id="A2", id="A2", formula={"C": 1}, charge=1),
        "B1": ParseCompound(base_id="B1", id="B1", formula={"C": 1, "H": 1}, charge=1),
        "B2": ParseCompound(base_id="B2", id="B2", formula={"C": 1}, charge=1),
    }
    compound_types: Dict[str, List[str]] = {"T1": ["A1", "A2"], "T2": ["B1", "B2"]}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"T1": -1},
            substrate_compartments={"T1": "CCO-IN"},
            products={"T2": 1},
            product_compartments={"T2": "CCO-IN"},
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.create_reaction_variants("RXN1", r.reactions["RXN1"])
    rxn = r.reactions["RXN1__var__0"]
    assert rxn.id == "RXN1__var__0"
    assert rxn.substrates == {"A1": -1}
    assert rxn.substrate_compartments == {"A1": "CCO-IN"}
    assert rxn.products == {"B1": 1}
    assert rxn.product_compartments == {"B1": "CCO-IN"}
    rxn = r.reactions["RXN1__var__1"]
    assert rxn.id == "RXN1__var__1"
    assert rxn.substrates == {"A2": -1}
    assert rxn.substrate_compartments == {"A2": "CCO-IN"}
    assert rxn.products == {"B2": 1}
    assert rxn.product_compartments == {"B2": "CCO-IN"}


def test_variants_missing_substrate() -> None:
    compounds: Dict[str, ParseCompound] = {
        "A1": ParseCompound(base_id="A1", id="A1", formula={"C": 1}, charge=1),
        "B1": ParseCompound(base_id="B1", id="B1", formula={"C": 1}, charge=1),
        "B2": ParseCompound(base_id="B2", id="B2", formula={"C": 1}, charge=1),
    }
    compound_types: Dict[str, List[str]] = {"T1": ["A1", "A2"], "T2": ["B1", "B2"]}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"T1": -1},
            substrate_compartments={"T1": "CCO-IN"},
            products={"T2": 1},
            product_compartments={"T2": "CCO-IN"},
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.create_reaction_variants("RXN1", r.reactions["RXN1"])
    rxn = r.reactions["RXN1__var__0"]
    assert rxn.id == "RXN1__var__0"
    assert rxn.substrates == {"A1": -1}
    assert rxn.substrate_compartments == {"A1": "CCO-IN"}
    assert rxn.products == {"B1": 1}
    assert rxn.product_compartments == {"B1": "CCO-IN"}
    rxn = r.reactions["RXN1__var__1"]
    assert rxn.id == "RXN1__var__1"
    assert rxn.substrates == {"A1": -1}
    assert rxn.substrate_compartments == {"A1": "CCO-IN"}
    assert rxn.products == {"B2": 1}
    assert rxn.product_compartments == {"B2": "CCO-IN"}


def test_variants_missing_product() -> None:
    compounds: Dict[str, ParseCompound] = {
        "A1": ParseCompound(base_id="A1", id="A1", formula={"C": 1}, charge=1),
        "A2": ParseCompound(base_id="B1", id="B1", formula={"C": 1}, charge=1),
        "B1": ParseCompound(base_id="B2", id="B2", formula={"C": 1}, charge=1),
    }
    compound_types: Dict[str, List[str]] = {"T1": ["A1", "A2"], "T2": ["B1", "B2"]}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"T1": -1},
            substrate_compartments={"T1": "CCO-IN"},
            products={"T2": 1},
            product_compartments={"T2": "CCO-IN"},
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.create_reaction_variants("RXN1", r.reactions["RXN1"])
    rxn = r.reactions["RXN1__var__0"]
    assert rxn.id == "RXN1__var__0"
    assert rxn.substrates == {"A1": -1}
    assert rxn.substrate_compartments == {"A1": "CCO-IN"}
    assert rxn.products == {"B1": 1}
    assert rxn.product_compartments == {"B1": "CCO-IN"}
    rxn = r.reactions["RXN1__var__1"]
    assert rxn.id == "RXN1__var__1"
    assert rxn.substrates == {"A2": -1}
    assert rxn.substrate_compartments == {"A2": "CCO-IN"}
    assert rxn.products == {"B1": 1}
    assert rxn.product_compartments == {"B1": "CCO-IN"}


def test_split_location_string() -> None:
    compounds: Dict[str, ParseCompound] = {}
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {}
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    assert r.split_location_string("CCO-CYTOSOL") == {"CCO-OUT": "CYTOSOL", "CCO-IN": "CYTOSOL"}
    assert r.split_location_string("CCO-EXTRACELLULAR") == {
        "CCO-OUT": "EXTRACELLULAR",
        "CCO-IN": "CYTOSOL",
    }
    assert r.split_location_string("CCO-EXTRACELLULAR-CCO-CYTOSOL") == {
        "CCO-OUT": "EXTRACELLULAR",
        "CCO-IN": "CYTOSOL",
    }
    assert r.split_location_string("CCO-CYTOSOL-CCO-EXTRACELLULAR") == {
        "CCO-OUT": "CYTOSOL",
        "CCO-IN": "EXTRACELLULAR",
    }


def test_fix_compartments_both_in() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(base_id="cpd1", id="cpd1", formula={"C": 1}, charge=1),
        "cpd2_c": ParseCompound(base_id="cpd2", id="cpd2", formula={"C": 1}, charge=1),
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            locations=[],
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.fix_reaction_compartments("RXN1")
    assert r.compounds["cpd1_c"].compartment == "CYTOSOL"
    assert r.compounds["cpd2_c"].compartment == "CYTOSOL"
    assert r.reactions["RXN1_c"].substrates == {"cpd1_c": -1}
    assert r.reactions["RXN1_c"].products == {"cpd2_c": 1}


def test_fix_compartments_both_out() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(base_id="cpd1", id="cpd1", formula={"C": 1}, charge=1),
        "cpd2_c": ParseCompound(base_id="cpd2", id="cpd2", formula={"C": 1}, charge=1),
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-OUT"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-OUT"},
            locations=[],
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.fix_reaction_compartments("RXN1")
    assert r.compounds["cpd1_c"].compartment == "CYTOSOL"
    assert r.compounds["cpd2_c"].compartment == "CYTOSOL"
    assert r.compounds["cpd1_e"].compartment == "EXTRACELLULAR"
    assert r.compounds["cpd2_e"].compartment == "EXTRACELLULAR"
    assert r.reactions["RXN1_e"].substrates == {"cpd1_e": -1}
    assert r.reactions["RXN1_e"].products == {"cpd2_e": 1}
    with pytest.raises(KeyError):
        r.reactions["RXN1"]


def test_fix_compartments_in_out() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(base_id="cpd1", id="cpd1", formula={"C": 1}, charge=1),
        "cpd2_c": ParseCompound(base_id="cpd2", id="cpd2", formula={"C": 1}, charge=1),
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-IN"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-OUT"},
            locations=[],
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.fix_reaction_compartments("RXN1")
    assert r.compounds["cpd1_c"].compartment == "CYTOSOL"
    assert r.compounds["cpd2_c"].compartment == "CYTOSOL"
    assert r.compounds["cpd2_e"].compartment == "EXTRACELLULAR"
    assert r.reactions["RXN1_c_e"].substrates == {"cpd1_c": -1}
    assert r.reactions["RXN1_c_e"].products == {"cpd2_e": 1}
    with pytest.raises(KeyError):
        r.reactions["RXN1"]


def test_fix_compartments_out_in() -> None:
    compounds: Dict[str, ParseCompound] = {
        "cpd1_c": ParseCompound(base_id="cpd1", id="cpd1", formula={"C": 1}, charge=1),
        "cpd2_c": ParseCompound(base_id="cpd2", id="cpd2", formula={"C": 1}, charge=1),
    }
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            substrate_compartments={"cpd1_c": "CCO-OUT"},
            products={"cpd2_c": 1},
            product_compartments={"cpd2_c": "CCO-IN"},
            locations=[],
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.fix_reaction_compartments("RXN1")
    assert r.compounds["cpd1_c"].compartment == "CYTOSOL"
    assert r.compounds["cpd2_c"].compartment == "CYTOSOL"
    assert r.compounds["cpd1_e"].compartment == "EXTRACELLULAR"
    assert r.reactions["RXN1_c_e"].substrates == {"cpd1_e": -1}
    assert r.reactions["RXN1_c_e"].products == {"cpd2_c": 1}
    with pytest.raises(KeyError):
        r.reactions["RXN1"]


def test_fix_compartments_periplasm() -> None:
    locations = [
        "CCO-CHL-THY-MEM",
        "CCO-CHLOR-STR",
        "CCO-MIT-IM-SPC",
        "CCO-MIT-IMEM",
        "CCO-OUTER-MEM",
        "CCO-PERI-BAC",
        "CCO-PERI-BAC-GN",
        "CCO-PERIPLASM",
        "CCO-PLASMA-MEM",
        "CCO-PLAST-IMEM",
        "CCO-PM-ANIMAL",
        "CCO-PM-BAC-ACT",
        "CCO-PM-BAC-NEG",
        "CCO-PM-BAC-POS",
        "CCO-RGH-ER-MEM",
        "CCO-VAC-MEM",
    ]
    for location in locations:
        compounds: Dict[str, ParseCompound] = {
            "cpd1_c": ParseCompound(base_id="cpd1", id="cpd1", formula={"C": 1}, charge=1),
            "cpd2_c": ParseCompound(base_id="cpd2", id="cpd2", formula={"C": 1}, charge=1),
        }
        compound_types: Dict[str, List[str]] = {}
        reactions: Dict[str, ParseReaction] = {
            "RXN1": ParseReaction(
                id="RXN1",
                base_id="RXN1",
                substrates={"cpd1_c": -1},
                substrate_compartments={"cpd1_c": "CCO-IN"},
                products={"cpd2_c": 1},
                product_compartments={"cpd2_c": "CCO-OUT"},
                locations=[location],
            )
        }
        r = Repairer(
            compounds=compounds,
            compound_types=compound_types,
            reactions=reactions,
            compartment_map=COMPARTMENT_MAP,
        )
        r.fix_reaction_compartments("RXN1")
        assert r.compounds["cpd1_c"].compartment == "CYTOSOL"
        assert r.compounds["cpd2_c"].compartment == "CYTOSOL"
        assert r.compounds["cpd2_p"].compartment == "PERIPLASM"
        assert r.reactions["RXN1_c_p"].substrates == {"cpd1_c": -1}
        assert r.reactions["RXN1_c_p"].products == {"cpd2_p": 1}
        with pytest.raises(KeyError):
            r.reactions["RXN1"]


def test_fix_compartments_extracellular() -> None:
    locations = ["CCO-EXTRACELLULAR"]
    for location in locations:
        compounds: Dict[str, ParseCompound] = {
            "cpd1_c": ParseCompound(base_id="cpd1", id="cpd1", formula={"C": 1}, charge=1),
            "cpd2_c": ParseCompound(base_id="cpd2", id="cpd2", formula={"C": 1}, charge=1),
        }
        compound_types: Dict[str, List[str]] = {}
        reactions: Dict[str, ParseReaction] = {
            "RXN1": ParseReaction(
                id="RXN1",
                base_id="RXN1",
                substrates={"cpd1_c": -1},
                substrate_compartments={"cpd1_c": "CCO-IN"},
                products={"cpd2_c": 1},
                product_compartments={"cpd2_c": "CCO-OUT"},
                locations=[location],
            )
        }
        r = Repairer(
            compounds=compounds,
            compound_types=compound_types,
            reactions=reactions,
            compartment_map=COMPARTMENT_MAP,
        )
        r.fix_reaction_compartments("RXN1")
        assert r.compounds["cpd1_c"].compartment == "CYTOSOL"
        assert r.compounds["cpd2_c"].compartment == "CYTOSOL"
        assert r.compounds["cpd2_e"].compartment == "EXTRACELLULAR"
        assert r.reactions["RXN1_c_e"].substrates == {"cpd1_c": -1}
        assert r.reactions["RXN1_c_e"].products == {"cpd2_e": 1}
        with pytest.raises(KeyError):
            r.reactions["RXN1"]


def test_fix_compartments_transporters_c_c() -> None:
    locations = [
        "CCO-CYTOSOL-CCO-MIT-LUM",
        "CCO-CYTOSOL-CCO-VAC-LUM",
        "CCO-MIT-LUM-CCO-CYTOSOL",
        "CCO-PEROX-LUM-CCO-CYTOSOL",
        "CCO-RGH-ER-LUM-CCO-CYTOSOL",
        "CCO-CYTOSOL",
        "CCO-IN",
        "CCO-LYS-LUM",
        "CCO-MIT-LUM",
        "CCO-GOLGI-LUM",
        "CCO-PEROX-LUM",
        "CCO-RGH-ER-LUM",
    ]
    for location in locations:
        compounds: Dict[str, ParseCompound] = {
            "cpd1_c": ParseCompound(base_id="cpd1", id="cpd1", formula={"C": 1}, charge=1),
            "cpd2_c": ParseCompound(base_id="cpd2", id="cpd2", formula={"C": 1}, charge=1),
        }
        compound_types: Dict[str, List[str]] = {}
        reactions: Dict[str, ParseReaction] = {
            "RXN1": ParseReaction(
                id="RXN1",
                base_id="RXN1",
                substrates={"cpd1_c": -1},
                substrate_compartments={"cpd1_c": "CCO-IN"},
                products={"cpd2_c": 1},
                product_compartments={"cpd2_c": "CCO-OUT"},
                locations=[location],
            )
        }
        r = Repairer(
            compounds=compounds,
            compound_types=compound_types,
            reactions=reactions,
            compartment_map=COMPARTMENT_MAP,
        )
        r.fix_reaction_compartments("RXN1")
        assert r.compounds["cpd1_c"].compartment == "CYTOSOL"
        assert r.compounds["cpd2_c"].compartment == "CYTOSOL"
        assert r.reactions["RXN1_c"].substrates == {"cpd1_c": -1}
        assert r.reactions["RXN1_c"].products == {"cpd2_c": 1}
        with pytest.raises(KeyError):
            r.reactions["RXN1"]


def test_fix_compartments_transporters_c_p() -> None:
    locations = [
        "CCO-CHLOR-STR-CCO-CYTOSOL",
        "CCO-SIDE-2-CCO-SIDE-1",
        "CCO-PERI-BAC-CCO-CYTOSOL",
        "CCO-PERI-BAC-CCO-IN",
        "CCO-CHLOR-STR-CCO-THY-LUM-CYA",
        "CCO-MIT-IM-SPC-CCO-MIT-LUM",
    ]
    for location in locations:
        compounds: Dict[str, ParseCompound] = {
            "cpd1_c": ParseCompound(base_id="cpd1", id="cpd1", formula={"C": 1}, charge=1),
            "cpd2_c": ParseCompound(base_id="cpd2", id="cpd2", formula={"C": 1}, charge=1),
        }
        compound_types: Dict[str, List[str]] = {}
        reactions: Dict[str, ParseReaction] = {
            "RXN1": ParseReaction(
                id="RXN1",
                base_id="RXN1",
                substrates={"cpd1_c": -1},
                substrate_compartments={"cpd1_c": "CCO-IN"},
                products={"cpd2_c": 1},
                product_compartments={"cpd2_c": "CCO-OUT"},
                locations=[location],
            )
        }
        r = Repairer(
            compounds=compounds,
            compound_types=compound_types,
            reactions=reactions,
            compartment_map=COMPARTMENT_MAP,
        )
        r.fix_reaction_compartments("RXN1")
        assert r.compounds["cpd1_c"].compartment == "CYTOSOL"
        assert r.compounds["cpd2_c"].compartment == "CYTOSOL"
        assert r.compounds["cpd2_p"].compartment == "PERIPLASM"
        assert r.reactions["RXN1_c_p"].substrates == {"cpd1_c": -1}
        assert r.reactions["RXN1_c_p"].products == {"cpd2_p": 1}
        with pytest.raises(KeyError):
            r.reactions["RXN1"]


def test_fix_compartments_transporters_p_p() -> None:
    locations = [
        "CCO-PERI-BAC-CCO-PERI-BAC",
    ]
    for location in locations:
        compounds: Dict[str, ParseCompound] = {
            "cpd1_c": ParseCompound(base_id="cpd1", id="cpd1", formula={"C": 1}, charge=1),
            "cpd2_c": ParseCompound(base_id="cpd2", id="cpd2", formula={"C": 1}, charge=1),
        }
        compound_types: Dict[str, List[str]] = {}
        reactions: Dict[str, ParseReaction] = {
            "RXN1": ParseReaction(
                id="RXN1",
                base_id="RXN1",
                substrates={"cpd1_c": -1},
                substrate_compartments={"cpd1_c": "CCO-IN"},
                products={"cpd2_c": 1},
                product_compartments={"cpd2_c": "CCO-OUT"},
                locations=[location],
                gibbs0=0,
            )
        }
        r = Repairer(
            compounds=compounds,
            compound_types=compound_types,
            reactions=reactions,
            compartment_map=COMPARTMENT_MAP,
        )
        r.fix_reaction_compartments("RXN1")
        assert r.compounds["cpd1_c"].compartment == "CYTOSOL"
        assert r.compounds["cpd2_c"].compartment == "CYTOSOL"
        assert r.compounds["cpd1_p"].compartment == "PERIPLASM"
        assert r.compounds["cpd2_p"].compartment == "PERIPLASM"
        assert r.reactions["RXN1_p"].substrates == {"cpd1_p": -1}
        assert r.reactions["RXN1_p"].products == {"cpd2_p": 1}
        with pytest.raises(KeyError):
            r.reactions["RXN1"]


def test_fix_compartments_transporters_p_c() -> None:
    locations = [
        "CCO-CYTOSOL-CCO-CHLOR-STR",
        "CCO-CYTOSOL-CCO-CHROM-STR",
        "CCO-CYTOSOL-CCO-PLASTID-STR",
        "CCO-CYTOSOL-CCO-VESICLE",
        "CCO-SIDE-1-CCO-SIDE-2",
    ]
    for location in locations:
        compounds: Dict[str, ParseCompound] = {
            "cpd1_c": ParseCompound(
                id="cpd1_c",
                base_id="cpd1",
                formula={"C": 1},
                charge=1,
            ),
            "cpd2_c": ParseCompound(
                id="cpd2_c",
                base_id="cpd2",
                formula={"C": 1},
                charge=1,
            ),
        }
        compound_types: Dict[str, List[str]] = {}
        reactions: Dict[str, ParseReaction] = {
            "RXN1": ParseReaction(
                id="RXN1",
                base_id="RXN1",
                substrates={"cpd1_c": -1},
                substrate_compartments={"cpd1_c": "CCO-IN"},
                products={"cpd2_c": 1},
                product_compartments={"cpd2_c": "CCO-OUT"},
                locations=[location],
            )
        }
        r = Repairer(
            compounds=compounds,
            compound_types=compound_types,
            reactions=reactions,
            compartment_map=COMPARTMENT_MAP,
        )
        r.fix_reaction_compartments("RXN1")
        assert r.compounds["cpd1_c"].compartment == "CYTOSOL"
        assert r.compounds["cpd2_c"].compartment == "CYTOSOL"
        assert r.compounds["cpd1_p"].compartment == "PERIPLASM"
        assert r.reactions["RXN1_p_c"].substrates == {"cpd1_p": -1}
        assert r.reactions["RXN1_p_c"].products == {"cpd2_c": 1}
        with pytest.raises(KeyError):
            r.reactions["RXN1"]


def test_fix_compartments_transporters_c_e() -> None:
    locations = [
        "CCO-EXTRACELLULAR-CCO-CYTOSOL",
        "CCO-EXTRACELLULAR-CCO-IN",
        "CCO-EXTRACELLULAR-CCO-UNKNOWN-SPACE",
        "CCO-OUT-CCO-CYTOSOL",
        "CCO-OUT-CCO-IN",
        "CCO-OUT-CCO-RGH-ER-LUM",
        "CCO-OUT",
    ]
    for location in locations:
        compounds: Dict[str, ParseCompound] = {
            "cpd1_c": ParseCompound(base_id="cpd1", id="cpd1", formula={"C": 1}, charge=1),
            "cpd2_c": ParseCompound(base_id="cpd2", id="cpd2", formula={"C": 1}, charge=1),
        }
        compound_types: Dict[str, List[str]] = {}
        reactions: Dict[str, ParseReaction] = {
            "RXN1": ParseReaction(
                id="RXN1",
                base_id="RXN1",
                substrates={"cpd1_c": -1},
                substrate_compartments={"cpd1_c": "CCO-IN"},
                products={"cpd2_c": 1},
                product_compartments={"cpd2_c": "CCO-OUT"},
                locations=[location],
            ),
        }
        r = Repairer(
            compounds=compounds,
            compound_types=compound_types,
            reactions=reactions,
            compartment_map=COMPARTMENT_MAP,
        )
        r.fix_reaction_compartments("RXN1")
        assert r.compounds["cpd1_c"].compartment == "CYTOSOL"
        assert r.compounds["cpd2_c"].compartment == "CYTOSOL"
        assert r.compounds["cpd2_e"].compartment == "EXTRACELLULAR"
        assert r.reactions["RXN1_c_e"].substrates == {"cpd1_c": -1}
        assert r.reactions["RXN1_c_e"].products == {"cpd2_e": 1}
        with pytest.raises(KeyError):
            r.reactions["RXN1"]


def test_fix_compartments_transporters_e_e() -> None:
    locations = ["CCO-OUT-CCO-EXTRACELLULAR"]
    for location in locations:
        compounds: Dict[str, ParseCompound] = {
            "cpd1_c": ParseCompound(base_id="cpd1", id="cpd1", formula={"C": 1}, charge=1),
            "cpd2_c": ParseCompound(base_id="cpd2", id="cpd2", formula={"C": 1}, charge=1),
        }
        compound_types: Dict[str, List[str]] = {}
        reactions: Dict[str, ParseReaction] = {
            "RXN1": ParseReaction(
                id="RXN1",
                base_id="RXN1",
                substrates={"cpd1_c": -1},
                substrate_compartments={"cpd1_c": "CCO-IN"},
                products={"cpd2_c": 1},
                product_compartments={"cpd2_c": "CCO-OUT"},
                locations=[location],
            )
        }
        r = Repairer(
            compounds=compounds,
            compound_types=compound_types,
            reactions=reactions,
            compartment_map=COMPARTMENT_MAP,
        )
        r.fix_reaction_compartments("RXN1")
        assert r.compounds["cpd1_c"].compartment == "CYTOSOL"
        assert r.compounds["cpd2_c"].compartment == "CYTOSOL"
        assert r.compounds["cpd1_e"].compartment == "EXTRACELLULAR"
        assert r.reactions["RXN1_e"].substrates == {"cpd1_e": -1}
        assert r.reactions["RXN1_e"].products == {"cpd2_e": 1}
        with pytest.raises(KeyError):
            r.reactions["RXN1"]


def test_set_stoichiometry_basic_case() -> None:
    compounds: Dict[str, ParseCompound] = {}
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            products={"cpd2_c": 1},
        )
    }

    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    res = r.set_reaction_stoichiometry(r.reactions["RXN1"])
    assert res
    assert r.reactions["RXN1"].stoichiometries == {"cpd1_c": -1, "cpd2_c": 1}


def test_set_stoichiometry_to_be_removed() -> None:
    compounds: Dict[str, ParseCompound] = {}
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            products={"cpd1_c": 1},
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    res = r.set_reaction_stoichiometry(r.reactions["RXN1"])
    assert not res


def test_set_stoichiometry_empty_products() -> None:
    compounds: Dict[str, ParseCompound] = {}
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -2},
            products={"cpd1_c": 1},
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    res = r.set_reaction_stoichiometry(r.reactions["RXN1"])
    assert not res


def test_set_stoichiometry_empty_products2() -> None:
    compounds: Dict[str, ParseCompound] = {}
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -2},
            products={},
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    res = r.set_reaction_stoichiometry(r.reactions["RXN1"])
    assert not res


def test_set_stoichiometry_empty_substrates() -> None:
    compounds: Dict[str, ParseCompound] = {}
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1},
            products={"cpd1_c": 2},
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    res = r.set_reaction_stoichiometry(r.reactions["RXN1"])
    assert not res


def test_set_stoichiometry_empty_substrates2() -> None:
    compounds: Dict[str, ParseCompound] = {}
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={},
            products={"cpd1_c": 2},
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    res = r.set_reaction_stoichiometry(r.reactions["RXN1"])
    assert not res


def test_set_stoichiometry_remove_duplicates() -> None:
    compounds: Dict[str, ParseCompound] = {}
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -2},
            products={"cpd1_c": 1, "cpd2_c": 1},
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    res = r.set_reaction_stoichiometry(r.reactions["RXN1"])
    assert res
    assert r.reactions["RXN1"].stoichiometries == {"cpd1_c": -1, "cpd2_c": 1}


def test_set_stoichiometry_remove_duplicates2() -> None:
    compounds: Dict[str, ParseCompound] = {}
    compound_types: Dict[str, List[str]] = {}
    reactions: Dict[str, ParseReaction] = {
        "RXN1": ParseReaction(
            id="RXN1",
            base_id="RXN1",
            substrates={"cpd1_c": -1, "cpd2_c": -1},
            products={"cpd1_c": 2},
        )
    }
    r = Repairer(
        compounds=compounds,
        compound_types=compound_types,
        reactions=reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    res = r.set_reaction_stoichiometry(r.reactions["RXN1"])
    assert res
    assert r.reactions["RXN1"].stoichiometries == {"cpd2_c": -1, "cpd1_c": 1}
