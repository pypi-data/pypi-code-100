from moped import Compound, Model, Reaction


def test_reversibility_duplication() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
        )
    )
    m.add_reactions(
        (
            Reaction(id="v_default", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
            Reaction(
                id="v_irrev",
                stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
                reversible=False,
            ),
            Reaction(
                id="v_rev",
                stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
                reversible=True,
            ),
        )
    )
    m.reversibility_duplication()
    assert tuple(m.reactions.keys()) == ("v_default", "v_irrev", "v_rev", "v_rev__rev__")
    assert m.reactions["v_rev"].stoichiometries == {"cpd1_c": -1, "cpd2_c": 1}
    assert m.reactions["v_rev__rev__"].stoichiometries == {"cpd1_c": 1, "cpd2_c": -1}


def test_remove_reversibility_duplication() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
        )
    )
    m.add_reactions(
        (
            Reaction(id="v_default", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
            Reaction(
                id="v_irrev",
                stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
                reversible=False,
            ),
            Reaction(
                id="v_rev",
                stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
                reversible=True,
            ),
        )
    )
    m.reversibility_duplication()
    m.remove_reversibility_duplication()
    assert tuple(m.reactions.keys()) == ("v_default", "v_irrev", "v_rev")
    assert m.reactions["v_rev"].stoichiometries == {"cpd1_c": -1, "cpd2_c": 1}


def test_cofactor_duplication() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
            Compound(base_id="ATP", compartment="CYTOSOL"),
            Compound(base_id="ADP", compartment="CYTOSOL"),
        )
    )
    m.add_reactions(
        (
            Reaction(
                id="v0",
                stoichiometries={
                    "cpd1_c": -1,
                    "ATP_c": -1,
                    "cpd2_c": 1,
                    "ADP_c": 1,
                },
            ),
            Reaction(id="v1", stoichiometries={"cpd1_c": -1, "ATP_c": -1, "cpd2_c": 1}),
            Reaction(id="v2", stoichiometries={"cpd1_c": -1, "cpd2_c": 1, "ADP_c": 1}),
        )
    )
    m.cofactor_pairs = {"ATP_c": "ADP_c"}
    m.cofactor_duplication()
    assert tuple(m.compounds) == (
        "cpd1_c",
        "cpd2_c",
        "ATP_c",
        "ADP_c",
        "ATP_c__cof__",
        "ADP_c__cof__",
    )
    assert tuple(m.reactions) == ("v0", "v1", "v2", "v0__cof__")
    assert m.reactions["v0"].stoichiometries == {"cpd1_c": -1, "cpd2_c": 1, "ATP_c": -1, "ADP_c": 1}
    assert m.reactions["v1"].stoichiometries == {"cpd1_c": -1, "ATP_c": -1, "cpd2_c": 1}
    assert m.reactions["v2"].stoichiometries == {"cpd1_c": -1, "cpd2_c": 1, "ADP_c": 1}
    assert m.reactions["v0__cof__"].stoichiometries == {
        "cpd1_c": -1,
        "cpd2_c": 1,
        "ATP_c__cof__": -1,
        "ADP_c__cof__": 1,
    }


def test_remove_cofactor_duplication() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
            Compound(base_id="ATP", compartment="CYTOSOL"),
            Compound(base_id="ADP", compartment="CYTOSOL"),
        )
    )
    m.add_reactions(
        (
            Reaction(
                id="v0",
                stoichiometries={
                    "cpd1_c": -1,
                    "ATP_c": -1,
                    "cpd2_c": 1,
                    "ADP_c": 1,
                },
            ),
            Reaction(id="v1", stoichiometries={"cpd1_c": -1, "ATP_c": -1, "cpd2_c": 1}),
            Reaction(id="v2", stoichiometries={"cpd1_c": -1, "cpd2_c": 1, "ADP_c": 1}),
        )
    )
    m.cofactor_duplication()
    m.remove_cofactor_duplication()
    assert tuple(m.compounds) == ("cpd1_c", "cpd2_c", "ATP_c", "ADP_c")
    assert tuple(m.reactions) == ("v0", "v1", "v2")
    assert m.reactions["v0"].stoichiometries == {"cpd1_c": -1, "cpd2_c": 1, "ATP_c": -1, "ADP_c": 1}
    assert m.reactions["v1"].stoichiometries == {"cpd1_c": -1, "ATP_c": -1, "cpd2_c": 1}
    assert m.reactions["v2"].stoichiometries == {"cpd1_c": -1, "cpd2_c": 1, "ADP_c": 1}
