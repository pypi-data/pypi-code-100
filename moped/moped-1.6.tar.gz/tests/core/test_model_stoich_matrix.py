from moped import Compound, Model, Reaction

import numpy as np


def test_get_stoichiometric_matrix() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
            Compound(base_id="cpd3", compartment="CYTOSOL"),
        )
    )
    m.add_reactions(
        (
            Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
            Reaction(id="v2", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}),
        )
    )
    assert np.all(
        np.equal(
            m.get_stoichiometric_matrix(),
            np.array([[-1.0, 0.0], [1.0, -1.0], [0.0, 1.0]]),
        )
    )


def test_get_stoichiometric_df() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compartments=compartments)
    m.add_compounds(
        (
            Compound(base_id="cpd1", compartment="CYTOSOL"),
            Compound(base_id="cpd2", compartment="CYTOSOL"),
            Compound(base_id="cpd3", compartment="CYTOSOL"),
        )
    )
    m.add_reactions(
        (
            Reaction(id="v1", stoichiometries={"cpd1_c": -1, "cpd2_c": 1}),
            Reaction(id="v2", stoichiometries={"cpd2_c": -1, "cpd3_c": 1}),
        )
    )
    df = m.get_stoichiometric_df()
    assert tuple(df.index) == ("cpd1_c", "cpd2_c", "cpd3_c")
    assert tuple(df.columns) == ("v1", "v2")
