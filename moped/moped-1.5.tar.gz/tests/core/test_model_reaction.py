from moped import Compound, Model, Reaction

import pytest


def test_add_reaction() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
        )
    )
    m.add_reaction(Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}))
    assert tuple(m.reactions.keys()) == ("v1",)
    assert m.compounds["cpd1_c"].in_reaction == {"v1"}
    assert m.compounds["cpd2_c"].in_reaction == {"v1"}


def test_add_reaction_var() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
        )
    )
    m.add_reaction(
        Reaction(
            id="v1__var__0_c",
            base_id="v1",
            stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
            _var=0,
        )
    )
    assert set(m.reactions.keys()) == {"v1__var__0_c"}
    assert m.variant_reactions["v1"] == {"v1__var__0_c"}
    assert m.compounds["cpd1_c"].in_reaction == {"v1__var__0_c"}
    assert m.compounds["cpd2_c"].in_reaction == {"v1__var__0_c"}


def test_add_reaction_fail_on_wrong_type() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
        )
    )
    with pytest.raises(TypeError):
        m.add_reaction("v1")  # type: ignore


def test_set_reaction_property() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
        )
    )
    m.add_reaction(Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}))
    m.set_reaction_property(
        "v1",
        {
            "id": "v1",
            "name": "v1",
            "stoichiometries": {"cpd1_c": 1, "cpd2_c": -1},
            "bounds": (-1000, 1000),
            "reversible": True,
            "gibbs0": 5,
            "ec": "5.4.123.2",
            "pathways": ["pwy-101"],
        },
    )
    assert m.reactions["v1"].id == "v1"
    assert m.reactions["v1"].name == "v1"
    assert m.reactions["v1"].stoichiometries == {"cpd1_c": 1, "cpd2_c": -1}
    assert m.reactions["v1"].bounds == (-1000, 1000)
    assert m.reactions["v1"].reversible is True
    assert m.reactions["v1"].gibbs0 == 5
    assert m.reactions["v1"].ec == "5.4.123.2"
    assert m.reactions["v1"].pathways == ["pwy-101"]


def test_set_reaction_property_wrong_key() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
        )
    )
    m.add_reaction(Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}))
    with pytest.raises(KeyError):
        m.set_reaction_property("v1", {"bogus-key": "bogus-value"})


def test_remove_reaction() -> None:
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
            Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
            Reaction(id="v2", stoichiometries={"cpd1_c": 1, "cpd2_c": -1}),
        )
    )
    m.remove_reaction("v1")
    assert tuple(m.reactions.keys()) == ("v2",)


def test_remove_reaction_var() -> None:
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
            Reaction(
                id="rxn1__var__0_c",
                base_id="rxn1",
                stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
                pathways={"PWY101"},
                _var=0,
            ),
            Reaction(
                id="rxn1__var__1_c",
                base_id="rxn1",
                stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
                pathways={"PWY101"},
                _var=1,
            ),
        )
    )
    assert m.pathways["PWY101"] == {"rxn1__var__1_c", "rxn1__var__0_c"}
    assert m.variant_reactions["rxn1"] == {"rxn1__var__1_c", "rxn1__var__0_c"}
    assert m.compounds["cpd1_c"].in_reaction == {"rxn1__var__1_c", "rxn1__var__0_c"}
    assert m.compounds["cpd2_c"].in_reaction == {"rxn1__var__1_c", "rxn1__var__0_c"}

    m.remove_reaction("rxn1__var__0_c")
    assert m.pathways["PWY101"] == {"rxn1__var__1_c"}
    assert m.variant_reactions["rxn1"] == {"rxn1__var__1_c"}
    assert m.compounds["cpd1_c"].in_reaction == {"rxn1__var__1_c"}
    assert m.compounds["cpd2_c"].in_reaction == {"rxn1__var__1_c"}

    m.remove_reaction("rxn1__var__1_c")
    with pytest.raises(KeyError):
        m.pathways["PWY101"]
    with pytest.raises(KeyError):
        m.variant_reactions["rxn1"]
    with pytest.raises(KeyError):
        m.compounds["cpd1_c"]
    with pytest.raises(KeyError):
        m.compounds["cpd2_c"]


def test_remove_reaction_compound_in_reaction() -> None:
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
            Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
            Reaction(id="v2", stoichiometries={"cpd1_c": 1, "cpd2_c": -1}),
        )
    )
    m.remove_reaction("v1")
    assert m.compounds["cpd1_c"].in_reaction == set(["v2"])
    assert m.compounds["cpd2_c"].in_reaction == set(["v2"])


def test_remove_reaction_types() -> None:
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
            Reaction(
                id="v1",
                stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
                types=["type1"],
            ),
            Reaction(
                id="v2",
                stoichiometries={"cpd1_c": 1, "cpd2_c": -1},
                types=["type1"],
            ),
        )
    )
    m.remove_reaction("v1")
    assert m._reaction_types["type1"] == {"v2"}
    m.remove_reaction("v2")
    assert not bool(m._reaction_types)


def test_remove_reactions_tuple() -> None:
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
            Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
            Reaction(id="v2", stoichiometries={"cpd1_c": 1, "cpd2_c": -1}),
            Reaction(id="v3", stoichiometries={"cpd1_c": 1, "cpd2_c": -1}),
        )
    )
    m.remove_reactions(("v1", "v3"))
    assert m.compounds["cpd1_c"].in_reaction == set(["v2"])
    assert m.compounds["cpd2_c"].in_reaction == set(["v2"])


def test_remove_reactions_list() -> None:
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
            Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
            Reaction(id="v2", stoichiometries={"cpd1_c": 1, "cpd2_c": -1}),
            Reaction(id="v3", stoichiometries={"cpd1_c": 1, "cpd2_c": -1}),
        )
    )
    m.remove_reactions(["v1", "v3"])
    assert m.compounds["cpd1_c"].in_reaction == set(["v2"])
    assert m.compounds["cpd2_c"].in_reaction == set(["v2"])


def test_remove_reactions_set() -> None:
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
            Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
            Reaction(id="v2", stoichiometries={"cpd1_c": 1, "cpd2_c": -1}),
            Reaction(id="v3", stoichiometries={"cpd1_c": 1, "cpd2_c": -1}),
        )
    )
    m.remove_reactions({"v1", "v3"})
    assert m.compounds["cpd1_c"].in_reaction == set(["v2"])
    assert m.compounds["cpd2_c"].in_reaction == set(["v2"])


def test_remove_reactions_dict() -> None:
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
            Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
            Reaction(id="v2", stoichiometries={"cpd1_c": 1, "cpd2_c": -1}),
            Reaction(id="v3", stoichiometries={"cpd1_c": 1, "cpd2_c": -1}),
        )
    )
    m.remove_reactions({"v1": 1, "v3": 1})
    assert m.compounds["cpd1_c"].in_reaction == set(["v2"])
    assert m.compounds["cpd2_c"].in_reaction == set(["v2"])


def test_reaction_getters() -> None:
    m = Model()
    m.add_compartment(compartment_id="c", compartment_suffix="c")
    m.add_compound(Compound(base_id="cpd1", compartment="c"))
    m.add_compound(Compound(base_id="cpd2", compartment="c"))

    reaction = Reaction(
        id="rxn1",
        base_id="rxn1",
        name="Reaction One",
        stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
        compartment="c",
        bounds=(-1000, 1000),
        reversible=True,
        gibbs0=1,
        ec="1.0.0.0",
        types=["type-1"],
        pathways={"pwy-1"},
        sequences={"monomer-1": "ABC"},
        monomers={"enzrxn-1": {"monomer-1"}},
        enzrxns={"enzrxn-1": {"km": {"cpd1": 1.0, "cpd2": 2.0}}},
        database_links={"kegg": {"some-id"}},
        transmembrane=False,
    )
    m.add_reaction(reaction=reaction)

    assert m.get_reaction_compartment_variants(reaction_base_id="rxn1") == {"rxn1"}
    assert m.get_reaction_base_id(reaction_id="rxn1") == "rxn1"
    assert m.get_reaction_compartment(reaction_id="rxn1") == "c"
    assert m.get_reaction_gibbs0(reaction_id="rxn1") == 1
    assert m.get_reaction_bounds(reaction_id="rxn1") == (-1000, 1000)
    assert m.get_reaction_reversibility(reaction_id="rxn1") is True
    assert m.get_reaction_pathways(reaction_id="rxn1") == {"pwy-1"}
    assert m.get_reaction_sequences(reaction_id="rxn1") == {"monomer-1": "ABC"}
    assert m.get_reaction_types(reaction_id="rxn1") == ["type-1"]
    assert m.get_reaction_database_links(reaction_id="rxn1") == {"kegg": {"some-id"}}

    assert m.get_base_reaction_ids() == {"rxn1"}
    assert m.get_reaction_type_ids() == {"type-1"}


def test_get_reaction_variants() -> None:
    m = Model()
    m.add_compartment(compartment_id="c", compartment_suffix="c")
    m.add_compound(Compound(base_id="cpd1", compartment="c"))
    m.add_compound(Compound(base_id="cpd2", compartment="c"))
    m.add_reaction(Reaction(id="rnx1", base_id="rxn1"))
    m.add_reaction(Reaction(id="rnx1__var__0", base_id="rxn1", _var=0))

    assert m.get_reaction_variants(base_reaction_id="rxn1") == {"rnx1__var__0"}


def test_get_reactions_of_compartment() -> None:
    m = Model()
    m.add_compartment(compartment_id="c", compartment_suffix="c")
    m.add_compartment(compartment_id="e", compartment_suffix="e")
    m.add_compound(Compound(base_id="cpd1", compartment="c"))
    m.add_compound(Compound(base_id="cpd2", compartment="c"))
    m.add_compound(Compound(base_id="cpd2", compartment="e"))
    m.add_reaction(
        Reaction(
            id="rxn1",
            base_id="rxn1",
            stoichiometries={"cpd1_c": -1, "cpd2_c": 1},
            transmembrane=False,
        )
    )
    m.add_reaction(
        Reaction(
            id="rxn1_trans",
            base_id="rxn1_trans",
            compartment="e",
            stoichiometries={"cpd2_e": -1, "cpd2_c": 1},
            transmembrane=True,
        )
    )
    assert m.get_reactions_of_compartment(compartment_id="c", include_transporters=False) == {"rxn1"}
    assert m.get_reactions_of_compartment(compartment_id="c", include_transporters=True) == {
        "rxn1",
        "rxn1_trans",
    }


def test_get_reversible_reactions() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_reactions(
        (
            Reaction(id="v_irrev", reversible=False),
            Reaction(id="v_rev", reversible=True),
        )
    )
    assert m.get_reversible_reactions() == ["v_rev"]


def test_get_irreversible_reactions() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_reactions(
        (
            Reaction(id="v_irrev", reversible=False),
            Reaction(id="v_rev", reversible=True),
        )
    )
    assert m.get_irreversible_reactions() == ["v_irrev"]


def test_add_pathway() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_reactions(
        (
            Reaction(id="v1"),
            Reaction(id="v2"),
            Reaction(id="v3"),
        )
    )
    m.add_pathway(pathway_id="pwy-101", pathway_reactions=["v2", "v3"])
    assert m.pathways == {"pwy-101": {"v2", "v3"}}
    assert not bool(m.reactions["v1"].pathways)
    assert m.reactions["v2"].pathways == {"pwy-101"}
    assert m.reactions["v3"].pathways == {"pwy-101"}


def test_remove_pathway() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_reactions(
        (
            Reaction(id="v1"),
            Reaction(id="v2"),
            Reaction(id="v3"),
        )
    )
    m.add_pathway(pathway_id="pwy-101", pathway_reactions=["v2", "v3"])
    m.remove_pathway(pathway_id="pwy-101")
    assert not bool(m.pathways)
    assert not bool(m.reactions["v1"].pathways)
    assert not bool(m.reactions["v2"].pathways)
    assert not bool(m.reactions["v3"].pathways)


def test_add_pathway_reaction_attribute() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_reactions(
        (
            Reaction(id="v1"),
            Reaction(id="v2"),
            Reaction(id="v3"),
        )
    )
    m.add_pathway("pwy-101", ["v2", "v3"])
    assert m.reactions["v1"].pathways == set()
    assert m.reactions["v2"].pathways == {"pwy-101"}
    assert m.reactions["v3"].pathways == {"pwy-101"}


def test_get_reactions_of_pathway() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_reactions(
        (
            Reaction(id="v1"),
            Reaction(id="v2"),
            Reaction(id="v3"),
        )
    )
    m.add_pathway("pwy-101", ["v2", "v3"])
    assert m.get_reactions_of_pathway("pwy-101") == {"v2", "v3"}


def test_get_pathway_ids() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_reactions(
        (
            Reaction(id="v1"),
            Reaction(id="v2"),
            Reaction(id="v3"),
        )
    )
    m.add_pathway("pwy-101", ["v2", "v3"])
    assert m.get_pathway_ids() == ("pwy-101",)


def test_add_transport_reaction_c_p() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="CYTOSOL"))
    m.add_transport_reaction(compound_id="cpd1_c", compartment_id="PERIPLASM")
    assert tuple(m.compounds.keys()) == ("cpd1_c", "cpd1_p")
    assert m.reactions["TR_cpd1_c_p"].stoichiometries == {"cpd1_c": -1, "cpd1_p": 1}


def test_add_transport_reaction_p_c() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="PERIPLASM"))
    m.add_transport_reaction(compound_id="cpd1_p", compartment_id="CYTOSOL")
    assert tuple(m.compounds.keys()) == ("cpd1_p", "cpd1_c")
    assert m.reactions["TR_cpd1_p_c"].stoichiometries == {"cpd1_p": -1, "cpd1_c": 1}


def test_add_transport_reaction_c_e() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="CYTOSOL"))
    m.add_transport_reaction(compound_id="cpd1_c", compartment_id="EXTRACELLULAR")
    assert tuple(m.compounds.keys()) == ("cpd1_c", "cpd1_e")
    assert m.reactions["TR_cpd1_c_e"].stoichiometries == {"cpd1_c": -1, "cpd1_e": 1}


def test_add_transport_reaction_e_c() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="EXTRACELLULAR"))
    m.add_transport_reaction(compound_id="cpd1_e", compartment_id="CYTOSOL")
    assert tuple(m.compounds.keys()) == ("cpd1_e", "cpd1_c")
    assert m.reactions["TR_cpd1_e_c"].stoichiometries == {"cpd1_e": -1, "cpd1_c": 1}


def test_add_transport_reaction_p_e() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="PERIPLASM"))
    m.add_transport_reaction(compound_id="cpd1_p", compartment_id="EXTRACELLULAR")
    assert tuple(m.compounds.keys()) == ("cpd1_p", "cpd1_e")
    assert m.reactions["TR_cpd1_p_e"].stoichiometries == {"cpd1_p": -1, "cpd1_e": 1}


def test_add_transport_reaction_e_p() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="EXTRACELLULAR"))
    m.add_transport_reaction(compound_id="cpd1_e", compartment_id="PERIPLASM")
    assert tuple(m.compounds.keys()) == ("cpd1_e", "cpd1_p")
    assert m.reactions["TR_cpd1_e_p"].stoichiometries == {"cpd1_e": -1, "cpd1_p": 1}


def test_add_influx_base_compound() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="CYTOSOL"))
    m.add_influx("cpd1", extracellular_compartment_id="EXTRACELLULAR")
    assert tuple(m.compounds) == ("cpd1_c", "cpd1_e")
    assert m.reactions["EX_cpd1_e"].stoichiometries == {"cpd1_e": -1}
    assert m.reactions["EX_cpd1_e"].bounds == (-1000, 0)
    assert m.reactions["EX_cpd1_e"].reversible is False


def test_add_efflux_base_compound() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="CYTOSOL"))
    m.add_efflux("cpd1", extracellular_compartment_id="EXTRACELLULAR")
    assert tuple(m.compounds) == ("cpd1_c", "cpd1_e")
    assert m.reactions["EX_cpd1_e"].stoichiometries == {"cpd1_e": -1}
    assert m.reactions["EX_cpd1_e"].bounds == (0, 1000)
    assert m.reactions["EX_cpd1_e"].reversible is False


def test_add_medium_base_compound() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="CYTOSOL"))
    m.add_medium_component("cpd1", extracellular_compartment_id="EXTRACELLULAR")
    assert tuple(m.compounds) == ("cpd1_c", "cpd1_e")
    assert m.reactions["EX_cpd1_e"].stoichiometries == {"cpd1_e": -1}
    assert m.reactions["EX_cpd1_e"].bounds == (-1000, 1000)
    assert m.reactions["EX_cpd1_e"].reversible is True


def test_add_influx_cytosol() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="CYTOSOL"))
    m.add_influx("cpd1_c", extracellular_compartment_id="EXTRACELLULAR")
    assert tuple(m.compounds) == ("cpd1_c", "cpd1_e")
    assert m.reactions["EX_cpd1_e"].stoichiometries == {"cpd1_e": -1}
    assert m.reactions["EX_cpd1_e"].bounds == (-1000, 0)
    assert m.reactions["EX_cpd1_e"].reversible is False


def test_add_efflux_cytosol() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="CYTOSOL"))
    m.add_efflux("cpd1_c", extracellular_compartment_id="EXTRACELLULAR")
    assert tuple(m.compounds) == ("cpd1_c", "cpd1_e")
    assert m.reactions["EX_cpd1_e"].stoichiometries == {"cpd1_e": -1}
    assert m.reactions["EX_cpd1_e"].bounds == (0, 1000)
    assert m.reactions["EX_cpd1_e"].reversible is False


def test_add_medium_cytosol() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="CYTOSOL"))
    m.add_medium_component("cpd1_c", extracellular_compartment_id="EXTRACELLULAR")
    assert tuple(m.compounds) == ("cpd1_c", "cpd1_e")
    assert m.reactions["EX_cpd1_e"].stoichiometries == {"cpd1_e": -1}
    assert m.reactions["EX_cpd1_e"].bounds == (-1000, 1000)
    assert m.reactions["EX_cpd1_e"].reversible is True


def test_add_influx_extracellular() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="EXTRACELLULAR"))
    m.add_influx("cpd1_e", extracellular_compartment_id="EXTRACELLULAR")
    assert tuple(m.compounds) == ("cpd1_e",)
    assert m.reactions["EX_cpd1_e"].stoichiometries == {"cpd1_e": -1}
    assert m.reactions["EX_cpd1_e"].bounds == (-1000, 0)
    assert m.reactions["EX_cpd1_e"].reversible is False


def test_add_efflux_extracellular() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="EXTRACELLULAR"))
    m.add_efflux("cpd1_e", extracellular_compartment_id="EXTRACELLULAR")
    assert tuple(m.compounds) == ("cpd1_e",)
    assert m.reactions["EX_cpd1_e"].stoichiometries == {"cpd1_e": -1}
    assert m.reactions["EX_cpd1_e"].bounds == (0, 1000)
    assert m.reactions["EX_cpd1_e"].reversible is False


def test_add_medium_extracellular() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="EXTRACELLULAR"))
    m.add_medium_component("cpd1_e", extracellular_compartment_id="EXTRACELLULAR")
    assert tuple(m.compounds) == ("cpd1_e",)
    assert m.reactions["EX_cpd1_e"].stoichiometries == {"cpd1_e": -1}
    assert m.reactions["EX_cpd1_e"].bounds == (-1000, 1000)
    assert m.reactions["EX_cpd1_e"].reversible is True


def test_remove_influx_base_compound() -> None:
    compartments = {"CYTOSOL": "c", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="CYTOSOL"))
    m.add_influx("cpd1", extracellular_compartment_id="EXTRACELLULAR")
    m.remove_influx(compound_id="cpd1")
    assert tuple(m.compounds) == ("cpd1_c",)
    assert not bool(m.reactions)


def test_remove_efflux_base_compound() -> None:
    compartments = {"CYTOSOL": "c", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="CYTOSOL"))
    m.add_efflux("cpd1", extracellular_compartment_id="EXTRACELLULAR")
    m.remove_efflux(compound_id="cpd1")
    assert tuple(m.compounds) == ("cpd1_c",)
    assert not bool(m.reactions)


def test_remove_medium_base_compound() -> None:
    compartments = {"CYTOSOL": "c", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="CYTOSOL"))
    m.add_medium_component("cpd1", extracellular_compartment_id="EXTRACELLULAR")
    m.remove_medium_component(compound_id="cpd1")
    assert tuple(m.compounds) == ("cpd1_c",)
    assert not bool(m.reactions)


def test_remove_influx_cytosol() -> None:
    compartments = {"CYTOSOL": "c", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="CYTOSOL"))
    m.add_influx("cpd1_c", extracellular_compartment_id="EXTRACELLULAR")
    m.remove_influx(compound_id="cpd1_c")
    assert tuple(m.compounds) == ("cpd1_c",)
    assert not bool(m.reactions)


def test_remove_efflux_cytosol() -> None:
    compartments = {"CYTOSOL": "c", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="CYTOSOL"))
    m.add_efflux("cpd1_c", extracellular_compartment_id="EXTRACELLULAR")
    m.remove_efflux(compound_id="cpd1_c")
    assert tuple(m.compounds) == ("cpd1_c",)
    assert not bool(m.reactions)


def test_remove_medium_cytosol() -> None:
    compartments = {"CYTOSOL": "c", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="CYTOSOL"))
    m.add_medium_component("cpd1_c", extracellular_compartment_id="EXTRACELLULAR")
    m.remove_medium_component(compound_id="cpd1_c")
    assert tuple(m.compounds) == ("cpd1_c",)
    assert not bool(m.reactions)


def test_remove_influx_extracellular() -> None:
    compartments = {"CYTOSOL": "c", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="EXTRACELLULAR"))
    m.add_influx("cpd1_e", extracellular_compartment_id="EXTRACELLULAR")
    m.remove_influx(compound_id="cpd1_e")
    assert not tuple(m.compounds)
    assert not bool(m.reactions)


def test_remove_efflux_extracellular() -> None:
    compartments = {"CYTOSOL": "c", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="EXTRACELLULAR"))
    m.add_efflux("cpd1_e", extracellular_compartment_id="EXTRACELLULAR")
    m.remove_efflux(compound_id="cpd1_e")
    assert not tuple(m.compounds)
    assert not bool(m.reactions)


def test_remove_medium_extracellular() -> None:
    compartments = {"CYTOSOL": "c", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="EXTRACELLULAR"))
    m.add_medium_component("cpd1_e", extracellular_compartment_id="EXTRACELLULAR")
    m.remove_medium_component(compound_id="cpd1_e")
    assert not tuple(m.compounds)
    assert not bool(m.reactions)


def test_remove_influx_missing() -> None:
    compartments = {"CYTOSOL": "c", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="EXTRACELLULAR"))
    m.add_influx("cpd1_e", extracellular_compartment_id="EXTRACELLULAR")
    with pytest.raises(KeyError):
        m.remove_influx(compound_id="garbage")


def test_remove_efflux_missing() -> None:
    compartments = {"CYTOSOL": "c", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="EXTRACELLULAR"))
    m.add_efflux("cpd1_e", extracellular_compartment_id="EXTRACELLULAR")
    with pytest.raises(KeyError):
        m.remove_efflux(compound_id="garbage")


def test_remove_medium_missing() -> None:
    compartments = {"CYTOSOL": "c", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compound(Compound(base_id="cpd1", compartment="EXTRACELLULAR"))
    m.add_medium_component("cpd1_e", extracellular_compartment_id="EXTRACELLULAR")
    with pytest.raises(KeyError):
        m.remove_medium_component(compound_id="garbage")
