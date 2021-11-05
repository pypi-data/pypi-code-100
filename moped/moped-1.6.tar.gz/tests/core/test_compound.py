from moped import Compound


def test_initialization_cytosol() -> None:
    cpd = Compound(base_id="CPD001", compartment="CYTOSOL")
    assert cpd.base_id == "CPD001"
    assert cpd.compartment == "CYTOSOL"


def test_initialization_compartment_periplasm() -> None:
    cpd = Compound(base_id="CPD001", compartment="PERIPLASM")
    assert cpd.base_id == "CPD001"
    assert cpd.compartment == "PERIPLASM"


def test_initialization_compartment_extracellular() -> None:
    cpd = Compound(base_id="CPD001", compartment="EXTRACELLULAR")
    assert cpd.base_id == "CPD001"
    assert cpd.compartment == "EXTRACELLULAR"


def test_initialize_name() -> None:
    c = Compound(base_id="CPD001", compartment="CYTOSOL", name="compound")
    assert c.name == "compound"


def test_initialize_formula() -> None:
    c = Compound(base_id="CPD001", compartment="CYTOSOL", formula={"C": 1})
    assert c.formula == {"C": 1}


def test_initialize_charge() -> None:
    c = Compound(base_id="CPD001", compartment="CYTOSOL", charge=1)
    assert c.charge == 1


def test_initialize_gibbs0() -> None:
    c = Compound(base_id="CPD001", compartment="CYTOSOL", gibbs0=1)
    assert c.gibbs0 == 1


def test_initialize_smiles() -> None:
    c = Compound(base_id="CPD001", compartment="CYTOSOL", smiles="CN=C=O")
    assert c.smiles == "CN=C=O"


def test_initialize_types() -> None:
    c = Compound(base_id="CPD001", compartment="CYTOSOL", types=["small-molecule"])
    assert c.types == ["small-molecule"]


def test_initialize_in_reaction() -> None:
    c = Compound(base_id="CPD001", compartment="CYTOSOL", in_reaction={"rxn-1"})
    assert c.in_reaction == {"rxn-1"}


def test_comparisons() -> None:
    c1 = Compound(base_id="CPD1", compartment="CYTOSOL")
    c1.id = "CDP1_c"
    c2 = Compound(base_id="CPD2", compartment="CYTOSOL")
    c2.id = "CDP2_c"

    assert c1 == c1
    assert c1 != c2
    assert c1 < c2
    assert c1 <= c2
    assert c2 > c1
    assert c2 >= c1


def test_iter() -> None:
    c = Compound(
        base_id="CPD001",
        name="CPD001",
        formula={"C": 1},
        charge=1,
        gibbs0=1,
        compartment="CYTOSOL",
        smiles="CN=C=O",
        types=["small-molecule"],
        in_reaction={"rxn-1"},
    )
    assert dict(c) == {
        "base_id": "CPD001",
        "name": "CPD001",
        "formula": {"C": 1},
        "charge": 1,
        "gibbs0": 1,
        "compartment": "CYTOSOL",
        "smiles": "CN=C=O",
        "types": ["small-molecule"],
        "in_reaction": {"rxn-1"},
    }


def test_str() -> None:
    c = Compound(
        base_id="CPD001",
        name="CPD001",
        formula={"C": 1},
        charge=1,
        gibbs0=1,
        compartment="CYTOSOL",
        smiles="CN=C=O",
        types=["small-molecule"],
        in_reaction={"rxn-1"},
    )
    c.id = "CPD001_c"

    assert str(c).split("\n") == [
        "Compound <CPD001_c>",
        "    base_id: CPD001",
        "    id: CPD001_c",
        "    name: CPD001",
        "    compartment: CYTOSOL",
        "    formula: {'C': 1}",
        "    charge: 1",
        "    gibbs0: 1",
        "    smiles: CN=C=O",
        "    types: ['small-molecule']",
        "    in_reaction: {'rxn-1'}",
    ]


def test_repr() -> None:
    c = Compound(
        base_id="CPD001",
        name="CPD001",
        formula={"C": 1},
        charge=1,
        gibbs0=1,
        compartment="CYTOSOL",
        smiles="CN=C=O",
        types=["small-molecule"],
        in_reaction={"rxn-1"},
    )
    c.id = "CPD001_c"
    assert repr(c).split(", ") == [
        "Compound(base_id='CPD001'",
        "id='CPD001_c'",
        "name='CPD001'",
        "compartment='CYTOSOL'",
        "formula={'C': 1}",
        "charge=1",
        "gibbs0=1",
        "smiles='CN=C=O'",
        "types=['small-molecule']",
        "in_reaction={'rxn-1'})",
    ]


def test_formula_to_string() -> None:
    c = Compound(base_id="CPD001", compartment="CYTOSOL", formula={"C": 1})
    assert c.formula_to_string() == "C1"


def test_formula_to_string_two_atoms() -> None:
    c = Compound(base_id="CPD001", compartment="CYTOSOL", formula={"C": 1, "H": 12})
    assert c.formula_to_string() == "C1H12"
