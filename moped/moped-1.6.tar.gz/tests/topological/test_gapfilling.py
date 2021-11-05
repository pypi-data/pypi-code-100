import io
from unittest import mock

from moped import Compound, Model, Reaction

import pytest


def test_fail_on_wrong_seed_num() -> None:
    m = Model()
    db = Model()
    with pytest.raises(TypeError):
        m.get_gapfilling_reactions(reference_model=db, seed=0, targets=["cpd3_c"], verbose=False)  # type: ignore


def test_fail_on_wrong_seed_list_num() -> None:
    m = Model()
    db = Model()
    with pytest.raises(TypeError):
        m.get_gapfilling_reactions(reference_model=db, seed=[0], targets=["cpd3_c"], verbose=False)  # type: ignore


def test_linear_chain() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    model_reactions = (Reaction("rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),)
    db_reactions = (
        Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
        Reaction(id="rxn2", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}),
    )
    m = Model(compounds=compounds, reactions=model_reactions, compartments=compartments)
    db = Model(compounds=compounds, reactions=db_reactions, compartments=compartments)
    assert ["rxn2"] == m.get_gapfilling_reactions(
        reference_model=db, seed=["cpd1_c"], targets=["cpd3_c"], verbose=False
    )


def test_linear_chain_gapfilling() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    model_reactions = (Reaction("rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),)
    db_reactions = (
        Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
        Reaction(id="rxn2", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}),
    )
    m = Model(compounds=compounds, reactions=model_reactions, compartments=compartments)
    db = Model(compounds=compounds, reactions=db_reactions, compartments=compartments)

    gapfilling_reactions = m.get_gapfilling_reactions(
        reference_model=db, seed=["cpd1_c"], targets=["cpd3_c"], verbose=False
    )
    m2 = m.copy()
    m2.gapfilling(reference_model=db, seed=["cpd1_c"], targets=["cpd3_c"], verbose=False)
    assert set(m.reactions) | set(gapfilling_reactions) == set(m2.reactions)


def test_linear_chain_str_seed() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    model_reactions = (Reaction("rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),)
    db_reactions = (
        Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
        Reaction(id="rxn2", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}),
    )
    m = Model(compounds=compounds, reactions=model_reactions, compartments=compartments)
    db = Model(compounds=compounds, reactions=db_reactions, compartments=compartments)
    assert ["rxn2"] == m.get_gapfilling_reactions(
        reference_model=db, seed="cpd1_c", targets=["cpd3_c"], verbose=False
    )


def test_linear_chain_verbose() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    model_reactions = (Reaction("rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),)
    db_reactions = (
        Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
        Reaction(id="rxn2", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}),
    )
    m = Model(compounds=compounds, reactions=model_reactions, compartments=compartments)
    db = Model(compounds=compounds, reactions=db_reactions, compartments=compartments)

    with mock.patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        m.get_gapfilling_reactions(reference_model=db, seed=["cpd1_c"], targets=["cpd3_c"], verbose=True)
    assert mock_stdout.getvalue().split("\n") == [
        "Searching for ['cpd3_c'] in reference database",
        "Could produce all compounds in reference database",
        "Found 1 essential reaction(s)",
        "",
    ]


def test_linear_chain_gapfilling_verbose() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    model_reactions = (Reaction("rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),)
    db_reactions = (
        Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
        Reaction(id="rxn2", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}),
    )
    m = Model(compounds=compounds, reactions=model_reactions, compartments=compartments)
    db = Model(compounds=compounds, reactions=db_reactions, compartments=compartments)
    with mock.patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        m.gapfilling(reference_model=db, seed=["cpd1_c"], targets=["cpd3_c"], verbose=True)
    assert mock_stdout.getvalue().split("\n") == [
        "Searching for ['cpd3_c'] in reference database",
        "Could produce all compounds in reference database",
        "Found 1 essential reaction(s)",
        "Adding reactions ['rxn2']",
        "",
    ]


def test_linear_chain_fail_verbose() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    model_reactions = (Reaction("rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),)
    m = Model(compounds=compounds, reactions=model_reactions, compartments=compartments)

    with mock.patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        with pytest.warns(UserWarning):
            m.get_gapfilling_reactions(reference_model=m, seed=["cpd1_c"], targets=["cpd3_c"], verbose=True)
    assert mock_stdout.getvalue().split("\n") == [
        "Searching for ['cpd3_c'] in reference database",
        "Could produce [] in reference database",
        "Found 0 essential reaction(s)",
        "",
    ]


def test_linear_chain_fail_on_missing() -> None:
    model_compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
    )
    db_compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    model_reactions = (Reaction("rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),)
    db_reactions = (Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),)
    m = Model(
        compounds=model_compounds,
        reactions=model_reactions,
        compartments=compartments,
    )
    db = Model(compounds=db_compounds, reactions=db_reactions, compartments=compartments)
    with pytest.warns(UserWarning):
        m.get_gapfilling_reactions(reference_model=db, seed=["cpd1_c"], targets=["cpd3_c"], verbose=False)


def test_linear_chain_water_addition() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
        Compound(base_id="cpd4", compartment="CYTOSOL"),
        Compound(base_id="WATER", compartment="CYTOSOL"),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    model_reactions = (Reaction("rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),)
    db_reactions = (
        Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
        Reaction(id="rxn2", stoichiometries={"cpd2_c": -1, "WATER_c": -1, "cpd3_c": 1}),
        Reaction(id="rxn3", stoichiometries={"cpd3_c": -1, "cpd4_c": 1}),
    )
    m = Model(compounds=compounds, reactions=model_reactions, compartments=compartments)
    db = Model(compounds=compounds, reactions=db_reactions, compartments=compartments)
    reaction_ids = m.get_gapfilling_reactions(
        reference_model=db,
        seed=["cpd1_c", "WATER_c"],
        targets=["cpd4_c"],
        verbose=False,
    )
    assert set(reaction_ids) == set(["rxn3", "rxn2"])


def test_linear_reversible_duplication() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    model_reactions = (Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),)
    db_reactions = (
        Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
        Reaction(id="rxn2", stoichiometries={"cpd3_c": -1, "cpd2_c": 1}, reversible=True),
    )
    m = Model(compounds=compounds, reactions=model_reactions, compartments=compartments)
    db = Model(compounds=compounds, reactions=db_reactions, compartments=compartments)
    db.reversibility_duplication()
    assert ["rxn2__rev__"] == m.get_gapfilling_reactions(
        reference_model=db, seed=["cpd1_c"], targets=["cpd3_c"], verbose=False
    )


def test_linear_chain_fail_on_reverse() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    model_reactions = (Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),)
    db_reactions = (
        Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
        Reaction(id="rxn2", stoichiometries={"cpd3_c": -1, "cpd2_c": 1}),
    )
    m = Model(compounds=compounds, reactions=model_reactions, compartments=compartments)
    db = Model(compounds=compounds, reactions=db_reactions, compartments=compartments)
    assert [] == m.get_gapfilling_reactions(
        reference_model=db, seed=["cpd1_c"], targets=["cpd3_c"], verbose=False
    )


def test_linear_chain_fail_on_reverse_with_duplication() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    model_reactions = (Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),)
    db_reactions = (
        Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
        Reaction(id="rxn2", stoichiometries={"cpd3_c": -1, "cpd2_c": 1}),
    )
    m = Model(compounds=compounds, reactions=model_reactions, compartments=compartments)
    db = Model(compounds=compounds, reactions=db_reactions, compartments=compartments)
    db.reversibility_duplication()
    assert [] == m.get_gapfilling_reactions(
        reference_model=db, seed=["cpd1_c"], targets=["cpd3_c"], verbose=False
    )


def test_linear_chain_cofactor_duplicated() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
        Compound(base_id="cpd4", compartment="CYTOSOL"),
        Compound(base_id="ATP", compartment="CYTOSOL"),
        Compound(base_id="ADP", compartment="CYTOSOL"),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    model_reactions = (Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),)
    db_reactions = (
        Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
        Reaction(
            id="rxn2",
            stoichiometries={"cpd2_c": -1, "ADP_c": -1, "cpd3_c": 1, "ATP_c": 1},
        ),
        Reaction(id="rxn3", stoichiometries={"cpd3_c": -1, "cpd4_c": 1}),
    )
    m = Model(compounds=compounds, reactions=model_reactions, compartments=compartments)
    db = Model(compounds=compounds, reactions=db_reactions, compartments=compartments)
    db.cofactor_pairs = {"ATP_c": "ADP_c"}
    db.cofactor_duplication()
    m.cofactor_pairs = {"ATP_c": "ADP_c"}
    reaction_ids = m.get_gapfilling_reactions(
        reference_model=db,
        seed=["cpd1_c"] + m.get_weak_cofactor_duplications(),
        targets=["cpd4_c"],
        verbose=False,
    )
    assert set(reaction_ids) == set(["rxn2__cof__", "rxn3"])


def test_linear_chain_include_cofactor_duplicated() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
        Compound(base_id="cpd4", compartment="CYTOSOL"),
        Compound(base_id="ATP", compartment="CYTOSOL"),
        Compound(base_id="ADP", compartment="CYTOSOL"),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    model_reactions = (Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),)
    db_reactions = (
        Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
        Reaction(
            id="rxn2",
            stoichiometries={"cpd2_c": -1, "ADP_c": -1, "cpd3_c": 1, "ATP_c": 1},
        ),
        Reaction(id="rxn3", stoichiometries={"cpd3_c": -1, "cpd4_c": 1}),
    )
    m = Model(compounds=compounds, reactions=model_reactions, compartments=compartments)
    m.add_cofactor_pair(strong_cofactor_base_id="ATP_c", weak_cofactor_base_id="ADP_c")
    db = Model(compounds=compounds, reactions=db_reactions, compartments=compartments)
    db.cofactor_pairs = {"ATP_c": "ADP_c"}
    db.cofactor_duplication()
    m.cofactor_pairs = {"ATP_c": "ADP_c"}
    reaction_ids = m.get_gapfilling_reactions(
        reference_model=db,
        seed=["cpd1_c"],
        targets=["cpd4_c"],
        include_weak_cofactors=True,
        verbose=False,
    )
    assert set(reaction_ids) == set(["rxn2__cof__", "rxn3"])


def test_linear_chain_cofactor_duplicated_fail_without_duplication() -> None:
    compounds = (
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd3", compartment="CYTOSOL"),
        Compound(base_id="cpd4", compartment="CYTOSOL"),
        Compound(base_id="ATP", compartment="CYTOSOL"),
        Compound(base_id="ADP", compartment="CYTOSOL"),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    model_reactions = (Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),)
    db_reactions = (
        Reaction(id="rxn1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
        Reaction(
            id="rxn2",
            stoichiometries={"cpd2_c": -1, "ADP_c": -1, "cpd3_c": 1, "ATP_c": 1},
        ),
        Reaction(id="rxn3", stoichiometries={"cpd3_c": -1, "cpd4_c": 1}),
    )
    m = Model(compounds=compounds, reactions=model_reactions, compartments=compartments)
    db = Model(compounds=compounds, reactions=db_reactions, compartments=compartments)
    db.cofactor_pairs = {"ATP_c": "ADP_c"}
    m.cofactor_pairs = {"ATP_c": "ADP_c"}

    reaction_ids = m.get_gapfilling_reactions(
        reference_model=db,
        seed=["cpd1_c"] + m.get_weak_cofactor_duplications(),
        targets=["cpd4_c"],
        verbose=False,
    )

    assert reaction_ids == []
