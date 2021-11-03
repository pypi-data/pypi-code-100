import io
from unittest import mock

from moped import Compound, Model, Reaction


def test_charge_balance_both_zero() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL", charge=0),
            Compound(base_id="cpd2", compartment="CYTOSOL", charge=0),
        )
    )
    m.add_reactions((Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),))
    assert m.check_charge_balance("v1")


def test_charge_balance_both_one() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL", charge=1),
            Compound(base_id="cpd2", compartment="CYTOSOL", charge=1),
        )
    )
    m.add_reactions((Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),))
    assert m.check_charge_balance("v1")


def test_charge_balance_substrate_stoichiometry() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL", charge=1),
            Compound(base_id="cpd2", compartment="CYTOSOL", charge=2),
        )
    )
    m.add_reactions((Reaction(id="v1", stoichiometries={"cpd1_c": -2, "cpd2_c": 1}),))
    assert m.check_charge_balance("v1")


def test_charge_balance_product_stoichiometry() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL", charge=2),
            Compound(base_id="cpd2", compartment="CYTOSOL", charge=1),
        )
    )
    m.add_reactions((Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 2}),))
    assert m.check_charge_balance("v1")


def test_charge_balance_fail_on_opposite_signs() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL", charge=-1),
            Compound(base_id="cpd2", compartment="CYTOSOL", charge=1),
        )
    )
    m.add_reactions((Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),))
    assert not m.check_charge_balance("v1")


def test_charge_balance_fail_on_opposite_signs2() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL", charge=1),
            Compound(base_id="cpd2", compartment="CYTOSOL", charge=-1),
        )
    )
    m.add_reactions((Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),))
    assert not m.check_charge_balance("v1")


def test_check_charge_balance_verbose() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL", charge=1.0),
            Compound(base_id="cpd2", compartment="CYTOSOL", charge=1.0),
        )
    )
    m.add_reactions((Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),))
    with mock.patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        m.check_charge_balance("v1", verbose=True)
        assert mock_stdout.getvalue().split("\n") == ["Substrate charge: 1.0", "Product charge: 1.0", ""]


def test_mass_balance_single_atom() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL", formula={"C": 1}),
            Compound(base_id="cpd2", compartment="CYTOSOL", formula={"C": 1}),
        )
    )
    m.add_reactions((Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),))
    assert m.check_mass_balance("v1")


def test_check_mass_balance_verbose() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL", formula={"C": 1}),
            Compound(base_id="cpd2", compartment="CYTOSOL", formula={"C": 1}),
        )
    )
    m.add_reactions((Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),))
    with mock.patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        m.check_mass_balance("v1", verbose=True)
        assert mock_stdout.getvalue().split("\n") == ["{'C': 1}", "{'C': 1}", ""]


def test_mass_balance_multiple_atoms() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(
                base_id="cpd1",
                compartment="CYTOSOL",
                formula={"C": 6, "H": 12, "O": 6},
            ),
            Compound(
                base_id="cpd2",
                compartment="CYTOSOL",
                formula={"C": 6, "H": 12, "O": 6},
            ),
        )
    )
    m.add_reactions((Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),))
    assert m.check_mass_balance("v1")


def test_check_mass_balance_missing_atom() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(
                base_id="cpd1",
                compartment="CYTOSOL",
                formula={"C": 6, "H": 12, "O": 6},
            ),
            Compound(
                base_id="cpd2",
                compartment="CYTOSOL",
                formula={
                    "C": 6,
                    "H": 12,
                },
            ),
        )
    )
    m.add_reactions((Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),))
    assert not m.check_mass_balance(reaction_id="v1")


def test_mass_balance_multiple_compounds() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(
                base_id="cpd1",
                compartment="CYTOSOL",
                formula={"C": 6, "H": 12, "O": 6},
            ),
            Compound(
                base_id="cpd2",
                compartment="CYTOSOL",
                formula={"C": 6, "H": 12, "O": 6},
            ),
            Compound(base_id="cpd3", compartment="CYTOSOL", formula={"C": 6}),
            Compound(base_id="cpd4", compartment="CYTOSOL", formula={"C": 6}),
        )
    )
    m.add_reactions(
        (
            Reaction(
                id="v1",
                stoichiometries={
                    "cpd1_c": -1,
                    "cpd3_c": -2,
                    "cpd2_c": 1,
                    "cpd4_c": 2,
                },
            ),
        )
    )
    assert m.check_mass_balance("v1")


def test_mass_balance_multiple_atoms_substrate_stoichiometry() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(
                base_id="cpd1",
                compartment="CYTOSOL",
                formula={"C": 3, "H": 6, "O": 3},
            ),
            Compound(
                base_id="cpd2",
                compartment="CYTOSOL",
                formula={"C": 6, "H": 12, "O": 6},
            ),
        )
    )
    m.add_reactions((Reaction(id="v1", stoichiometries={"cpd1_c": -2, "cpd2_c": 1}),))
    assert m.check_mass_balance("v1")


def test_mass_balance_multiple_atoms_product_stoichiometry() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(
                base_id="cpd1",
                compartment="CYTOSOL",
                formula={"C": 6, "H": 12, "O": 6},
            ),
            Compound(
                base_id="cpd2",
                compartment="CYTOSOL",
                formula={"C": 3, "H": 6, "O": 3},
            ),
        )
    )
    m.add_reactions((Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 2}),))
    assert m.check_mass_balance("v1")


def test_mass_balance_fail_on_missing_substrate_formula() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL", formula={}),
            Compound(
                base_id="cpd2",
                compartment="CYTOSOL",
                formula={"C": 3, "H": 6, "O": 3},
            ),
        )
    )
    m.add_reactions((Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 2}),))
    assert not m.check_mass_balance("v1")


def test_mass_balance_fail_on_missing_product_formula() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(
                base_id="cpd1",
                compartment="CYTOSOL",
                formula={"C": 3, "H": 6, "O": 3},
            ),
            Compound(base_id="cpd2", compartment="CYTOSOL", formula={}),
        )
    )
    m.add_reactions((Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 2}),))
    assert not m.check_mass_balance("v1")


def test_mass_balance_fail_on_missing_substrate_atom() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL", formula={"C": 1}),
            Compound(base_id="cpd2", compartment="CYTOSOL", formula={"C": 1, "H": 1}),
        )
    )
    m.add_reactions((Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 2}),))
    assert not m.check_mass_balance("v1")


def test_mass_balance_fail_on_missing_product_atom() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL", formula={"C": 1, "H": 1}),
            Compound(base_id="cpd2", compartment="CYTOSOL", formula={"C": 1}),
        )
    )
    m.add_reactions((Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 2}),))
    assert not m.check_mass_balance("v1")
