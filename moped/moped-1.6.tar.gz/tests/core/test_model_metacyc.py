from moped import Compound, Model, Reaction


def test_move_electron_transport_cofactors_to_cytosol() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p"}
    compounds = (
        Compound(base_id="ATP", compartment="CYTOSOL"),
        Compound(base_id="ATP", compartment="PERIPLASM"),
        Compound(base_id="ADP", compartment="CYTOSOL"),
        Compound(base_id="ADP", compartment="PERIPLASM"),
        Compound(base_id="cpd1", compartment="CYTOSOL"),
        Compound(base_id="cpd1", compartment="PERIPLASM"),
        Compound(base_id="cpd2", compartment="CYTOSOL"),
        Compound(base_id="cpd2", compartment="PERIPLASM"),
    )
    reactions = (
        Reaction(
            id="transporter",
            stoichiometries={"ATP_p": -1, "cpd1_p": -1, "ADP_p": 1, "cpd1_c": 1},
            transmembrane=True,
            compartment=("CYTOSOL", "PERIPLASM"),
            types=["Electron-Transfer-Reactions"],
        ),
        Reaction(
            id="only-cofactors-periplasm",
            stoichiometries={"ATP_p": -1, "cpd1_c": -1, "ADP_p": 1, "cpd2_c": 1},
            transmembrane=True,
            compartment=("CYTOSOL", "PERIPLASM"),
            types=["Electron-Transfer-Reactions"],
        ),
        Reaction(
            id="all-periplasm",
            stoichiometries={"ATP_p": -1, "cpd1_p": -1, "ADP_p": 1, "cpd2_p": 1},
            transmembrane=True,
            compartment=("PERIPLASM",),
            types=["Electron-Transfer-Reactions"],
        ),
    )
    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    m._move_electron_transport_cofactors_to_cytosol()

    assert m.reactions["transporter_c_p"].id == "transporter_c_p"
    assert m.reactions["transporter_c_p"].stoichiometries == {
        "cpd1_p": -1,
        "cpd1_c": 1,
        "ATP_c": -1,
        "ADP_c": 1,
    }
    assert m.reactions["transporter_c_p"].transmembrane is True
    assert m.reactions["transporter_c_p"].compartment == ("CYTOSOL", "PERIPLASM")

    assert m.reactions["only-cofactors-periplasm_c"].id == "only-cofactors-periplasm_c"
    assert m.reactions["only-cofactors-periplasm_c"].stoichiometries == {
        "cpd1_c": -1,
        "cpd2_c": 1,
        "ATP_c": -1,
        "ADP_c": 1,
    }
    assert m.reactions["only-cofactors-periplasm_c"].transmembrane is False
    assert m.reactions["only-cofactors-periplasm_c"].compartment == "CYTOSOL"

    assert m.reactions["all-periplasm_c_p"].id == "all-periplasm_c_p"
    assert m.reactions["all-periplasm_c_p"].stoichiometries == {
        "cpd1_p": -1,
        "cpd2_p": 1,
        "ATP_c": -1,
        "ADP_c": 1,
    }
    assert m.reactions["all-periplasm_c_p"].transmembrane is True
    assert m.reactions["all-periplasm_c_p"].compartment == ("CYTOSOL", "PERIPLASM")


def test_repair_photosynthesis_reactions() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p"}

    compounds = (
        Compound(base_id="Light", compartment="CYTOSOL"),
        Compound(base_id="WATER", compartment="CYTOSOL"),
        Compound(base_id="PLASTOQUINONE-9", compartment="CYTOSOL"),
        Compound(base_id="OXYGEN-MOLECULE", compartment="CYTOSOL"),
        Compound(base_id="CPD-12829", compartment="CYTOSOL"),
        Compound(base_id="PROTON", compartment="PERIPLASM"),
        Compound(base_id="PROTON", compartment="CYTOSOL"),
        Compound(base_id="Oxidized-Plastocyanins", compartment="CYTOSOL"),
        Compound(base_id="CPD-12829", compartment="CYTOSOL"),
        Compound(base_id="Plastocyanin-Reduced", compartment="CYTOSOL"),
    )
    reactions = (
        Reaction(
            id="PSII-RXN__var__0_c_p",
            base_id="PSII-RXN",
            stoichiometries={
                "Light_c": -1,
                "WATER_c": -2.0,
                "PLASTOQUINONE-9_c": -2.0,
                "OXYGEN-MOLECULE_c": 1,
                "CPD-12829_c": 2.0,
                "PROTON_c": 4.0,
                "PROTON_p": -4.0,
            },
            compartment=("CYTOSOL", "PERIPLASM"),
            pathways={"PWY-101"},
            transmembrane=True,
            _var=0,
        ),
        Reaction(
            id="PLASTOQUINOL--PLASTOCYANIN-REDUCTASE-RXN__var__0_c_p",
            base_id="PLASTOQUINOL--PLASTOCYANIN-REDUCTASE-RXN",
            stoichiometries={
                "Oxidized-Plastocyanins_c": -2.0,
                "CPD-12829_c": -1,
                "Plastocyanin-Reduced_c": 2.0,
                "PLASTOQUINONE-9_c": 1,
                "PROTON_c": 4.0,
                "PROTON_p": -2.0,
            },
            compartment=("CYTOSOL", "PERIPLASM"),
            pathways={"PWY-101"},
            transmembrane=True,
            _var=0,
        ),
    )

    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    m._repair_photosynthesis_reactions()
    assert m.reactions["PSII-RXN__var__0_c_p"].stoichiometries == {
        "Light_c": -1,
        "WATER_c": -2.0,
        "PLASTOQUINONE-9_c": -2.0,
        "OXYGEN-MOLECULE_c": 1,
        "CPD-12829_c": 2.0,
        "PROTON_p": 4.0,
        "PROTON_c": -4.0,
    }
    assert m.reactions["PLASTOQUINOL--PLASTOCYANIN-REDUCTASE-RXN__var__0_c_p"].stoichiometries == {
        "Oxidized-Plastocyanins_c": -2.0,
        "CPD-12829_c": -1,
        "Plastocyanin-Reduced_c": 2.0,
        "PLASTOQUINONE-9_c": 1,
        "PROTON_p": 4.0,
        "PROTON_c": -2.0,
    }


def test_repair_photosynthesis_reactions_isolation() -> None:
    compartments = {"CYTOSOL": "c", "PERIPLASM": "p"}

    compounds = (
        Compound(base_id="PROTON", compartment="PERIPLASM"),
        Compound(base_id="PROTON", compartment="CYTOSOL"),
    )
    reactions = (
        Reaction(
            id="rxn1",
            stoichiometries={
                "PROTON_c": -1.0,
                "PROTON_p": 2.0,
            },
            compartment=("CYTOSOL", "PERIPLASM"),
            pathways={"PWY-101"},
            transmembrane=True,
        ),
        Reaction(
            id="rxn2",
            stoichiometries={
                "PROTON_p": 2.0,
            },
            compartment=("CYTOSOL", "PERIPLASM"),
            pathways={"PWY-101"},
            transmembrane=True,
        ),
        Reaction(
            id="rxn3",
            stoichiometries={
                "PROTON_c": -1.0,
            },
            compartment=("CYTOSOL", "PERIPLASM"),
            pathways={"PWY-101"},
            transmembrane=True,
        ),
    )

    m = Model(compounds=compounds, reactions=reactions, compartments=compartments)
    m._repair_photosynthesis_reactions()
    assert m.reactions["rxn1_c_p"].stoichiometries == {"PROTON_p": -1.0, "PROTON_c": 2.0}
    assert m.reactions["rxn2_c"].stoichiometries == {"PROTON_c": 2.0}
    assert m.reactions["rxn3_p"].stoichiometries == {"PROTON_p": -1.0}
