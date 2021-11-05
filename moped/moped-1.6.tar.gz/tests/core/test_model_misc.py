from moped import Compound, Model, Reaction


def test_str_and_repr() -> None:
    m = Model()
    assert repr(m) == "Model: Model\n    compounds: 0\n    reactions: 0\n"
    assert str(m) == "Model: Model\n    compounds: 0\n    reactions: 0\n"

    m.add_compartment(compartment_id="c", compartment_suffix="c")
    m.add_compound(Compound(base_id="cpd1", compartment="c"))
    m.add_compound(Compound(base_id="cpd2", compartment="c"))
    m.add_reaction(Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}))
    assert repr(m) == "Model: Model\n    compounds: 2\n    reactions: 1\n"
    assert str(m) == "Model: Model\n    compounds: 2\n    reactions: 1\n"


def test_str_and_repr_name() -> None:
    m = Model(name="My model name")
    assert repr(m) == "Model: My model name\n    compounds: 0\n    reactions: 0\n"
    assert str(m) == "Model: My model name\n    compounds: 0\n    reactions: 0\n"

    m.add_compartment(compartment_id="c", compartment_suffix="c")
    m.add_compound(Compound(base_id="cpd1", compartment="c"))
    m.add_compound(Compound(base_id="cpd2", compartment="c"))
    m.add_reaction(Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}))
    assert repr(m) == "Model: My model name\n    compounds: 2\n    reactions: 1\n"
    assert str(m) == "Model: My model name\n    compounds: 2\n    reactions: 1\n"


def test_copy() -> None:
    m1 = Model()
    m1.add_compartment(compartment_id="c", compartment_suffix="c")
    m1.add_compound(Compound(base_id="cpd1", compartment="c"))
    m1.add_compound(Compound(base_id="cpd2", compartment="c"))
    m1.add_reaction(Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}))
    m2 = m1.copy()
    assert m1 is not m2
    assert m1.compounds == m2.compounds
    assert m1.reactions == m2.reactions
    assert m1.compounds["cpd1_c"] is not m2.compounds["cpd1_c"]
    assert m1.compounds["cpd2_c"] is not m2.compounds["cpd2_c"]
    assert m1.reactions["rxn1"] is not m2.reactions["rxn1"]


def test_context_manager_copy() -> None:
    m1 = Model()
    m1.add_compartment(compartment_id="c", compartment_suffix="c")
    m1.add_compound(Compound(base_id="cpd1", compartment="c"))
    m1.add_compound(Compound(base_id="cpd2", compartment="c"))
    m1.add_reaction(Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}))
    with m1 as m2:
        assert m1 is not m2
        assert m1.compounds == m2.compounds
        assert m1.reactions == m2.reactions
        assert m1.compounds["cpd1_c"] is not m2.compounds["cpd1_c"]
        assert m1.compounds["cpd2_c"] is not m2.compounds["cpd2_c"]
        assert m1.reactions["rxn1"] is not m2.reactions["rxn1"]


def test_context_manager_restore_changes() -> None:
    m1 = Model()
    m1.add_compartment(compartment_id="c", compartment_suffix="c")
    m1.add_compound(Compound(base_id="cpd1", compartment="c"))
    m1.add_compound(Compound(base_id="cpd2", compartment="c"))
    m1.add_reaction(Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}))
    with m1:
        m1.add_compound(Compound(base_id="cpd3", compartment="c"))
    assert tuple(m1.compounds.keys()) == ("cpd1_c", "cpd2_c")


def test_create_submodel() -> None:
    m1 = Model()
    m1.add_compartment(compartment_id="c", compartment_suffix="c")
    m1.add_compound(Compound(base_id="cpd1", compartment="c"))
    m1.add_compound(Compound(base_id="cpd2", compartment="c"))
    m1.add_compound(Compound(base_id="cpd3", compartment="c"))
    m1.add_reaction(Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}))
    m1.add_reaction(Reaction(id="rxn2", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}))

    m2 = m1.create_submodel(reaction_ids=["rxn1"])
    assert m2.name == "Model submodel"
    assert set(m2.compounds.keys()) == {"cpd1_c", "cpd2_c"}
    assert set(m2.reactions.keys()) == {
        "rxn1",
    }

    m2 = m1.create_submodel(reaction_ids=["rxn1"], name="test")
    assert m2.name == "test"
