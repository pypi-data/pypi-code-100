from moped import Compound, Model, Reaction
from moped.topological.scope import _split_stoichiometries

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


def test_fail_on_wrong_seed_num() -> None:
    m = Model()
    with pytest.raises(TypeError):
        rxns, cpds = m.scope(seed=1)  # type: ignore


def test_fail_on_wrong_seed_list_num() -> None:
    m = Model()
    with pytest.raises(TypeError):
        rxns, cpds = m.scope(seed=[1])  # type: ignore


def test_linear_chain() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
        Compound(base_id="WATER", compartment="CYTOSOL"),
    )
    reactions = (
        Reaction("rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
        Reaction("rxn2", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    rxns, cpds = m.scope(seed=["cpd1_c"], return_lumped_results=False)
    assert rxns == [{"rxn1"}, {"rxn2"}]
    assert cpds == [{"cpd2_c"}, {"cpd3_c"}]


def test_linear_chain_lumped_results() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
        Compound(base_id="WATER", compartment="CYTOSOL"),
    )
    reactions = (
        Reaction("rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
        Reaction("rxn2", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    rxns, cpds = m.scope(seed=["cpd1_c"], return_lumped_results=True)
    assert rxns == {"rxn1", "rxn2"}
    assert cpds == {"cpd2_c", "cpd3_c"}


def test_linear_chain_str_seed() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
        Compound(base_id="WATER", compartment="CYTOSOL"),
    )
    reactions = (
        Reaction("rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
        Reaction("rxn2", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    rxns, cpds = m.scope(seed="cpd1_c", return_lumped_results=False)
    assert rxns == [{"rxn1"}, {"rxn2"}]
    assert cpds == [{"cpd2_c"}, {"cpd3_c"}]


def test_linear_chain_water_addition() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
        Compound(base_id="cpd4", compartment="CYTOSOL"),
        Compound(base_id="WATER", compartment="CYTOSOL"),
    )
    reactions = (
        Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
        Reaction(id="rxn2", stoichiometries={"cpd2_c": -1, "WATER_c": -1, "cpd3_c": 1}),
        Reaction(id="rxn3", stoichiometries={"cpd3_c": -1, "cpd4_c": 1}),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    rxns, cpds = m.scope(seed=["cpd1_c", "WATER_c"], return_lumped_results=False)
    assert rxns == [{"rxn1"}, {"rxn2"}, {"rxn3"}]
    assert cpds == [{"cpd2_c"}, {"cpd3_c"}, {"cpd4_c"}]


def test_linear_chain_cofactor_duplicated() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
        Compound(base_id="cpd4", compartment="CYTOSOL"),
        Compound(base_id="NADH", compartment="CYTOSOL"),
        Compound(base_id="NAD", compartment="CYTOSOL"),
        Compound(base_id="WATER", compartment="CYTOSOL"),
    )
    reactions = (
        Reaction(
            id="rxn1",
            stoichiometries={"cpd1_c": -1, "NAD_c": -1, "cpd2_c": 1, "NADH_c": 1},
        ),
        Reaction(id="rxn2", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}),
        Reaction(
            id="rxn3",
            stoichiometries={"cpd3_c": -1, "NADH_c": -1, "cpd4_c": 1, "NAD_c": 1},
        ),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    m.cofactor_pairs = {"NADH_c": "NAD_c"}
    m.cofactor_duplication()
    rxns, cpds = m.scope(seed=["cpd1_c"], include_weak_cofactors=True, return_lumped_results=False)
    assert rxns == [{"rxn1__cof__"}, {"rxn2"}, {"rxn3__cof__"}]
    assert cpds == [{"cpd2_c", "NADH_c__cof__"}, {"cpd3_c"}, {"cpd4_c"}]


def test_linear_chain_irreversible_duplicated() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
        Compound(base_id="WATER", compartment="CYTOSOL"),
    )
    reactions = (
        Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}, reversible=False),
        Reaction(id="rxn2", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}, reversible=False),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    m.reversibility_duplication()
    rxns, cpds = m.scope(seed=["cpd3_c"], return_lumped_results=False)
    assert rxns == []
    assert cpds == []


def test_linear_chain_reversible_duplicated() -> None:
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
    rxns, cpds = m.scope(seed=["cpd3_c"], return_lumped_results=False)
    assert rxns == [{"rxn2__rev__"}, {"rxn2", "rxn1__rev__"}, {"rxn1"}]
    assert cpds == [{"cpd2_c"}, {"cpd1_c"}, set()]


def test_multiple_scopes() -> None:
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
    results = m.multiple_scopes(
        seeds=[["cpd1_c"], ["cpd2_c"], ["cpd3_c"]],
        return_lumped_results=False,
        multiprocessing=False,
    )
    assert results[("cpd1_c",)] == (
        [{"rxn1"}, {"rxn1__rev__", "rxn2"}, {"rxn2__rev__"}],
        [{"cpd2_c"}, {"cpd3_c"}, set()],
    )
    assert results[("cpd2_c",)] == (
        [{"rxn1__rev__", "rxn2"}, {"rxn1", "rxn2__rev__"}],
        [{"cpd1_c", "cpd3_c"}, set()],
    )
    assert results[("cpd3_c",)] == (
        [{"rxn2__rev__"}, {"rxn2", "rxn1__rev__"}, {"rxn1"}],
        [{"cpd2_c"}, {"cpd1_c"}, set()],
    )


def test_multiple_scopes_multiprocessing() -> None:
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
    results = m.multiple_scopes(
        seeds=[["cpd1_c"], ["cpd2_c"], ["cpd3_c"]],
        return_lumped_results=False,
        multiprocessing=True,
    )
    assert results[("cpd1_c",)] == (
        [{"rxn1"}, {"rxn1__rev__", "rxn2"}, {"rxn2__rev__"}],
        [{"cpd2_c"}, {"cpd3_c"}, set()],
    )
    assert results[("cpd2_c",)] == (
        [{"rxn1__rev__", "rxn2"}, {"rxn1", "rxn2__rev__"}],
        [{"cpd1_c", "cpd3_c"}, set()],
    )
    assert results[("cpd3_c",)] == (
        [{"rxn2__rev__"}, {"rxn2", "rxn1__rev__"}, {"rxn1"}],
        [{"cpd2_c"}, {"cpd1_c"}, set()],
    )
