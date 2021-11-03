from moped import Compound, Model, Reaction

import pytest


def test_set_objective_single() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
    )
    reactions = (Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),)
    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    m.set_objective({"v1": 1})
    assert m.objective == {"v1": 1}


def test_set_objective_multiple() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
    )
    reactions = (
        Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
        Reaction(id="v2", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}),
    )
    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    m.set_objective({"v1": 1, "v2": 2})
    assert m.objective == {"v1": 1, "v2": 2}


def test_set_objective_fail_on_missing() -> None:
    m = Model()
    with pytest.raises(KeyError):
        m.set_objective(objective={"v1": 1})


def test_init_objective() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
    )
    reactions = (
        Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
        Reaction(id="v2", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}),
    )
    objective = {"v1": 1.0, "v2": 2.0}
    m = Model(
        compounds=compounds,
        reactions=reactions,
        compartments=compartments,
        objective=objective,
    )
    assert m.objective == {"v1": 1, "v2": 2}
