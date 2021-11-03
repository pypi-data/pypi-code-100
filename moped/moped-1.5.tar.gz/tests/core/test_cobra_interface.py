from moped import Compound, Model, Reaction


def create_minimal_toy_model() -> Model:
    compounds = (
        Compound(base_id="S", compartment="CYTOSOL", formula={"C": 1}, charge=0),
        Compound(base_id="E", compartment="CYTOSOL", formula={"E": 1}, charge=0),
        Compound(base_id="SE", compartment="CYTOSOL", formula={"C": 1, "E": 1}, charge=0),
        Compound(base_id="P", compartment="CYTOSOL", formula={"C": 1}, charge=0),
    )
    reactions = (
        Reaction(
            id="v1_c",
            base_id="v1",
            stoichiometries={"S_c": -1, "E_c": -1, "SE_c": 1},
            bounds=(-10, 1000),
            sequences={"MONOMER-001": "GATC"},
        ),
        Reaction(
            id="v2_c",
            base_id="v2",
            stoichiometries={"SE_c": -1, "P_c": 1, "E_c": 1},
            bounds=(0, 1000),
            sequences={"MONOMER-002": "GATC"},
        ),
    )
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p", "EXTRACELLULAR": "e"}
    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    m.add_transport_reaction(compound_id="S_c", compartment_id="EXTRACELLULAR", bounds=(-1000, 0))
    m.add_influx("S_c", extracellular_compartment_id="EXTRACELLULAR")
    m.add_transport_reaction(compound_id="P_c", compartment_id="EXTRACELLULAR", bounds=(0, 1000))
    m.add_efflux("P_c", extracellular_compartment_id="EXTRACELLULAR")
    m.set_objective({"v1_c": 1, "v2_c": 1})
    return m.copy()


def test_to_cobra() -> None:
    m = create_minimal_toy_model()
    cm = m.to_cobra()
    assert list(m.compounds) == [i.id for i in cm.metabolites]
    assert list(m.reactions) == [i.id for i in cm.reactions]
    assert m.objective == {
        rec.id: rec.objective_coefficient for rec in cm.reactions if rec.objective_coefficient != 0
    }


def test_cobra_metabolite_compartment() -> None:
    m = create_minimal_toy_model()
    cm = m.to_cobra()
    for metabolite in cm.metabolites:
        assert m.compartments[m.compounds[metabolite.id].compartment] == metabolite.compartment


def test_cobra_metabolite_in_reaction() -> None:
    m = create_minimal_toy_model()
    cm = m.to_cobra()
    for metabolite in cm.metabolites:
        assert sorted(m.compounds[metabolite.id].in_reaction) == sorted([i.id for i in metabolite.reactions])


def test_cobra_metabolite_charge() -> None:
    m = create_minimal_toy_model()
    cm = m.to_cobra()
    for metabolite in cm.metabolites:
        assert m.compounds[metabolite.id].charge == metabolite.charge


def test_cobra_metabolite_formula() -> None:
    m = create_minimal_toy_model()
    cm = m.to_cobra()
    for metabolite in cm.metabolites:
        assert (
            "".join([k + str(v) for k, v in m.compounds[metabolite.id].formula.items()]) == metabolite.formula
        )


def test_cobra_reaction_stoichiometries() -> None:
    m = create_minimal_toy_model()
    cm = m.to_cobra()
    for reaction in cm.reactions:
        assert m.reactions[reaction.id].stoichiometries == {k.id: v for k, v in reaction.metabolites.items()}


def test_cobra_reaction_bounds() -> None:
    m = create_minimal_toy_model()
    cm = m.to_cobra()
    for reaction in cm.reactions:
        assert m.reactions[reaction.id].bounds == reaction.bounds


def test_cobra_reaction_reversibility() -> None:
    m = create_minimal_toy_model()
    cm = m.to_cobra()
    for reaction in cm.reactions:
        assert m.reactions[reaction.id].reversible == reaction.reversibility


def test_back_and_forth() -> None:
    model = create_minimal_toy_model()
    cobra_model = model.to_cobra()
    model_re = Model()
    model_re.read_from_cobra(cobra_model)
    assert model.compounds == model_re.compounds
    for compound_id in model.compounds:
        compound = model.compounds[compound_id]
        compound_re = model_re.compounds[compound_id]

        assert compound.base_id == compound_re.base_id
        assert compound.id == compound_re.id
        assert compound.compartment == compound_re.compartment
        assert compound.formula == compound_re.formula
        assert compound.in_reaction == compound_re.in_reaction

    assert model.reactions == model_re.reactions
    for reaction_id in model.reactions:
        reaction = model.reactions[reaction_id]
        reaction_re = model_re.reactions[reaction_id]

        assert reaction.id == reaction_re.id
        assert reaction.base_id == reaction_re.base_id
        assert reaction.stoichiometries == reaction_re.stoichiometries
        assert reaction.bounds == reaction_re.bounds
        # assert reaction.sequences == reaction_re.sequences


def test_get_producing_reactions() -> None:
    model = create_minimal_toy_model()
    cobra_model = model.to_cobra()
    cobra_solution = cobra_model.optimize()
    assert model.get_producing_reactions(cobra_solution=cobra_solution, compound_id="S_c") == {
        "TR_S_c_e": 1000.0
    }
    assert model.get_producing_reactions(cobra_solution=cobra_solution, compound_id="E_c") == {"v2_c": 1000.0}
    assert model.get_producing_reactions(cobra_solution=cobra_solution, compound_id="SE_c") == {
        "v1_c": 1000.0
    }
    assert model.get_producing_reactions(cobra_solution=cobra_solution, compound_id="P_c") == {"v2_c": 1000.0}
    assert model.get_producing_reactions(cobra_solution=cobra_solution, compound_id="S_e") == {
        "EX_S_e": 1000.0
    }
    assert model.get_producing_reactions(cobra_solution=cobra_solution, compound_id="P_e") == {
        "TR_P_c_e": 1000.0
    }


def test_get_consuming_reactions() -> None:
    model = create_minimal_toy_model()
    cobra_model = model.to_cobra()
    cobra_solution = cobra_model.optimize()
    assert model.get_consuming_reactions(cobra_solution=cobra_solution, compound_id="S_c") == {"v1_c": 1000.0}
    assert model.get_consuming_reactions(cobra_solution=cobra_solution, compound_id="E_c") == {"v1_c": 1000.0}
    assert model.get_consuming_reactions(cobra_solution=cobra_solution, compound_id="SE_c") == {
        "v2_c": 1000.0
    }
    assert model.get_consuming_reactions(cobra_solution=cobra_solution, compound_id="P_c") == {
        "TR_P_c_e": 1000.0
    }
    assert model.get_consuming_reactions(cobra_solution=cobra_solution, compound_id="S_e") == {
        "TR_S_c_e": 1000.0
    }
    assert model.get_consuming_reactions(cobra_solution=cobra_solution, compound_id="P_e") == {
        "EX_P_e": 1000.0
    }


def test_get_influx_reactions() -> None:
    m = create_minimal_toy_model()
    cobra_model = m.to_cobra()
    cobra_solution = cobra_model.optimize()

    res = m.get_influx_reactions(cobra_solution=cobra_solution, sort_result=False)
    assert res["EX_P_e"] == 1000.0
    assert list(res.keys()) == ["EX_P_e"]

    res = m.get_influx_reactions(cobra_solution=cobra_solution, sort_result=True)
    assert res["EX_P_e"] == 1000.0
    assert list(res.keys()) == ["EX_P_e"]


def test_get_efflux_reactions() -> None:
    m = create_minimal_toy_model()
    cobra_model = m.to_cobra()
    cobra_solution = cobra_model.optimize()
    res = m.get_efflux_reactions(cobra_solution=cobra_solution, sort_result=False)
    assert res["EX_S_e"] == -1000.0
    assert list(res.keys()) == ["EX_S_e"]

    res = m.get_efflux_reactions(cobra_solution=cobra_solution, sort_result=True)
    assert res["EX_S_e"] == -1000.0
    assert list(res.keys()) == ["EX_S_e"]
