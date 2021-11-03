from moped import Compound, Model, Reaction

import pytest


def test_add_cpd_from_ref_new() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    db = Model(compartments=compartments)
    m = Model(compartments=compartments)
    db.add_compound(
        Compound(
            base_id="cpd1",
            compartment="CYTOSOL",
            formula={"C": 1},
            charge=1,
            gibbs0=10,
            smiles="abc",
            types=["cpd"],
        )
    )
    m.add_compound_from_reference(db, "cpd1_c")
    cpd = m.compounds["cpd1_c"]
    assert cpd.id == "cpd1_c"
    assert cpd.formula == {"C": 1}
    assert cpd.charge == 1
    assert cpd.gibbs0 == 10
    assert cpd.smiles == "abc"
    assert cpd.types == ["cpd"]
    assert cpd.in_reaction == set()


def test_add_cpd_from_ref_existing() -> None:
    """Should keep the in_reaction attribute"""
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    db = Model(compartments=compartments)
    m = Model(compartments=compartments)

    db.add_compounds(
        (
            Compound(
                base_id="cpd1",
                compartment="CYTOSOL",
                formula={"C": 1},
                charge=1,
                gibbs0=10,
                smiles="abc",
                types=["cpd"],
                in_reaction={"rxn2_c"},
            ),
        )
    )
    m.add_compounds((Compound(base_id="cpd1", compartment="CYTOSOL", in_reaction={"rxn1_c"}),))
    m.add_compound_from_reference(db, "cpd1_c")
    cpd = m.compounds["cpd1_c"]
    assert cpd.id == "cpd1_c"
    assert cpd.formula == {"C": 1}
    assert cpd.charge == 1
    assert cpd.gibbs0 == 10
    assert cpd.smiles == "abc"
    assert cpd.types == ["cpd"]
    assert cpd.in_reaction == {"rxn1_c"}


def test_add_reaction_from_ref_new() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    db = Model(compartments=compartments)
    m = Model(compartments=compartments)
    db.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
            Compound(base_id="cpd3", compartment="CYTOSOL"),
        )
    )
    db.add_reactions(
        (
            Reaction(
                id="rxn1_c",
                base_id="rxn1",
                stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
            ),
            Reaction(
                id="rxn2_c",
                base_id="rxn2",
                stoichiometries={"cpd2_c": -1, "cpd3_c": 1},
            ),
            Reaction(
                id="rxn3_c",
                base_id="rxn3",
                stoichiometries={"cpd1_c": -1, "cpd3_c": 1},
                pathways={"pwy1"},
            ),
        ),
    )
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
            Compound(base_id="cpd3", compartment="CYTOSOL"),
        )
    )
    m.add_reactions(
        (
            Reaction(
                id="rxn1_c",
                base_id="rxn1",
                stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
            ),
            Reaction(
                id="rxn2_c",
                base_id="rxn2",
                stoichiometries={"cpd2_c": -1, "cpd3_c": 1},
            ),
        )
    )
    m.add_reaction_from_reference(db, "rxn3_c")
    assert m.compounds["cpd1_c"].in_reaction == {"rxn1_c", "rxn3_c"}
    assert m.compounds["cpd2_c"].in_reaction == {"rxn1_c", "rxn2_c"}
    assert m.compounds["cpd3_c"].in_reaction == {"rxn2_c", "rxn3_c"}
    assert dict(m.pathways) == {"pwy1": {"rxn3_c"}}


def test_add_reaction_replacing() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    db = Model(compartments=compartments)
    m = Model(compartments=compartments)
    db.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
            Compound(base_id="cpd3", compartment="CYTOSOL"),
        ),
    )
    db.add_reactions(
        (
            Reaction(
                id="rxn1_c",
                base_id="rxn1",
                stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
            ),
            Reaction(
                id="rxn2_c",
                base_id="rxn2",
                stoichiometries={"cpd2_c": -1, "cpd3_c": 1},
            ),
            Reaction(
                id="rxn3_c",
                base_id="rxn3",
                stoichiometries={"cpd1_c": -1, "cpd3_c": 1},
                reversible=True,
                pathways={"pwy0"},
            ),
        ),
    )
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
            Compound(base_id="cpd3", compartment="CYTOSOL"),
        ),
    )
    m.add_reactions(
        (
            Reaction(
                id="rxn1_c",
                base_id="rxn1",
                stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
            ),
            Reaction(
                id="rxn2_c",
                base_id="rxn2",
                stoichiometries={"cpd2_c": -1, "cpd3_c": 1},
            ),
            Reaction(
                id="rxn3_c",
                base_id="rxn3",
                stoichiometries={"cpd2_c": -2, "cpd3_c": 2},
                reversible=False,
                pathways={"pwy1"},
            ),
        )
    )
    m.add_reaction_from_reference(db, "rxn3_c")
    assert m.compounds["cpd1_c"].in_reaction == {"rxn1_c", "rxn3_c"}
    assert m.compounds["cpd2_c"].in_reaction == {"rxn1_c", "rxn2_c"}
    assert m.compounds["cpd3_c"].in_reaction == {"rxn2_c", "rxn3_c"}

    assert m.reactions["rxn3_c"].stoichiometries == {"cpd1_c": -1, "cpd3_c": 1}
    assert m.reactions["rxn3_c"].reversible
    assert dict(m.pathways) == {"pwy0": {"rxn3_c"}}


def test_add_from_reference() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    db = Model(compartments=compartments)
    m = Model(compartments=compartments)
    db.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
        )
    )
    db.add_reactions(
        (
            Reaction(
                id="rxn1_c",
                base_id="rxn1",
                stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
            ),
        )
    )
    m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1_c")
    assert set(m.compounds.keys()) == {"cpd1_c", "cpd2_c"}
    assert set(m.reactions.keys()) == {"rxn1_c"}


def test_add_reaction_from_reference_missing_in_reference() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    db = Model(compartments=compartments)
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
        )
    )
    m.add_reaction(
        Reaction(
            id="rxn1_c",
            base_id="rxn1",
            stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
        )
    )
    with pytest.raises(KeyError):
        m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1_c")


def test_add_multiple_from_reference() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    db = Model(compartments=compartments)
    m = Model(compartments=compartments)
    db.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
        )
    )
    db.add_reactions(
        (
            Reaction(
                id="rxn1_c",
                base_id="rxn1",
                stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
            ),
            Reaction(
                id="rxn2_c",
                base_id="rxn1",
                stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
            ),
        )
    )
    m.add_reactions_from_reference(reference_model=db, reaction_ids=["rxn1_c", "rxn2_c"])
    assert set(m.compounds.keys()) == {"cpd1_c", "cpd2_c"}
    assert set(m.reactions.keys()) == {"rxn1_c", "rxn2_c"}


def test_add_from_reference_cof_removal_afterwards() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    db = Model(compartments=compartments)
    m = Model(compartments=compartments)
    db.add_compounds(
        (
            Compound(base_id="ATP", compartment="CYTOSOL"),
            Compound(base_id="ADP", compartment="CYTOSOL"),
        )
    )
    db.add_reactions(
        (
            Reaction(
                id="rxn1_c",
                base_id="rxn1",
                stoichiometries={"ATP_c": -1, "ADP_c": 1},
            ),
        )
    )
    db.cofactor_pairs = {"ATP_c": "ADP_c"}
    db.cofactor_duplication()
    m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1_c")
    assert set(m.compounds.keys()) == {"ATP_c", "ATP_c__cof__", "ADP_c__cof__", "ADP_c"}
    assert set(m.reactions.keys()) == {"rxn1_c", "rxn1_c__cof__"}
    m.remove_cofactor_duplication()
    assert set(m.compounds.keys()) == {"ATP_c", "ADP_c"}
    assert set(m.reactions.keys()) == {"rxn1_c"}


def test_add_from_reference_cof_removal_afterwards_2() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    db = Model(compartments=compartments)
    m = Model(compartments=compartments)
    db.add_compounds(
        (
            Compound(base_id="ATP", compartment="CYTOSOL"),
            Compound(base_id="ADP", compartment="CYTOSOL"),
        )
    )
    db.add_reactions(
        (
            Reaction(
                id="rxn1_c",
                base_id="rxn1",
                stoichiometries={"ATP_c": -1, "ADP_c": 1},
            ),
        )
    )
    db.cofactor_pairs = {"ATP_c": "ADP_c"}
    db.cofactor_duplication()
    m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1_c__cof__")
    assert set(m.compounds.keys()) == {"ATP_c", "ATP_c__cof__", "ADP_c__cof__", "ADP_c"}
    assert set(m.reactions.keys()) == {"rxn1_c", "rxn1_c__cof__"}
    m.remove_cofactor_duplication()
    assert set(m.compounds.keys()) == {"ATP_c", "ADP_c"}
    assert set(m.reactions.keys()) == {"rxn1_c"}


def test_add_from_reference_rev_removal_afterwards() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    db = Model(compartments=compartments)
    m = Model(compartments=compartments)
    db.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
        )
    )
    db.add_reactions(
        (
            Reaction(
                id="rxn1_c",
                base_id="rxn1",
                stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
                reversible=True,
            ),
        )
    )
    db.reversibility_duplication()
    m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1_c")
    assert set(m.compounds.keys()) == {"cpd1_c", "cpd2_c"}
    assert set(m.reactions.keys()) == {"rxn1_c", "rxn1_c__rev__"}
    m.remove_reversibility_duplication()
    assert set(m.compounds.keys()) == {"cpd1_c", "cpd2_c"}
    assert set(m.reactions.keys()) == {"rxn1_c"}


def test_add_from_reference_rev_removal_afterwards_2() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    db = Model(compartments=compartments)
    m = Model(compartments=compartments)
    db.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
        )
    )
    db.add_reactions(
        (
            Reaction(
                id="rxn1_c",
                base_id="rxn1",
                stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
                reversible=True,
            ),
        )
    )
    db.reversibility_duplication()
    m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1_c__rev__")
    assert set(m.compounds.keys()) == {"cpd1_c", "cpd2_c"}
    assert set(m.reactions.keys()) == {"rxn1_c", "rxn1_c__rev__"}
    m.remove_reversibility_duplication()
    assert set(m.compounds.keys()) == {"cpd1_c", "cpd2_c"}
    assert set(m.reactions.keys()) == {"rxn1_c"}


def test_add_from_reference_cof() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    db = Model(compartments=compartments)
    m = Model(compartments=compartments)
    db.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
            Compound(base_id="ATP", compartment="CYTOSOL"),
            Compound(base_id="ADP", compartment="CYTOSOL"),
        )
    )
    db.add_reactions(
        (
            Reaction(
                id="rxn1_c",
                base_id="rxn1",
                stoichiometries={
                    "cpd1_c": -1,
                    "ATP_c": -1,
                    "cpd2_c": 1,
                    "ADP_c": 1,
                },
            ),
        )
    )
    db.cofactor_pairs = {"ATP_c": "ADP_c"}
    db.cofactor_duplication()
    m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1_c")
    assert set(m.compounds.keys()) == {
        "cpd1_c",
        "ATP_c",
        "cpd2_c",
        "ADP_c",
        "ATP_c__cof__",
        "ADP_c__cof__",
    }
    assert set(m.reactions.keys()) == {"rxn1_c", "rxn1_c__cof__"}


def test_add_from_reference_rev() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    db = Model(compartments=compartments)
    m = Model(compartments=compartments)
    db.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
        )
    )
    db.add_reactions(
        (
            Reaction(
                id="rxn1_c",
                base_id="rxn1",
                stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
                reversible=True,
            ),
        )
    )
    db.reversibility_duplication()
    m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1_c")
    assert set(m.compounds.keys()) == {"cpd1_c", "cpd2_c"}
    assert set(m.reactions.keys()) == {"rxn1_c", "rxn1_c__rev__"}


def test_add_from_reference_cof_and_rev() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    db = Model(compartments=compartments)
    m = Model(compartments=compartments)
    db.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
            Compound(base_id="ATP", compartment="CYTOSOL"),
            Compound(base_id="ADP", compartment="CYTOSOL"),
        )
    )
    db.add_reactions(
        (
            Reaction(
                id="rxn1_c",
                base_id="rxn1",
                stoichiometries={
                    "cpd1_c": -1,
                    "ATP_c": -1,
                    "cpd2_c": 1,
                    "ADP_c": 1,
                },
                reversible=True,
            ),
        )
    )
    db.cofactor_pairs = {"ATP_c": "ADP_c"}
    db.cofactor_duplication()
    db.reversibility_duplication()
    m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1_c")
    assert set(m.compounds.keys()) == {
        "cpd1_c",
        "ATP_c",
        "cpd2_c",
        "ADP_c",
        "ATP_c__cof__",
        "ADP_c__cof__",
    }
    assert set(m.reactions.keys()) == {"rxn1_c", "rxn1_c__rev__", "rxn1_c__cof____rev__", "rxn1_c__cof__"}


def test_add_from_reference_var_base_id() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    db = Model(compartments=compartments)
    m = Model(compartments=compartments)
    db.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
            Compound(base_id="ATP", compartment="CYTOSOL"),
            Compound(base_id="ADP", compartment="CYTOSOL"),
        )
    )
    db.add_reactions(
        (
            Reaction(
                id="rxn1__var__0_c",
                base_id="rxn1",
                stoichiometries={
                    "cpd1_c": -1,
                    "ATP_c": -1,
                    "cpd2_c": 1,
                    "ADP_c": 1,
                },
                reversible=True,
            ),
            Reaction(
                id="rxn1__var__1_c",
                base_id="rxn1",
                stoichiometries={
                    "cpd1_c": -1,
                    "ATP_c": -1,
                    "cpd2_c": 1,
                    "ADP_c": 1,
                },
                reversible=True,
            ),
        )
    )
    m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1")
    assert set(m.compounds.keys()) == {"cpd1_c", "ATP_c", "cpd2_c", "ADP_c"}
    assert set(m.reactions.keys()) == {"rxn1__var__0_c", "rxn1__var__1_c"}

    def test_add_from_reference_var_id() -> None:
        compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
        db = Model(compartments=compartments)
        m = Model(compartments=compartments)
        db.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL"),
                Compound(base_id="cpd2", compartment="CYTOSOL"),
                Compound(base_id="ATP", compartment="CYTOSOL"),
                Compound(base_id="ADP", compartment="CYTOSOL"),
            )
        )
        db.add_reactions(
            (
                Reaction(
                    id="rxn1__var__0_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
                Reaction(
                    id="rxn1__var__1_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
            )
        )
        m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1__var__0_c")
        assert set(m.compounds.keys()) == {"cpd1_c", "ATP_c", "cpd2_c", "ADP_c"}
        assert set(m.reactions.keys()) == {"rxn1__var__0_c", "rxn1__var__1_c"}

    def test_add_from_reference_var_cof_rev_base_id() -> None:
        compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
        db = Model(compartments=compartments)
        m = Model(compartments=compartments)
        db.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL"),
                Compound(base_id="cpd2", compartment="CYTOSOL"),
                Compound(base_id="ATP", compartment="CYTOSOL"),
                Compound(base_id="ADP", compartment="CYTOSOL"),
            )
        )
        db.add_reactions(
            (
                Reaction(
                    id="rxn1__var__0_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
                Reaction(
                    id="rxn1__var__1_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
            )
        )
        db.cofactor_pairs = {"ATP_c": "ADP_c"}
        db.cofactor_duplication()
        db.reversibility_duplication()
        m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1")
        assert set(m.compounds.keys()) == {
            "ATP_c__cof__",
            "ADP_c__cof__",
            "ADP_c",
            "cpd2_c",
            "ATP_c",
            "cpd1_c",
        }
        assert set(m.reactions.keys()) == {
            "rxn1__var__0_c",
            "rxn1__var__0_c__cof__",
            "rxn1__var__0_c__rev__",
            "rxn1__var__0_c__cof____rev__",
            "rxn1__var__1_c",
            "rxn1__var__1_c__cof__",
            "rxn1__var__1_c__rev__",
            "rxn1__var__1_c__cof____rev__",
        }

    def test_add_from_reference_var_cof_rev_id() -> None:
        compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
        db = Model(compartments=compartments)
        m = Model(compartments=compartments)
        db.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL"),
                Compound(base_id="cpd2", compartment="CYTOSOL"),
                Compound(base_id="ATP", compartment="CYTOSOL"),
                Compound(base_id="ADP", compartment="CYTOSOL"),
            )
        )
        db.add_reactions(
            (
                Reaction(
                    id="rxn1__var__0_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
                Reaction(
                    id="rxn1__var__1_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
            )
        )
        db.cofactor_pairs = {"ATP_c": "ADP_c"}
        db.cofactor_duplication()
        db.reversibility_duplication()
        m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1__var__0_c")
        assert set(m.compounds.keys()) == {
            "ATP_c__cof__",
            "ADP_c__cof__",
            "ADP_c",
            "cpd2_c",
            "ATP_c",
            "cpd1_c",
        }
        assert set(m.reactions.keys()) == {
            "rxn1__var__0_c",
            "rxn1__var__0_c__cof__",
            "rxn1__var__0_c__rev__",
            "rxn1__var__0_c__cof____rev__",
            "rxn1__var__1_c",
            "rxn1__var__1_c__cof__",
            "rxn1__var__1_c__rev__",
            "rxn1__var__1_c__cof____rev__",
        }

    def test_replace_from_reference() -> None:
        compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
        db = Model(compartments=compartments)
        m = Model(compartments=compartments)
        db.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL"),
                Compound(base_id="cpd2", compartment="CYTOSOL"),
            )
        )
        db.add_reactions(
            (
                Reaction(
                    id="rxn1_c",
                    base_id="rxn1",
                    stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
                ),
            )
        )
        m.add_compounds(
            (
                Compound(base_id="cpd1_old", compartment="CYTOSOL"),
                Compound(base_id="cpd2_old", compartment="CYTOSOL"),
            )
        )
        m.add_reactions(
            (
                Reaction(
                    id="rxn1_c",
                    base_id="rxn1",
                    stoichiometries={"cpd1_old_c": -1, "cpd2_old_c": 1},
                ),
            )
        )
        m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1_c")
        assert set(m.compounds.keys()) == {"cpd1_c", "cpd2_c"}
        assert set(m.reactions.keys()) == {"rxn1_c"}

    def test_replace_from_reference_cof() -> None:
        compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
        db = Model(compartments=compartments)
        m = Model(compartments=compartments)
        db.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL"),
                Compound(base_id="cpd2", compartment="CYTOSOL"),
                Compound(base_id="ATP", compartment="CYTOSOL"),
                Compound(base_id="ADP", compartment="CYTOSOL"),
            )
        )
        db.add_reactions(
            (
                Reaction(
                    id="rxn1_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                ),
            )
        )
        m.add_compounds(
            (
                Compound(base_id="cpd1_old", compartment="CYTOSOL"),
                Compound(base_id="cpd2_old", compartment="CYTOSOL"),
                Compound(base_id="ATP", compartment="CYTOSOL"),
                Compound(base_id="ADP", compartment="CYTOSOL"),
            )
        )
        m.add_reactions(
            (
                Reaction(
                    id="rxn1_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_old_c": -1,
                        "ATP_c": -1,
                        "cpd2_old_c": 1,
                        "ADP_c": 1,
                    },
                ),
            )
        )
        db.cofactor_pairs = {"ATP_c": "ADP_c"}
        db.cofactor_duplication()
        m.cofactor_pairs = {"ATP_c": "ADP_c"}
        m.cofactor_duplication()
        m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1")
        assert set(m.compounds.keys()) == {
            "cpd1_c",
            "cpd2_c",
            "ATP_c",
            "ADP_c",
            "ATP_c__cof__",
            "ADP_c__cof__",
        }
        assert set(m.reactions.keys()) == {"rxn1_c", "rxn1_c__cof__"}

    def test_replace_from_reference_rev() -> None:
        compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
        db = Model(compartments=compartments)
        m = Model(compartments=compartments)
        db.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL"),
                Compound(base_id="cpd2", compartment="CYTOSOL"),
            )
        )
        db.add_reactions(
            (
                Reaction(
                    id="rxn1_c",
                    base_id="rxn1",
                    stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
                    reversible=True,
                ),
            )
        )
        m.add_compounds(
            (
                Compound(base_id="cpd1_old", compartment="CYTOSOL"),
                Compound(base_id="cpd2_old", compartment="CYTOSOL"),
            )
        )
        m.add_reactions(
            (
                Reaction(
                    id="rxn1_c",
                    base_id="rxn1",
                    stoichiometries={"cpd1_old_c": -1, "cpd2_old_c": 1},
                    reversible=True,
                ),
            )
        )
        db.reversibility_duplication()
        m.reversibility_duplication()
        m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1")
        assert set(m.compounds.keys()) == {"cpd1_c", "cpd2_c"}
        assert set(m.reactions.keys()) == {"rxn1_c", "rxn1_c__rev__"}

    def test_replace_from_reference_cof_and_rev() -> None:
        compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
        db = Model(compartments=compartments)
        m = Model(compartments=compartments)
        db.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL"),
                Compound(base_id="cpd2", compartment="CYTOSOL"),
                Compound(base_id="ATP", compartment="CYTOSOL"),
                Compound(base_id="ADP", compartment="CYTOSOL"),
            )
        )
        db.add_reactions(
            (
                Reaction(
                    id="rxn1_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
            )
        )
        m.add_compounds(
            (
                Compound(base_id="cpd1_old", compartment="CYTOSOL"),
                Compound(base_id="cpd2_old", compartment="CYTOSOL"),
                Compound(base_id="ATP", compartment="CYTOSOL"),
                Compound(base_id="ADP", compartment="CYTOSOL"),
            )
        )
        m.add_reactions(
            (
                Reaction(
                    id="rxn1_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_old_c": -1,
                        "ATP_c": -1,
                        "cpd2_old_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
            )
        )
        db.cofactor_pairs = {"ATP_c": "ADP_c"}
        db.cofactor_duplication()
        db.reversibility_duplication()
        m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1")
        assert set(m.compounds.keys()) == {
            "cpd1_c",
            "ATP_c",
            "cpd2_c",
            "ADP_c",
            "ATP_c__cof__",
            "ADP_c__cof__",
        }
        assert set(m.reactions.keys()) == {"rxn1_c", "rxn1_c__rev__", "rxn1_c__cof____rev__", "rxn1_c__cof__"}

    def test_replace_from_reference_var_base_id() -> None:
        compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
        db = Model(compartments=compartments)
        m = Model(compartments=compartments)
        db.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL"),
                Compound(base_id="cpd2", compartment="CYTOSOL"),
                Compound(base_id="ATP", compartment="CYTOSOL"),
                Compound(base_id="ADP", compartment="CYTOSOL"),
            )
        )
        db.add_reactions(
            (
                Reaction(
                    id="rxn1__var__0_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
                Reaction(
                    id="rxn1__var__1_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
            )
        )
        m.add_compounds(
            (
                Compound(base_id="cpd1_old", compartment="CYTOSOL"),
                Compound(base_id="cpd2_old", compartment="CYTOSOL"),
                Compound(base_id="ATP", compartment="CYTOSOL"),
                Compound(base_id="ADP", compartment="CYTOSOL"),
            )
        )
        m.add_reactions(
            (
                Reaction(
                    id="rxn1__var__0_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_old_c": -1,
                        "ATP_c": -1,
                        "cpd2_old_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
                Reaction(
                    id="rxn1__var__1_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_old_c": -1,
                        "ATP_c": -1,
                        "cpd2_old_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
            )
        )
        m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1")
        assert set(m.compounds.keys()) == {"cpd1_c", "ATP_c", "cpd2_c", "ADP_c"}
        assert set(m.reactions.keys()) == {"rxn1__var__0_c", "rxn1__var__1_c"}

    def test_replace_from_reference_var_id() -> None:
        compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
        db = Model(compartments=compartments)
        m = Model(compartments=compartments)
        db.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL"),
                Compound(base_id="cpd2", compartment="CYTOSOL"),
                Compound(base_id="ATP", compartment="CYTOSOL"),
                Compound(base_id="ADP", compartment="CYTOSOL"),
            )
        )
        db.add_reactions(
            (
                Reaction(
                    id="rxn1__var__0_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
                Reaction(
                    id="rxn1__var__1_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
            )
        )
        m.add_compounds(
            (
                Compound(base_id="cpd1_old", compartment="CYTOSOL"),
                Compound(base_id="cpd2_old", compartment="CYTOSOL"),
                Compound(base_id="ATP", compartment="CYTOSOL"),
                Compound(base_id="ADP", compartment="CYTOSOL"),
            )
        )
        m.add_reactions(
            (
                Reaction(
                    id="rxn1__var__0_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_old_c": -1,
                        "ATP_c": -1,
                        "cpd2_old_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
            )
        )
        m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1__var__0_c")
        assert set(m.compounds.keys()) == {"cpd1_c", "ATP_c", "cpd2_c", "ADP_c"}
        assert set(m.reactions.keys()) == {"rxn1__var__0_c", "rxn1__var__1_c"}

    def test_replace_from_reference_var_cof_rev_base_id() -> None:
        compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
        db = Model(compartments=compartments)
        m = Model(compartments=compartments)
        db.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL"),
                Compound(base_id="cpd2", compartment="CYTOSOL"),
                Compound(base_id="ATP", compartment="CYTOSOL"),
                Compound(base_id="ADP", compartment="CYTOSOL"),
            )
        )
        db.add_reactions(
            (
                Reaction(
                    id="rxn1__var__0_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
                Reaction(
                    id="rxn1__var__1_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
            )
        )
        m.add_compounds(
            (
                Compound(base_id="cpd1_old", compartment="CYTOSOL"),
                Compound(base_id="cpd2_old", compartment="CYTOSOL"),
                Compound(base_id="ATP", compartment="CYTOSOL"),
                Compound(base_id="ADP", compartment="CYTOSOL"),
            )
        )
        m.add_reactions(
            (
                Reaction(
                    id="rxn1__var__0_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_old_c": -1,
                        "ATP_c": -1,
                        "cpd2_old_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
            )
        )
        db.cofactor_pairs = {"ATP_c": "ADP_c"}
        db.cofactor_duplication()
        db.reversibility_duplication()
        m.cofactor_pairs = {"ATP_c": "ADP_c"}
        m.cofactor_duplication()
        m.reversibility_duplication()
        m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1")
        assert set(m.compounds.keys()) == {
            "ATP_c__cof__",
            "ADP_c__cof__",
            "ADP_c",
            "cpd2_c",
            "ATP_c",
            "cpd1_c",
        }
        assert set(m.reactions.keys()) == {
            "rxn1__var__0_c",
            "rxn1__var__0_c__cof__",
            "rxn1__var__0_c__rev__",
            "rxn1__var__0_c__cof____rev__",
            "rxn1__var__1_c",
            "rxn1__var__1_c__cof__",
            "rxn1__var__1_c__rev__",
            "rxn1__var__1_c__cof____rev__",
        }

    def test_replace_from_reference_var_cof_rev_id() -> None:
        compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
        db = Model(compartments=compartments)
        m = Model(compartments=compartments)
        db.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL"),
                Compound(base_id="cpd2", compartment="CYTOSOL"),
                Compound(base_id="ATP", compartment="CYTOSOL"),
                Compound(base_id="ADP", compartment="CYTOSOL"),
            )
        )
        db.add_reactions(
            (
                Reaction(
                    id="rxn1__var__0_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
                Reaction(
                    id="rxn1__var__1_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
            )
        )
        m.add_compounds(
            (
                Compound(base_id="cpd1_old", compartment="CYTOSOL"),
                Compound(base_id="cpd2_old", compartment="CYTOSOL"),
                Compound(base_id="ATP", compartment="CYTOSOL"),
                Compound(base_id="ADP", compartment="CYTOSOL"),
            )
        )
        m.add_reactions(
            (
                Reaction(
                    id="rxn1__var__0_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_old_c": -1,
                        "ATP_c": -1,
                        "cpd2_old_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
            )
        )
        db.cofactor_pairs = {"ATP_c": "ADP_c"}
        db.cofactor_duplication()
        db.reversibility_duplication()
        m.cofactor_pairs = {"ATP_c": "ADP_c"}
        m.cofactor_duplication()
        m.reversibility_duplication()
        m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1__var__0_c")
        assert set(m.compounds.keys()) == {
            "ATP_c__cof__",
            "ADP_c__cof__",
            "ADP_c",
            "cpd2_c",
            "ATP_c",
            "cpd1_c",
        }
        assert set(m.reactions.keys()) == {
            "rxn1__var__0_c",
            "rxn1__var__0_c__rev__",
            "rxn1__var__0_c__cof__",
            "rxn1__var__0_c__cof____rev__",
            "rxn1__var__1_c",
            "rxn1__var__1_c__rev__",
            "rxn1__var__1_c__cof__",
            "rxn1__var__1_c__cof____rev__",
        }

    def test_add_from_reference_rev_input() -> None:
        compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
        db = Model(compartments=compartments)
        m = Model(compartments=compartments)
        db.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL"),
                Compound(base_id="cpd2", compartment="CYTOSOL"),
                Compound(base_id="ATP", compartment="CYTOSOL"),
                Compound(base_id="ADP", compartment="CYTOSOL"),
            )
        )
        db.add_reactions(
            (
                Reaction(
                    id="rxn1__var__0_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
            )
        )
        db.cofactor_pairs = {"ATP_c": "ADP_c"}
        db.cofactor_duplication()
        db.reversibility_duplication()
        m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1__var__0_c__rev__")
        assert set(m.compounds.keys()) == {
            "cpd1_c",
            "ATP_c",
            "cpd2_c",
            "ADP_c",
            "ATP_c__cof__",
            "ADP_c__cof__",
        }
        assert set(m.reactions.keys()) == {
            "rxn1__var__0_c",
            "rxn1__var__0_c__rev__",
            "rxn1__var__0_c__cof__",
            "rxn1__var__0_c__cof____rev__",
        }

    def test_add_from_reference_cof_input() -> None:
        compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
        db = Model(compartments=compartments)
        m = Model(compartments=compartments)
        db.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL"),
                Compound(base_id="cpd2", compartment="CYTOSOL"),
                Compound(base_id="ATP", compartment="CYTOSOL"),
                Compound(base_id="ADP", compartment="CYTOSOL"),
            )
        )
        db.add_reactions(
            (
                Reaction(
                    id="rxn1__var__0_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
            )
        )
        db.cofactor_pairs = {"ATP_c": "ADP_c"}
        db.cofactor_duplication()
        db.reversibility_duplication()
        m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1__var__0_c__cof__")
        assert set(m.compounds.keys()) == {
            "cpd1_c",
            "ATP_c",
            "cpd2_c",
            "ADP_c",
            "ATP_c__cof__",
            "ADP_c__cof__",
        }
        assert set(m.reactions.keys()) == {
            "rxn1__var__0_c",
            "rxn1__var__0_c__rev__",
            "rxn1__var__0_c__cof__",
            "rxn1__var__0_c__cof____rev__",
        }

    def test_replace_from_reference_rev_input() -> None:
        compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
        db = Model(compartments=compartments)
        m = Model(compartments=compartments)
        db.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL"),
                Compound(base_id="cpd2", compartment="CYTOSOL"),
                Compound(base_id="ATP", compartment="CYTOSOL"),
                Compound(base_id="ADP", compartment="CYTOSOL"),
            )
        )
        db.add_reactions(
            (
                Reaction(
                    id="rxn1__var__0_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
            )
        )
        m.add_compounds(
            (
                Compound(base_id="cpd1_old", compartment="CYTOSOL"),
                Compound(base_id="cpd2_old", compartment="CYTOSOL"),
                Compound(base_id="ATP", compartment="CYTOSOL"),
                Compound(base_id="ADP", compartment="CYTOSOL"),
            )
        )
        m.add_reactions(
            (
                Reaction(
                    id="rxn1__var__0_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_old_c": -1,
                        "ATP_c": -1,
                        "cpd2_old_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
            )
        )
        db.cofactor_pairs = {"ATP_c": "ADP_c"}
        db.cofactor_duplication()
        db.reversibility_duplication()
        m.cofactor_pairs = {"ATP_c": "ADP_c"}
        m.cofactor_duplication()
        m.reversibility_duplication()
        m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1__var__0_c__rev__")
        assert set(m.compounds.keys()) == {
            "cpd1_c",
            "ATP_c",
            "cpd2_c",
            "ADP_c",
            "ATP_c__cof__",
            "ADP_c__cof__",
        }
        assert set(m.reactions.keys()) == {
            "rxn1__var__0_c",
            "rxn1__var__0_c__rev__",
            "rxn1__var__0_c__cof__",
            "rxn1__var__0_c__cof____rev__",
        }

    def test_replace_from_reference_cof_input() -> None:
        compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
        db = Model(compartments=compartments)
        m = Model(compartments=compartments)
        db.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL"),
                Compound(base_id="cpd2", compartment="CYTOSOL"),
                Compound(base_id="ATP", compartment="CYTOSOL"),
                Compound(base_id="ADP", compartment="CYTOSOL"),
            )
        )
        db.add_reactions(
            (
                Reaction(
                    id="rxn1__var__0_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
            )
        )
        m.add_compounds(
            (
                Compound(base_id="cpd1_old", compartment="CYTOSOL"),
                Compound(base_id="cpd2_old", compartment="CYTOSOL"),
                Compound(base_id="ATP", compartment="CYTOSOL"),
                Compound(base_id="ADP", compartment="CYTOSOL"),
            )
        )
        m.add_reactions(
            (
                Reaction(
                    id="rxn1__var__0_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_old_c": -1,
                        "ATP_c": -1,
                        "cpd2_old_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
            )
        )
        db.cofactor_pairs = {"ATP_c": "ADP_c"}
        db.cofactor_duplication()
        db.reversibility_duplication()
        m.cofactor_pairs = {"ATP_c": "ADP_c"}
        m.cofactor_duplication()
        m.reversibility_duplication()
        m.add_reaction_from_reference(reference_model=db, reaction_id="rxn1__var__0_c__cof__")
        assert set(m.compounds.keys()) == {
            "cpd1_c",
            "ATP_c",
            "cpd2_c",
            "ADP_c",
            "ATP_c__cof__",
            "ADP_c__cof__",
        }
        assert set(m.reactions.keys()) == {
            "rxn1__var__0_c",
            "rxn1__var__0_c__rev__",
            "rxn1__var__0_c__cof__",
            "rxn1__var__0_c__cof____rev__",
        }

    def test_update_from_reference_var() -> None:
        compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
        db = Model(compartments=compartments)
        m = Model(compartments=compartments)
        db.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL"),
                Compound(base_id="cpd2", compartment="CYTOSOL"),
            )
        )
        db.add_reactions(
            (
                Reaction(
                    id="rxn1__var__0_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
                Reaction(
                    id="rxn1__var__1_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_c": -1,
                        "ATP_c": -1,
                        "cpd2_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
            )
        )
        m.add_compounds(
            (
                Compound(base_id="cpd1_old", compartment="CYTOSOL"),
                Compound(base_id="cpd2_old", compartment="CYTOSOL"),
            )
        )
        m.add_reactions(
            (
                Reaction(
                    id="rxn1__var__0_c",
                    base_id="rxn1",
                    stoichiometries={
                        "cpd1_old_c": -1,
                        "ATP_c": -1,
                        "cpd2_old_c": 1,
                        "ADP_c": 1,
                    },
                    reversible=True,
                ),
            )
        )
        m.update_from_reference(reference_model=db)
        assert set(m.compounds.keys()) == {"cpd1_c", "ATP_c", "cpd2_c", "ADP_c"}
        assert set(m.reactions.keys()) == {"rxn1__var__0_c", "rxn1__var__1_c"}

    def test_update_model_remove_unbalanced() -> None:
        compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
        db = Model(compartments=compartments)
        m = Model(compartments=compartments)
        db.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL", charge=1),
                Compound(base_id="cpd2", compartment="CYTOSOL", charge=1),
            )
        )
        db.add_reactions(
            (
                Reaction(
                    id="rxn1_c",
                    base_id="rxn1",
                    stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
                ),
            )
        )
        m.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL", charge=2),
                Compound(base_id="cpd2", compartment="CYTOSOL", charge=1),
            )
        )
        m.add_reactions(
            (
                Reaction(
                    id="rxn2",
                    base_id="rxn2",
                    stoichiometries={"cpd1_c": -1, "cpd2_c": 2},
                ),
            )
        )
        m.update_from_reference(db)
        assert m.reactions == {}

    def test_update_model_remove_unmapped_unbalanced() -> None:
        """Remove reactions that are unbalanced after the update of a compound"""
        compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
        db = Model(compartments=compartments)
        m = Model(compartments=compartments)
        db.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL", charge=1),
                Compound(base_id="cpd2", compartment="CYTOSOL", charge=1),
            )
        )
        db.add_reactions(
            (
                Reaction(
                    id="rxn1",
                    base_id="rxn1",
                    stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
                ),
            )
        )
        m.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL", charge=2),
                Compound(base_id="cpd2", compartment="CYTOSOL", charge=1),
            )
        )
        m.add_reactions(
            (
                Reaction(
                    id="rxn1",
                    base_id="rxn1",
                    stoichiometries={"cpd1_c": -1, "cpd2_c": 2},
                ),
                Reaction(
                    id="rxn2",
                    base_id="rxn2",
                    stoichiometries={"cpd1_c": -1, "cpd2_c": 2},
                ),
            )
        )
        m.update_from_reference(db)
        assert set(m.reactions) == {"rxn1"}

    def test_update_model_remove_unmapped_unbalanced_mass_verbose() -> None:
        """Remove reactions that are unbalanced after the update of a compound"""
        compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
        db = Model(compartments=compartments)
        m = Model(compartments=compartments)
        db.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL", charge=2, formula={"C": 1}),
                Compound(base_id="cpd2", compartment="CYTOSOL", charge=1, formula={"C": 1}),
            )
        )
        db.add_reactions(
            (
                Reaction(
                    id="rxn1",
                    base_id="rxn1",
                    stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
                ),
            )
        )
        m.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL", charge=2, formula={"C": 2}),
                Compound(base_id="cpd2", compartment="CYTOSOL", charge=1, formula={"C": 1}),
            )
        )
        m.add_reactions(
            (
                Reaction(
                    id="rxn1",
                    base_id="rxn1",
                    stoichiometries={"cpd1_c": -1, "cpd2_c": 2},
                ),
                Reaction(
                    id="rxn2",
                    base_id="rxn2",
                    stoichiometries={"cpd1_c": -1, "cpd2_c": 2},
                ),
            )
        )
        m.update_from_reference(reference_model=db, verbose=True)
        assert set(m.reactions) == {"rxn1"}

    def test_update_model_remove_unmapped_unbalanced_charge_verbose() -> None:
        """Remove reactions that are unbalanced after the update of a compound"""
        compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
        db = Model(compartments=compartments)
        m = Model(compartments=compartments)
        db.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL", charge=1, formula={"C": 2}),
                Compound(base_id="cpd2", compartment="CYTOSOL", charge=1, formula={"C": 1}),
            )
        )
        db.add_reactions(
            (
                Reaction(
                    id="rxn1",
                    base_id="rxn1",
                    stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
                ),
            )
        )
        m.add_compounds(
            (
                Compound(base_id="cpd1", compartment="CYTOSOL", charge=2, formula={"C": 2}),
                Compound(base_id="cpd2", compartment="CYTOSOL", charge=1, formula={"C": 1}),
            )
        )
        m.add_reactions(
            (
                Reaction(
                    id="rxn1",
                    base_id="rxn1",
                    stoichiometries={"cpd1_c": -1, "cpd2_c": 2},
                ),
                Reaction(
                    id="rxn2",
                    base_id="rxn2",
                    stoichiometries={"cpd1_c": -1, "cpd2_c": 2},
                ),
            )
        )
        m.update_from_reference(reference_model=db, verbose=True)
        assert set(m.reactions) == {"rxn1"}
