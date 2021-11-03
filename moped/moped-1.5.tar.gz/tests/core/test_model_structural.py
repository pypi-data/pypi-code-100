from moped import Compound, Model

import pytest


def test_get_biomass_template() -> None:
    expected = {
        "TRP_c": -0.055234,
        "GLT_c": -0.255712,
        "MALONYL-COA_c": -3.1e-05,
        "GTP_c": -0.209121,
        "NADP_c": -0.000112,
        "WATER_c": -48.752916,
        "LEU_c": -0.437778,
        "ASN_c": -0.234232,
        "L-ASPARTATE_c": -0.234232,
        "L-ALPHA-ALANINE_c": -0.499149,
        "ARG_c": -0.28742,
        "TYR_c": -0.133993,
        "THR_c": -0.246506,
        "CTP_c": -0.129799,
        "SER_c": -0.209684,
        "ATP_c": -54.119975,
        "GLN_c": -0.255712,
        "MET_c": -0.149336,
        "LYS_c": -0.333448,
        "ACETYL-COA_c": -0.000279,
        "CYS_c": -0.088988,
        "HIS_c": -0.092056,
        "VAL_c": -0.411184,
        "UTP_c": -0.140101,
        "ILE_c": -0.282306,
        "NADPH_c": -0.000335,
        "NAD_c": -0.001787,
        "PRO_c": -0.214798,
        "PHE_c": -0.180021,
        "GLY_c": -0.595297,
        "Pi_c": 53.945874,
        "PROTON_c": 51.472,
        "ADP_c": 53.95,
    }
    m = Model()
    biomass = m.get_biomass_template(organism="ecoli")
    assert biomass == expected


def test_get_biomass_template_fail_on_missing() -> None:
    m = Model()
    with pytest.raises(KeyError):
        m.get_biomass_template(organism="garbage")


def test_add_cofactor_pair() -> None:
    m = Model()
    m.add_compartment(compartment_id="c", compartment_suffix="c")
    m.add_compound(Compound(base_id="ATP", compartment="c"))
    m.add_compound(Compound(base_id="ADP", compartment="c"))
    m.add_cofactor_pair(strong_cofactor_base_id="ATP", weak_cofactor_base_id="ADP")
    assert m.cofactor_pairs == {"ATP_c": "ADP_c"}


def test_add_cofactor_pair_multiple_compartments() -> None:
    m = Model()
    m.add_compartment(compartment_id="c", compartment_suffix="c")
    m.add_compartment(compartment_id="e", compartment_suffix="e")
    m.add_compound(Compound(base_id="ATP", compartment="c"))
    m.add_compound(Compound(base_id="ADP", compartment="c"))
    m.add_compound(Compound(base_id="ATP", compartment="e"))
    m.add_compound(Compound(base_id="ADP", compartment="e"))
    m.add_cofactor_pair(strong_cofactor_base_id="ATP", weak_cofactor_base_id="ADP")
    assert m.cofactor_pairs == {"ATP_c": "ADP_c", "ATP_e": "ADP_e"}


def test_get_weak_cofactors() -> None:
    m = Model()
    m.add_compartment(compartment_id="c", compartment_suffix="c")
    m.add_compartment(compartment_id="e", compartment_suffix="e")
    m.add_compound(Compound(base_id="ATP", compartment="c"))
    m.add_compound(Compound(base_id="ADP", compartment="c"))
    m.add_compound(Compound(base_id="ATP", compartment="e"))
    m.add_compound(Compound(base_id="ADP", compartment="e"))
    m.add_cofactor_pair(strong_cofactor_base_id="ATP", weak_cofactor_base_id="ADP")
    assert set(m.get_weak_cofactors()) == set(["ADP_c", "ADP_e"])


def test_get_strong_cofactors() -> None:

    m = Model()
    m.add_compartment(compartment_id="c", compartment_suffix="c")
    m.add_compartment(compartment_id="e", compartment_suffix="e")
    m.add_compound(Compound(base_id="ATP", compartment="c"))
    m.add_compound(Compound(base_id="ADP", compartment="c"))
    m.add_compound(Compound(base_id="ATP", compartment="e"))
    m.add_compound(Compound(base_id="ADP", compartment="e"))
    m.add_cofactor_pair(strong_cofactor_base_id="ATP", weak_cofactor_base_id="ADP")
    assert set(m.get_strong_cofactors()) == set(["ATP_c", "ATP_e"])


def test_get_strong_cofactor_duplications() -> None:
    m = Model()
    m.add_compartment(compartment_id="c", compartment_suffix="c")
    m.add_compartment(compartment_id="e", compartment_suffix="e")
    m.add_compound(Compound(base_id="ATP", compartment="c"))
    m.add_compound(Compound(base_id="ADP", compartment="c"))
    m.add_compound(Compound(base_id="ATP", compartment="e"))
    m.add_compound(Compound(base_id="ADP", compartment="e"))
    m.add_cofactor_pair(strong_cofactor_base_id="ATP", weak_cofactor_base_id="ADP")
    assert set(m.get_strong_cofactor_duplications()) == set(["ATP_c__cof__", "ATP_e__cof__"])


def test_add_minimal_seed() -> None:
    m = Model()
    m.add_minimal_seed(compound_ids=("a", "b", "c"))
    assert m.minimal_seed == {"a", "b", "c"}


def test_get_minimal_seed() -> None:
    m = Model()
    m.add_minimal_seed(compound_ids=("a", "b", "c"))
    assert m.get_minimal_seed(carbon_source_id="GLC") == {"GLC", "a", "b", "c"}


def test_get_minimal_seed_fail_without_supplied() -> None:
    m = Model()
    with pytest.raises(ValueError):
        m.get_minimal_seed(carbon_source_id="GLC")
