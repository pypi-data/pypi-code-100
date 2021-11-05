from moped import Compound, Model, Reaction

import pytest


def test_add_compound() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="CYTOSOL"))
    assert tuple(m.compounds.keys()) == ("cpd1_c",)


def test_compound_independence() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    compound = Compound(base_id="cpd1", compartment="CYTOSOL")
    m1 = Model(compartments=compartments)
    m2 = Model(compartments=compartments)
    m1.add_compound(compound)
    m2.add_compound(compound)
    m2.compounds["cpd1_c"].in_reaction.add("rxn1_c")
    assert m1.compounds["cpd1_c"].in_reaction == set()
    assert m2.compounds["cpd1_c"].in_reaction == {"rxn1_c"}


def test_add_compound_nonsense_input_str() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    with pytest.raises(TypeError):
        m.add_compound("cpd")  # type: ignore


def test_add_compound_nonsense_input_int() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    with pytest.raises(TypeError):
        m.add_compound(1)  # type: ignore


def test_add_compound_nonsense_input_float() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    with pytest.raises(TypeError):
        m.add_compound(1.0)  # type: ignore


def test_add_compound_nonsense_input_none() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    with pytest.raises(TypeError):
        m.add_compound(None)  # type: ignore


def test_add_compound_nonsense_input_list() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    cpd1 = Compound(base_id="cpd1", compartment="CYTOSOL")
    with pytest.raises(TypeError):
        m.add_compound([cpd1])  # type: ignore


def test_add_compound_nonsense_input_set() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    cpd1 = Compound(base_id="cpd1", compartment="CYTOSOL")
    with pytest.raises(TypeError):
        m.add_compound({cpd1})  # type: ignore


def test_add_compound_nonsense_input_dict() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    cpd1 = Compound(base_id="cpd1", compartment="CYTOSOL")
    with pytest.raises(TypeError):
        m.add_compound({"key": cpd1})  # type: ignore


def test_add_compound_nonsense_input_dict2() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    cpd1 = Compound(base_id="cpd1", compartment="CYTOSOL")
    with pytest.raises(TypeError):
        m.add_compound({cpd1: "value"})  # type: ignore


def test_add_compounds() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
        )
    )
    assert tuple(m.compounds.keys()) == ("cpd1_c", "cpd2_c")


def test_add_compartment_compound_variant_extracellular() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="CYTOSOL"))
    m.add_compartment_compound_variant("cpd1_c", "EXTRACELLULAR")
    assert tuple(m.compounds.keys()) == ("cpd1_c", "cpd1_e")
    assert m.compounds["cpd1_c"].compartment == "CYTOSOL"
    assert m.compounds["cpd1_e"].compartment == "EXTRACELLULAR"


def test_add_compartment_compound_variant_in_reaction() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
        )
    )
    m.add_reaction(Reaction(id="rxn1_c", base_id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}))
    m.add_compartment_compound_variant("cpd1_c", "EXTRACELLULAR")
    assert m.compounds["cpd1_c"].in_reaction == set(["rxn1_c"])
    assert m.compounds["cpd1_e"].in_reaction == set()


def test_add_compartment_compound_missing_compound() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    with pytest.raises(KeyError):
        m.add_compartment_compound_variant("cpd1_c", "EXTRACELLULAR")


def test_set_compound_property() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    cpd1 = Compound(base_id="cpd1", compartment="CYTOSOL")
    m.add_compound(cpd1)
    m.set_compound_property(
        "cpd1_c",
        {
            "id": "cpd1_c",
            "name": "cpd2_c",
            "formula": {"C": 1, "H": 4},
            "charge": 5,
            "gibbs0": 4,
            "compartment": "_p",
            "smiles": "CH4",
            "types": ["Some type"],
            "in_reaction": ["rxn1_c"],
        },
    )
    assert m.compounds["cpd1_c"].id == "cpd1_c"
    assert m.compounds["cpd1_c"].name == "cpd2_c"
    assert m.compounds["cpd1_c"].formula == {"C": 1, "H": 4}
    assert m.compounds["cpd1_c"].charge == 5
    assert m.compounds["cpd1_c"].gibbs0 == 4
    assert m.compounds["cpd1_c"].compartment == "_p"
    assert m.compounds["cpd1_c"].smiles == "CH4"
    assert m.compounds["cpd1_c"].types == ["Some type"]
    assert m.compounds["cpd1_c"].in_reaction == ["rxn1_c"]


def test_set_compound_property_wrong_key() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    cpd1 = Compound(base_id="cpd1", compartment="CYTOSOL")
    m.add_compound(cpd1)
    with pytest.raises(KeyError):
        m.set_compound_property("cpd1_c", {"bogus-key": "bogus-value"})


def test_remove_compound() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
        )
    )
    m.remove_compound("cpd1_c")
    assert tuple(m.compounds.keys()) == ("cpd2_c",)


def test_remove_compounds_tuple() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
            Compound(base_id="cpd3", compartment="CYTOSOL"),
        )
    )
    m.remove_compounds(("cpd1_c", "cpd3_c"))
    assert tuple(m.compounds.keys()) == ("cpd2_c",)


def test_remove_compounds_list() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
            Compound(base_id="cpd3", compartment="CYTOSOL"),
        )
    )
    m.remove_compounds(["cpd1_c", "cpd3_c"])
    assert tuple(m.compounds.keys()) == ("cpd2_c",)


def test_remove_compounds_set() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
            Compound(base_id="cpd3", compartment="CYTOSOL"),
        )
    )
    m.remove_compounds({"cpd1_c", "cpd3_c"})
    assert tuple(m.compounds.keys()) == ("cpd2_c",)


def test_remove_compounds_dict() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
            Compound(base_id="cpd3", compartment="CYTOSOL"),
        )
    )
    m.remove_compounds({"cpd1_c": 1, "cpd3_c": 1})
    assert tuple(m.compounds.keys()) == ("cpd2_c",)


def test_remove_compound_types() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL", types=["type1"]),
            Compound(base_id="cpd2", compartment="CYTOSOL", types=["type1"]),
        )
    )
    m.remove_compound(compound_id="cpd1_c")
    assert tuple(m.compounds.keys()) == ("cpd2_c",)
    assert m._compound_types == {"type1": {"cpd2_c"}}
    m.remove_compound(compound_id="cpd2_c")
    assert not bool(m.compounds)
    assert not bool(m._compound_types)


def test_remove_nonexistant_compound() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
        )
    )
    with pytest.raises(KeyError):
        m.remove_compound("cpd3")


def test_get_reactions_of_compound() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    v1 = Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1})
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
        )
    )
    m.add_reaction(v1)
    assert m.get_reactions_of_compound("cpd1_c") == set(["v1"])
    assert m.get_reactions_of_compound("cpd2_c") == set(["v1"])


def test_get_compounds_of_compartment() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m.add_compounds(
        (
            Compound(base_id="cpd0", compartment="CYTOSOL"),
            Compound(base_id="cpd1", compartment="PERIPLASM"),
            Compound(base_id="cpd2", compartment="EXTRACELLULAR"),
        )
    )
    assert m.get_compounds_of_compartment(compartment_id="CYTOSOL") == ["cpd0_c"]
    assert m.get_compounds_of_compartment(compartment_id="PERIPLASM") == ["cpd1_p"]
    assert m.get_compounds_of_compartment(compartment_id="EXTRACELLULAR") == ["cpd2_e"]
    with pytest.raises(KeyError):
        m.get_compounds_of_compartment(compartment_id="GARBAGE")


def test_compound_getters() -> None:
    m = Model()
    m.add_compartment(compartment_id="cytosol", compartment_suffix="c")
    m.add_compound(
        compound=Compound(
            base_id="cpd1",
            formula={"C": 6, "H": 12, "O": 6},
            charge=1,
            compartment="cytosol",
            gibbs0=1,
            name="Compound One",
            smiles="ABCDEFG",
            types=["type1", "type2"],
            in_reaction={"rxn1"},
            database_links={"kegg": {"some-cpd-id"}},
        )
    )

    assert m.get_compound_compartment_variants(compound_base_id="cpd1") == {"cpd1_c"}
    assert m.get_compound_base_id(compound_id="cpd1_c") == "cpd1"
    assert m.get_compound_compartment(compound_id="cpd1_c") == "cytosol"
    assert m.get_compound_formula(compound_id="cpd1_c") == {"C": 6, "H": 12, "O": 6}
    assert m.get_compound_charge(compound_id="cpd1_c") == 1
    assert m.get_compound_gibbs0(compound_id="cpd1_c") == 1
    assert m.get_compound_database_links(compound_id="cpd1_c") == {"kegg": {"some-cpd-id"}}
    assert m.get_compounds_of_type(compound_type="type1") == {"cpd1_c"}
    assert m.get_base_compound_ids() == {"cpd1"}
    assert m.get_compound_type_ids() == {"type2", "type1"}
    assert m.get_compounds_of_compartment(compartment_id="cytosol") == ["cpd1_c"]
