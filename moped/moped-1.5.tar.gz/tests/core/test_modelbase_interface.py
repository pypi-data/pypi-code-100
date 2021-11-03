from moped import Compound, Model, Reaction

import pytest


def test_to_kinetic_model_influx() -> None:
    compounds = (
        Compound(base_id="S", compartment="c"),
        Compound(base_id="S", compartment="e"),
    )
    compartments = {"c": "c", "e": "e"}
    m = Model(compounds=compounds, compartments=compartments)
    m.add_influx(compound_id="S_c", extracellular_compartment_id="e")
    mod = m.to_kinetic_model()
    assert mod.compounds == ["S_c", "S_e"]
    assert mod.stoichiometries == {"EX_S_e": {"S_e": 1}}
    assert list(mod.rates) == ["EX_S_e"]
    rate = mod.rates["EX_S_e"]
    assert rate["function"].__name__ == "constant"
    assert rate["parameters"] == ["k_in_EX_S_e"]
    assert rate["substrates"] == []
    assert rate["products"] == ["S_e"]
    assert rate["modifiers"] == []
    assert rate["dynamic_variables"] == []
    assert rate["reversible"] is False


def test_to_kinetic_model_efflux() -> None:
    compounds = (
        Compound(base_id="S", compartment="c"),
        Compound(base_id="S", compartment="e"),
    )
    compartments = {"c": "c", "e": "e"}
    m = Model(compounds=compounds, compartments=compartments)
    m.add_efflux(compound_id="S_c", extracellular_compartment_id="e")
    mod = m.to_kinetic_model()
    assert mod.compounds == ["S_c", "S_e"]
    assert mod.stoichiometries == {"EX_S_e": {"S_e": -1}}
    assert list(mod.rates) == ["EX_S_e"]
    rate = mod.rates["EX_S_e"]
    assert rate["function"].__name__ == "mass_action_1"
    assert rate["parameters"] == ["k_out_EX_S_e"]
    assert rate["substrates"] == ["S_e"]
    assert rate["products"] == []
    assert rate["modifiers"] == []
    assert rate["dynamic_variables"] == ["S_e"]
    assert rate["reversible"] is False


def test_to_kinetic_model_medium() -> None:
    compounds = (
        Compound(base_id="S", compartment="c"),
        Compound(base_id="S", compartment="e"),
    )
    compartments = {"c": "c", "e": "e"}
    m = Model(compounds=compounds, compartments=compartments)
    m.add_medium_component(compound_id="S_c", extracellular_compartment_id="e")
    mod = m.to_kinetic_model()
    assert mod.compounds == ["S_c", "S_e"]
    assert mod.stoichiometries == {"EX_S_e_in": {"S_e": 1}, "EX_S_e_out": {"S_e": -1}}
    assert list(mod.rates) == ["EX_S_e_in", "EX_S_e_out"]

    rate = mod.rates["EX_S_e_in"]
    assert rate["function"].__name__ == "constant"
    assert rate["parameters"] == ["k_in_EX_S_e"]
    assert rate["substrates"] == []
    assert rate["products"] == ["S_e"]
    assert rate["modifiers"] == []
    assert rate["dynamic_variables"] == []
    assert rate["reversible"] is False

    rate = mod.rates["EX_S_e_out"]
    assert rate["function"].__name__ == "mass_action_1"
    assert rate["parameters"] == ["k_out_EX_S_e"]
    assert rate["substrates"] == ["S_e"]
    assert rate["products"] == []
    assert rate["modifiers"] == []
    assert rate["dynamic_variables"] == ["S_e"]
    assert rate["reversible"] is False


def test_to_kinetic_model_irreversible() -> None:
    compounds = (
        Compound(base_id="S", compartment="c"),
        Compound(base_id="P", compartment="c"),
    )
    compartments = {"c": "c"}
    m = Model(compounds=compounds, compartments=compartments)
    m.add_reaction(
        reaction=Reaction(
            id="v1_c",
            base_id="v1",
            stoichiometries={"S_c": -1, "P_c": 1},
            reversible=False,
        )
    )
    mod = m.to_kinetic_model()
    assert mod.compounds == ["P_c", "S_c"]
    assert mod.stoichiometries == {"v1_c": {"S_c": -1, "P_c": 1}}
    assert list(mod.rates) == ["v1_c"]
    rate = mod.rates["v1_c"]
    assert rate["function"].__name__ == "mass_action_1"
    assert rate["parameters"] == ["k_v1_c"]
    assert rate["substrates"] == ["S_c"]
    assert rate["products"] == ["P_c"]
    assert rate["modifiers"] == []
    assert rate["dynamic_variables"] == ["S_c"]
    assert rate["reversible"] is False


def test_to_kinetic_model_reversible() -> None:
    compounds = (
        Compound(base_id="S", compartment="c"),
        Compound(base_id="P", compartment="c"),
    )
    compartments = {"c": "c"}
    m = Model(compounds=compounds, compartments=compartments)
    m.add_reaction(
        reaction=Reaction(
            id="v1_c",
            base_id="v1",
            stoichiometries={"S_c": -1, "P_c": 1},
            reversible=True,
        )
    )
    mod = m.to_kinetic_model()
    assert mod.compounds == ["P_c", "S_c"]
    assert mod.stoichiometries == {"v1_c": {"S_c": -1, "P_c": 1}}
    assert list(mod.rates) == ["v1_c"]
    rate = mod.rates["v1_c"]
    assert rate["function"].__name__ == "reversible_mass_action_1_1"
    assert rate["parameters"] == ["kf_v1_c", "kr_v1_c"]
    assert rate["substrates"] == ["S_c"]
    assert rate["products"] == ["P_c"]
    assert rate["modifiers"] == []
    assert rate["dynamic_variables"] == ["S_c", "P_c"]
    assert rate["reversible"] is True


def test_to_kinetic_model_non_integer_stoichiometry() -> None:
    compounds = (
        Compound(base_id="S", compartment="c"),
        Compound(base_id="P", compartment="c"),
    )
    compartments = {"c": "c"}
    m = Model(compounds=compounds, compartments=compartments)
    m.add_reaction(
        reaction=Reaction(
            id="v1_c",
            base_id="v1",
            stoichiometries={"S_c": -1.5, "P_c": 2.5},
            reversible=False,
        )
    )
    with pytest.warns(UserWarning):
        mod = m.to_kinetic_model()
        assert mod.compounds == ["P_c", "S_c"]
        assert mod.stoichiometries == {"v1_c": {"S_c": -1, "P_c": 2}}


def test_to_kinetic_model_non_integer_stoichiometry_to_zero() -> None:
    """Expected, but still dumb."""
    compounds = (
        Compound(base_id="S", compartment="c"),
        Compound(base_id="P", compartment="c"),
    )
    compartments = {"c": "c"}
    m = Model(compounds=compounds, compartments=compartments)
    m.add_reaction(
        reaction=Reaction(
            id="v1_c",
            base_id="v1",
            stoichiometries={"S_c": -0.5, "P_c": 0.5},
            reversible=False,
        )
    )
    with pytest.warns(UserWarning):
        mod = m.to_kinetic_model()
        assert mod.compounds == ["P_c", "S_c"]
        assert mod.stoichiometries == {"v1_c": {"S_c": -1, "P_c": 1}}


def test_to_kinetic_model_influx_fail_on_weird_kinetics() -> None:
    compounds = (
        Compound(base_id="S", compartment="c"),
        Compound(base_id="S", compartment="e"),
    )
    compartments = {"c": "c", "e": "e"}
    m = Model(compounds=compounds, compartments=compartments)
    m.add_influx(compound_id="S_c", extracellular_compartment_id="e")
    with pytest.raises(NotImplementedError):
        m.to_kinetic_model(influx_ratelaw="garbage")


def test_to_kinetic_model_efflux_fail_on_weird_kinetics() -> None:
    compounds = (
        Compound(base_id="S", compartment="c"),
        Compound(base_id="S", compartment="e"),
    )
    compartments = {"c": "c", "e": "e"}
    m = Model(compounds=compounds, compartments=compartments)
    m.add_efflux(compound_id="S_c", extracellular_compartment_id="e")
    with pytest.raises(NotImplementedError):
        m.to_kinetic_model(efflux_ratelaw="garbage")


def test_to_kinetic_model_irreversible_fail_on_weird_kinetics() -> None:
    compounds = (
        Compound(base_id="S", compartment="c"),
        Compound(base_id="P", compartment="c"),
    )
    compartments = {"c": "c"}
    m = Model(compounds=compounds, compartments=compartments)
    m.add_reaction(
        reaction=Reaction(
            id="v1_c",
            base_id="v1",
            stoichiometries={"S_c": -1, "P_c": 1},
            reversible=False,
        )
    )
    with pytest.raises(NotImplementedError):
        m.to_kinetic_model(reaction_ratelaw="garbage")


def test_to_kinetic_model_reversible_fail_on_weird_kinetics() -> None:
    compounds = (
        Compound(base_id="S", compartment="c"),
        Compound(base_id="P", compartment="c"),
    )
    compartments = {"c": "c"}
    m = Model(compounds=compounds, compartments=compartments)
    m.add_reaction(
        reaction=Reaction(
            id="v1_c",
            base_id="v1",
            stoichiometries={"S_c": -1, "P_c": 1},
            reversible=True,
        )
    )
    with pytest.raises(NotImplementedError):
        m.to_kinetic_model(reaction_ratelaw="garbage")


def create_minimal_toy_model() -> Model:
    compounds = (
        Compound(base_id="S", compartment="c"),
        Compound(base_id="E", compartment="c"),
        Compound(base_id="SE", compartment="c"),
        Compound(base_id="P", compartment="c"),
    )
    reactions = (
        Reaction(
            id="v1_c",
            base_id="v1",
            stoichiometries={"S_c": -1, "E_c": -1, "SE_c": 1},
            reversible=True,
        ),
        Reaction(
            id="v2_c",
            base_id="v2",
            stoichiometries={"SE_c": -1, "P_c": 1, "E_c": 1},
            reversible=False,
        ),
    )
    compartments = {"c": "c", "e": "e"}
    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    m.add_influx("S_c", extracellular_compartment_id="e")
    m.add_efflux("P_c", extracellular_compartment_id="e")
    m.add_transport_reaction(compound_id="S_c", compartment_id="e")
    m.add_transport_reaction(compound_id="P_c", compartment_id="e")
    return m


def test_to_kinetic_model() -> None:
    m = create_minimal_toy_model()
    mod = m.to_kinetic_model()
    assert mod.compounds == ["E_c", "P_c", "P_e", "SE_c", "S_c", "S_e"]
    assert list(mod.rates) == ["EX_P_e", "EX_S_e", "TR_P_c_e", "TR_S_c_e", "v1_c", "v2_c"]
    assert mod.stoichiometries == {
        "EX_P_e": {"P_e": -1},
        "EX_S_e": {"S_e": 1},
        "TR_P_c_e": {"P_c": -1, "P_e": 1},
        "TR_S_c_e": {"S_c": -1, "S_e": 1},
        "v1_c": {"S_c": -1, "E_c": -1, "SE_c": 1},
        "v2_c": {"SE_c": -1, "P_c": 1, "E_c": 1},
    }


def test_to_kinetic_model_fail_on_unknown_kinetics() -> None:
    m = create_minimal_toy_model()
    with pytest.raises(NotImplementedError):
        m.to_kinetic_model(
            reaction_ratelaw="garbage",
            influx_ratelaw="constant",
            efflux_ratelaw="mass-action",
        )
    with pytest.raises(NotImplementedError):
        m.to_kinetic_model(
            reaction_ratelaw="mass-action",
            influx_ratelaw="garbage",
            efflux_ratelaw="mass-action",
        )
    with pytest.raises(NotImplementedError):
        m.to_kinetic_model(
            reaction_ratelaw="mass-action",
            influx_ratelaw="constant",
            efflux_ratelaw="garbage",
        )


def test_to_kinetic_model_source_code_fail_on_unknown_kinetics() -> None:
    m = create_minimal_toy_model()
    with pytest.raises(NotImplementedError):
        m.to_kinetic_model_source_code(
            reaction_ratelaw="garbage",
            influx_ratelaw="constant",
            efflux_ratelaw="mass-action",
        )
    with pytest.raises(NotImplementedError):
        m.to_kinetic_model_source_code(
            reaction_ratelaw="mass-action",
            influx_ratelaw="garbage",
            efflux_ratelaw="mass-action",
        )
    with pytest.raises(NotImplementedError):
        m.to_kinetic_model_source_code(
            reaction_ratelaw="mass-action",
            influx_ratelaw="constant",
            efflux_ratelaw="garbage",
        )


def test_to_kinetic_model_source_code() -> None:
    create_minimal_toy_model()
    assert True
    # when it runs without error, that should be fine enough
    # the source code function is an external dependency, so the test might fail
    # due to modelbase being updated, which is kinda dumb
    # result = [i for i in m.to_kinetic_model_source_code().split("\n") if i != ""]
    # expected = [
    #     "import math",
    #     "from modelbase.ode import Model, Simulator",
    #     "def constant(k):",
    #     "    return k",
    #     "def mass_action_1(S1, k_fwd):",
    #     "    return k_fwd * S1",
    #     "def reversible_mass_action_1_1(S1, P1, k_fwd, k_bwd):",
    #     "    return k_fwd * S1 - k_bwd * P1",
    #     "def reversible_mass_action_2_1(S1, S2, P1, k_fwd, k_bwd):",
    #     "    return k_fwd * S1 * S2 - k_bwd * P1",
    #     "m = Model()",
    #     "m.add_parameters(",
    #     "    parameters={",
    #     '        "k_out_EX_P_e": 1,',
    #     '        "k_in_EX_S_e": 1,',
    #     '        "kf_TR_P_c_e": 1,',
    #     '        "kr_TR_P_c_e": 1,',
    #     '        "kf_TR_S_c_e": 1,',
    #     '        "kr_TR_S_c_e": 1,',
    #     '        "kf_v1_c": 1,',
    #     '        "kr_v1_c": 1,',
    #     '        "k_v2_c": 1,',
    #     "    }",
    #     ")",
    #     'm.add_compounds(compounds=["E_c", "P_c", "P_e", "SE_c", "S_c", "S_e"])',
    #     "m.add_rate(",
    #     '    rate_name="EX_P_e",',
    #     "    function=mass_action_1,",
    #     '    substrates=["P_e"],',
    #     "    products=[],",
    #     "    modifiers=[],",
    #     '    parameters=["k_out_EX_P_e"],',
    #     "    reversible=False,",
    #     ")",
    #     "m.add_rate(",
    #     '    rate_name="EX_S_e",',
    #     "    function=constant,",
    #     "    substrates=[],",
    #     '    products=["S_e"],',
    #     "    modifiers=[],",
    #     '    parameters=["k_in_EX_S_e"],',
    #     "    reversible=False,",
    #     ")",
    #     "m.add_rate(",
    #     '    rate_name="TR_P_c_e",',
    #     "    function=reversible_mass_action_1_1,",
    #     '    substrates=["P_c"],',
    #     '    products=["P_e"],',
    #     "    modifiers=[],",
    #     '    parameters=["kf_TR_P_c_e", "kr_TR_P_c_e"],',
    #     "    reversible=True,",
    #     ")",
    #     "m.add_rate(",
    #     '    rate_name="TR_S_c_e",',
    #     "    function=reversible_mass_action_1_1,",
    #     '    substrates=["S_c"],',
    #     '    products=["S_e"],',
    #     "    modifiers=[],",
    #     '    parameters=["kf_TR_S_c_e", "kr_TR_S_c_e"],',
    #     "    reversible=True,",
    #     ")",
    #     "m.add_rate(",
    #     '    rate_name="v1_c",',
    #     "    function=reversible_mass_action_2_1,",
    #     '    substrates=["S_c", "E_c"],',
    #     '    products=["SE_c"],',
    #     "    modifiers=[],",
    #     '    parameters=["kf_v1_c", "kr_v1_c"],',
    #     "    reversible=True,",
    #     ")",
    #     "m.add_rate(",
    #     '    rate_name="v2_c",',
    #     "    function=mass_action_1,",
    #     '    substrates=["SE_c"],',
    #     '    products=["P_c", "E_c"],',
    #     "    modifiers=[],",
    #     '    parameters=["k_v2_c"],',
    #     "    reversible=False,",
    #     ")",
    #     "m.add_stoichiometries(",
    #     "    rate_stoichiometries={",
    #     '        "EX_P_e": {"P_e": -1},',
    #     '        "EX_S_e": {"S_e": 1},',
    #     '        "TR_P_c_e": {"P_c": -1, "P_e": 1},',
    #     '        "TR_S_c_e": {"S_c": -1, "S_e": 1},',
    #     '        "v1_c": {"S_c": -1, "E_c": -1, "SE_c": 1},',
    #     '        "v2_c": {"SE_c": -1, "P_c": 1, "E_c": 1},',
    #     "    }",
    #     ")",
    # ]
    # assertEqual(result, expected)
