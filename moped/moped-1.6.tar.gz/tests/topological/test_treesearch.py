from moped import Compound, Model, Reaction
from moped.topological.treesearch import _split_stoichiometries, metabolite_tree_search

import pytest


def test_split_stoichiometries() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
    )
    reactions = (Reaction("rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),)
    compartments = {"CYTOSOL": "c"}
    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    assert _split_stoichiometries(m) == {"rxn1": {"substrates": {"cpd1_c": -1}, "products": {"cpd2_c": 1}}}


def test_split_stoichiometries_exclude_medium_reactions() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
    )
    reactions = (Reaction("rxn1", stoichiometries={"cpd1_c": -1}),)
    compartments = {"CYTOSOL": "c"}
    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    assert _split_stoichiometries(m) == {}


def test_fail_on_wrong_search_type() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
        Compound(base_id="WATER", compartment="CYTOSOL"),
    )
    reactions = (
        Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}, reversible=True),
        Reaction(id="rxn2", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}, reversible=True),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    m.reversibility_duplication()

    with pytest.raises(ValueError):
        metabolite_tree_search(
            model=m,
            start_compound_id="cpd1_c",
            end_compound_id="cpd3_c",
            max_iterations=50,
            ignored_reaction_ids=None,
            ignored_compound_ids=None,
            search_type="nonsense",  # type: ignore
        )


def test_fail_on_missing_metabolite() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
        Compound(base_id="WATER", compartment="CYTOSOL"),
    )
    reactions = (
        Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}, reversible=True),
        Reaction(id="rxn2", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}, reversible=True),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    m.reversibility_duplication()
    with pytest.raises(KeyError):
        m.depth_first_search(
            start_compound_id="cpd1_c",
            end_compound_id="cpd4_c",
            max_iterations=50,
        )


def test_fail_on_no_solution() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
        Compound(base_id="WATER", compartment="CYTOSOL"),
    )
    reactions = (Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}, reversible=True),)
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    m.reversibility_duplication()
    with pytest.raises(ValueError):
        m.depth_first_search(
            start_compound_id="cpd1_c",
            end_compound_id="cpd3_c",
            max_iterations=50,
        )


def test_fail_on_max_iterations() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
        Compound(base_id="WATER", compartment="CYTOSOL"),
    )
    reactions = (
        Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}, reversible=True),
        Reaction(id="rxn2", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}, reversible=True),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    m.reversibility_duplication()

    with pytest.raises(ValueError):
        m.depth_first_search(
            start_compound_id="cpd1_c",
            end_compound_id="cpd3_c",
            max_iterations=1,
        )


def test_depth_first_search() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
        Compound(base_id="WATER", compartment="CYTOSOL"),
    )
    reactions = (
        Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}, reversible=True),
        Reaction(id="rxn2", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}, reversible=True),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    m.reversibility_duplication()

    cpds, rxns = m.depth_first_search(
        start_compound_id="cpd1_c",
        end_compound_id="cpd3_c",
        max_iterations=50,
    )
    assert cpds == ["cpd1_c", "cpd2_c", "cpd3_c"]
    assert rxns == ["rxn1", "rxn2"]


def test_breadth_first_search() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
        Compound(base_id="WATER", compartment="CYTOSOL"),
    )
    reactions = (
        Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}, reversible=True),
        Reaction(id="rxn2", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}, reversible=True),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    m.reversibility_duplication()

    cpds, rxns = m.breadth_first_search(
        start_compound_id="cpd1_c",
        end_compound_id="cpd3_c",
        max_iterations=50,
    )
    assert cpds == ["cpd1_c", "cpd2_c", "cpd3_c"]
    assert rxns == ["rxn1", "rxn2"]


def test_metabolite_search_ignore_reactions() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
        Compound(base_id="WATER", compartment="CYTOSOL"),
    )
    reactions = (
        Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}, reversible=True),
        Reaction(id="rxn2", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}, reversible=True),
        Reaction(id="rxn3", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}, reversible=True),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    m.reversibility_duplication()

    cpds, rxns = m.depth_first_search(
        start_compound_id="cpd1_c",
        end_compound_id="cpd3_c",
        max_iterations=50,
        ignored_reaction_ids=["rxn2"],
    )
    assert cpds == ["cpd1_c", "cpd2_c", "cpd3_c"]
    assert rxns == ["rxn1", "rxn3"]


def test_metabolite_search_ignore_compounds() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2.1", compartment="CYTOSOL"),
        Compound(base_id="cpd2.2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
        Compound(base_id="WATER", compartment="CYTOSOL"),
    )
    reactions = (
        Reaction(
            id="rxn1.1",
            stoichiometries={"cpd1_c": -1, "cpd2.1_c": 1},
            reversible=True,
        ),
        Reaction(
            id="rxn1.2",
            stoichiometries={"cpd1_c": -1, "cpd2.2_c": 1},
            reversible=True,
        ),
        Reaction(
            id="rxn2.1",
            stoichiometries={"cpd2.1_c": -1, "cpd3_c": 1},
            reversible=True,
        ),
        Reaction(
            id="rxn2.2",
            stoichiometries={"cpd2.2_c": -1, "cpd3_c": 1},
            reversible=True,
        ),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    m.reversibility_duplication()

    cpds, rxns = m.depth_first_search(
        start_compound_id="cpd1_c",
        end_compound_id="cpd3_c",
        max_iterations=50,
        ignored_compound_ids=["cpd2.1_c"],
    )
    assert cpds == ["cpd1_c", "cpd2.2_c", "cpd3_c"]
    assert rxns == ["rxn1.2", "rxn2.2"]
