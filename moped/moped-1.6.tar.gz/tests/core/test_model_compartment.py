from moped import Compound, Model


def test_add_compartment_suffix() -> None:
    m = Model()
    m.add_compartment(compartment_id="cytosol", compartment_suffix="c")
    m.add_compound(Compound(base_id="cpd1", compartment="cytosol"))
    assert tuple(m.compounds.keys()) == ("cpd1_c",)


def test_add_compartment_suffix_empty() -> None:
    m = Model()
    m.add_compartment(compartment_id="cytosol", compartment_suffix="")
    m.add_compound(Compound(base_id="cpd1", compartment="cytosol"))
    assert tuple(m.compounds.keys()) == ("cpd1",)


def test_add_compartment_compound_variant_id() -> None:
    m = Model()
    m.add_compartments(compartments={"cytosol": "c", "extracellular": "e"})
    m.add_compound(Compound(base_id="cpd1", compartment="cytosol"))
    new_cpd = m.add_compartment_compound_variant(compound_id="cpd1_c", compartment_id="extracellular")
    assert new_cpd.base_id == "cpd1"
    assert new_cpd.id == "cpd1_e"
    assert new_cpd.in_reaction == set()
    assert new_cpd.compartment == "extracellular"
    assert tuple(m.compounds.keys()) == ("cpd1_c", "cpd1_e")


def test_add_compartment_compound_variant_base_id() -> None:
    m = Model()
    m.add_compartments(compartments={"cytosol": "c", "extracellular": "e"})
    m.add_compound(Compound(base_id="cpd1", compartment="cytosol"))
    new_cpd = m.add_compartment_compound_variant(compound_id="cpd1", compartment_id="extracellular")

    assert new_cpd.base_id == "cpd1"
    assert new_cpd.id == "cpd1_e"
    assert new_cpd.in_reaction == set()
    assert new_cpd.compartment == "extracellular"
    assert tuple(m.compounds.keys()) == ("cpd1_c", "cpd1_e")
