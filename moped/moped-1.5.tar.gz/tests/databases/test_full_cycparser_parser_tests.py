from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple
from unittest import mock

from moped.core.model import Model
from moped.databases.cyc import (
    CompoundParser,
    ParseCompound,
    ParseReaction,
    ReactionParser,
    Repairer,
)

import pytest

COMPARTMENT_MAP = {
    "CYTOSOL": "CYTOSOL",
    "IN": "CYTOSOL",
    "UNKNOWN-SPACE": "CYTOSOL",
    "SIDE-1": "CYTOSOL",
    "SIDE-2": "EXTRACELLULAR",
    "EXTRACELLULAR": "EXTRACELLULAR",
    "CHL-THY-MEM": "PERIPLASM",
    "CHLOR-STR": "CYTOSOL",
    "CHROM-STR": "CYTOSOL",
    "GOLGI-LUM": "CYTOSOL",
    "LYS-LUM": "CYTOSOL",
    "MIT-IM-SPC": "CYTOSOL",
    "MIT-IMEM": "PERIPLASM",
    "MIT-LUM": "CYTOSOL",
    "OUTER-MEM": "PERIPLASM",
    "PERI-BAC": "PERIPLASM",
    "PERI-BAC-GN": "PERIPLASM",
    "PERIPLASM": "PERIPLASM",
    "PEROX-LUM": "CYTOSOL",
    "PLASMA-MEM": "PERIPLASM",
    "PLAST-IMEM": "PERIPLASM",
    "PLASTID-STR": "PERIPLASM",
    "PM-ANIMAL": "PERIPLASM",
    "PM-BAC-ACT": "PERIPLASM",
    "PM-BAC-NEG": "PERIPLASM",
    "PM-BAC-POS": "PERIPLASM",
    "RGH-ER-LUM": "CYTOSOL",
    "RGH-ER-MEM": "PERIPLASM",
    "THY-LUM-CYA": "CYTOSOL",
    "VAC-LUM": "CYTOSOL",
    "VAC-MEM": "PERIPLASM",
    "VESICLE": "PERIPLASM",
    "OUT": "PERIPLASM",
}


def read_mock_compounds(file: List[str]) -> Tuple[Dict[str, ParseCompound], Dict[str, List[str]]]:
    with mock.patch(
        "moped.databases.cyc._open_file_and_remove_comments",
        mock.Mock(return_value=("", 0)),
    ):
        CP = CompoundParser(Path(""), {})
        CP.file = file
        return CP.parse()


def read_mock_reactions(file: List[str]) -> Dict[str, ParseReaction]:
    with mock.patch(
        "moped.databases.cyc._open_file_and_remove_comments",
        mock.Mock(return_value=("", 0)),
    ):
        RP = ReactionParser(Path(""), {})
        RP.file = file
        return RP.parse()


def mock_parsing(compound_file: List[str], reaction_file: List[str]) -> Model:
    """CAUTION: manual additions are set to {}"""
    parse_compounds, compound_types = read_mock_compounds(compound_file)
    parse_reactions = read_mock_reactions(reaction_file)
    r = Repairer(
        compounds=parse_compounds,
        compound_types=compound_types,
        reactions=parse_reactions,
        compartment_map=COMPARTMENT_MAP,
    )
    r.manual_additions = {}
    compounds, reactions, compartments = r.repair()
    with mock.patch("moped.core.model.Cyc", mock.Mock()) as MockCyc:
        MockCyc.return_value.parse.return_value = (
            compounds,
            reactions,
            compartments,
        )
        m = Model()
        m.read_from_pgdb(pgdb_path="")
    return m


def test_no_compartment_info() -> None:
    """We assume the cytosol as the default location"""
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "RIGHT - CPD2",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    assert m.compounds["CPD1_c"].compartment == "CYTOSOL"
    assert m.compounds["CPD2_c"].compartment == "CYTOSOL"
    assert not m.reactions["RXN_c"].transmembrane
    stoich = {"CPD1_c": -1, "CPD2_c": 1}
    assert m.reactions["RXN_c"].stoichiometries == stoich
    # Periplasm
    with pytest.raises(KeyError):
        m.compounds["CPD1_p"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_p"]
    with pytest.raises(KeyError):
        m.reactions["RXN_p"]
    # Extracellular
    with pytest.raises(KeyError):
        m.compounds["CPD1_e"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_e"]
    with pytest.raises(KeyError):
        m.reactions["RXN_e"]


def test_no_location_all_in() -> None:
    """We assume the cytosol as the default location"""
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-IN",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-IN",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    assert m.compounds["CPD1_c"].compartment == "CYTOSOL"
    assert m.compounds["CPD2_c"].compartment == "CYTOSOL"
    assert not m.reactions["RXN_c"].transmembrane
    stoich = {"CPD1_c": -1, "CPD2_c": 1}
    assert m.reactions["RXN_c"].stoichiometries == stoich
    # Periplasm
    with pytest.raises(KeyError):
        m.compounds["CPD1_p"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_p"]
    with pytest.raises(KeyError):
        m.reactions["RXN_p"]
    # Extracellular
    with pytest.raises(KeyError):
        m.compounds["CPD1_e"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_e"]
    with pytest.raises(KeyError):
        m.reactions["RXN_e"]


def test_single_location_cytosol_all_in() -> None:
    """This should stay in the cytosol"""
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-IN",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-IN",
        "RXN-LOCATIONS - CCO-CYTOSOL",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    assert m.compounds["CPD1_c"].compartment == "CYTOSOL"
    assert m.compounds["CPD2_c"].compartment == "CYTOSOL"
    assert not m.reactions["RXN_c"].transmembrane
    assert m.reactions["RXN_c"].stoichiometries == {"CPD1_c": -1, "CPD2_c": 1}
    # Periplasm
    with pytest.raises(KeyError):
        m.compounds["CPD1_p"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_p"]
    with pytest.raises(KeyError):
        m.reactions["RXN_p"]
    # Extracellular
    with pytest.raises(KeyError):
        m.compounds["CPD1_e"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_e"]
    with pytest.raises(KeyError):
        m.reactions["RXN_e"]


def test_single_location_periplasm_all_in() -> None:
    """This should only be in the periplasm"""
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-IN",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-IN",
        "RXN-LOCATIONS - CCO-PERIPLASM",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    with pytest.raises(KeyError):
        m.compounds["CPD1_c"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_c"]
    with pytest.raises(KeyError):
        m.reactions["RXN_c"]
    # Periplasm
    assert m.compounds["CPD1_p"].compartment == "PERIPLASM"
    assert m.compounds["CPD2_p"].compartment == "PERIPLASM"
    assert not m.reactions["RXN_p"].transmembrane
    stoich = {"CPD1_p": -1, "CPD2_p": 1}
    assert m.reactions["RXN_p"].stoichiometries == stoich
    # Extracellular
    with pytest.raises(KeyError):
        m.compounds["CPD1_e"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_e"]
    with pytest.raises(KeyError):
        m.reactions["RXN_e"]


def test_single_location_extracellular_all_in() -> None:
    """This should only be extracellular"""
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-IN",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-IN",
        "RXN-LOCATIONS - CCO-EXTRACELLULAR",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    with pytest.raises(KeyError):
        m.compounds["CPD1_c"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_c"]
    with pytest.raises(KeyError):
        m.reactions["RXN_c"]
    # Periplasm
    with pytest.raises(KeyError):
        m.compounds["CPD1_p"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_p"]
    with pytest.raises(KeyError):
        m.reactions["RXN_p"]
    # Extracellular
    assert m.compounds["CPD1_e"].compartment == "EXTRACELLULAR"
    assert m.compounds["CPD2_e"].compartment == "EXTRACELLULAR"
    assert not m.reactions["RXN_e"].transmembrane
    stoich = {"CPD1_e": -1, "CPD2_e": 1}
    assert m.reactions["RXN_e"].stoichiometries == stoich


def test_multiple_locations_cytosol_periplasm_all_in() -> None:
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-IN",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-IN",
        "RXN-LOCATIONS - CCO-CYTOSOL",
        "RXN-LOCATIONS - CCO-PERIPLASM",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    assert m.compounds["CPD1_c"].compartment == "CYTOSOL"
    assert m.compounds["CPD2_c"].compartment == "CYTOSOL"
    assert not m.reactions["RXN_c"].transmembrane
    stoich = {"CPD1_c": -1, "CPD2_c": 1}
    assert m.reactions["RXN_c"].stoichiometries == stoich
    # Periplasm
    assert m.compounds["CPD1_p"].compartment == "PERIPLASM"
    assert m.compounds["CPD2_p"].compartment == "PERIPLASM"
    assert not m.reactions["RXN_c"].transmembrane
    stoich = {"CPD1_p": -1, "CPD2_p": 1}
    assert m.reactions["RXN_p"].stoichiometries == stoich
    # Extracellular
    with pytest.raises(KeyError):
        m.compounds["CPD1_e"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_e"]
    with pytest.raises(KeyError):
        m.reactions["RXN_e"]


def test_multiple_locations_cytosol_extracellular_all_in() -> None:
    """This should give both cytosolic and extracellular"""
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-IN",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-IN",
        "RXN-LOCATIONS - CCO-CYTOSOL",
        "RXN-LOCATIONS - CCO-EXTRACELLULAR",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    assert m.compounds["CPD1_c"].compartment == "CYTOSOL"
    assert m.compounds["CPD2_c"].compartment == "CYTOSOL"
    assert not m.reactions["RXN_c"].transmembrane
    assert m.reactions["RXN_c"].stoichiometries == {"CPD1_c": -1, "CPD2_c": 1}
    # Periplasm
    with pytest.raises(KeyError):
        m.compounds["CPD1_p"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_p"]
    with pytest.raises(KeyError):
        m.reactions["RXN_p"]
    # Extracellular
    assert m.compounds["CPD1_e"].compartment == "EXTRACELLULAR"
    assert m.compounds["CPD2_e"].compartment == "EXTRACELLULAR"
    assert not m.reactions["RXN_e"].transmembrane
    stoich = {"CPD1_e": -1, "CPD2_e": 1}
    assert m.reactions["RXN_e"].stoichiometries == stoich


def test_fake_transmembrane_location_all_in() -> None:
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-IN",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-IN",
        "RXN-LOCATIONS - CCO-EXTRACELLULAR-CCO-CYTOSOL",  # out - in
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    assert m.compounds["CPD1_c"].compartment == "CYTOSOL"
    assert m.compounds["CPD2_c"].compartment == "CYTOSOL"
    assert not m.reactions["RXN_c"].transmembrane
    stoich = {"CPD1_c": -1, "CPD2_c": 1}
    assert m.reactions["RXN_c"].stoichiometries == stoich
    # Periplasm
    with pytest.raises(KeyError):
        m.compounds["CPD1_p"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_p"]
    with pytest.raises(KeyError):
        m.reactions["RXN_p"]
    # Extracellular
    with pytest.raises(KeyError):
        m.compounds["CPD1_e"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_e"]
    with pytest.raises(KeyError):
        m.reactions["RXN_e"]


def test_no_location_all_out() -> None:
    """We assume the extracellular as the default location"""
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-OUT",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-OUT",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    with pytest.raises(KeyError):
        m.compounds["CPD1_c"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_c"]
    with pytest.raises(KeyError):
        m.reactions["RXN_c"]
    # Periplasm
    with pytest.raises(KeyError):
        m.compounds["CPD1_p"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_p"]
    with pytest.raises(KeyError):
        m.reactions["RXN_p"]
    # Extracellular
    assert m.compounds["CPD1_e"].compartment == "EXTRACELLULAR"
    assert m.compounds["CPD2_e"].compartment == "EXTRACELLULAR"
    assert not m.reactions["RXN_e"].transmembrane
    stoich = {"CPD1_e": -1, "CPD2_e": 1}
    assert m.reactions["RXN_e"].stoichiometries == stoich


def test_single_location_cytosol_all_out() -> None:
    """This should stay in the cytosol"""
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-OUT",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-OUT",
        "RXN-LOCATIONS - CCO-CYTOSOL",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    assert m.compounds["CPD1_c"].compartment == "CYTOSOL"
    assert m.compounds["CPD2_c"].compartment == "CYTOSOL"
    assert not m.reactions["RXN_c"].transmembrane
    stoich = {"CPD1_c": -1, "CPD2_c": 1}
    assert m.reactions["RXN_c"].stoichiometries == stoich
    # Periplasm
    with pytest.raises(KeyError):
        m.compounds["CPD1_p"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_p"]
    with pytest.raises(KeyError):
        m.reactions["RXN_p"]
    # Extracellular
    with pytest.raises(KeyError):
        m.compounds["CPD1_e"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_e"]
    with pytest.raises(KeyError):
        m.reactions["RXN_e"]


def test_single_location_periplasm_all_out() -> None:
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-OUT",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-OUT",
        "RXN-LOCATIONS - CCO-PERIPLASM",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    with pytest.raises(KeyError):
        m.compounds["CPD1_c"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_c"]
    with pytest.raises(KeyError):
        m.reactions["RXN_c"]
    # Periplasm - the compounds will be created, but the reaction should not
    assert m.compounds["CPD1_p"].compartment == "PERIPLASM"
    assert m.compounds["CPD2_p"].compartment == "PERIPLASM"
    assert not m.reactions["RXN_p"].transmembrane
    stoich = {"CPD1_p": -1, "CPD2_p": 1}
    assert m.reactions["RXN_p"].stoichiometries == stoich
    # Extracellular
    with pytest.raises(KeyError):
        m.compounds["CPD1_e"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_e"]
    with pytest.raises(KeyError):
        m.reactions["RXN_e"]


def test_single_location_extracellular_all_out() -> None:
    """This should stay in the extracellular"""
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-OUT",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-OUT",
        "RXN-LOCATIONS - CCO-EXTRACELLULAR",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    with pytest.raises(KeyError):
        m.compounds["CPD1_c"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_c"]
    with pytest.raises(KeyError):
        m.reactions["RXN_c"]
    # Periplasm
    with pytest.raises(KeyError):
        m.compounds["CPD1_p"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_p"]
    with pytest.raises(KeyError):
        m.reactions["RXN_p"]
    # Extracellular
    assert m.compounds["CPD1_e"].compartment == "EXTRACELLULAR"
    assert m.compounds["CPD2_e"].compartment == "EXTRACELLULAR"
    assert not m.reactions["RXN_e"].transmembrane
    stoich = {"CPD1_e": -1, "CPD2_e": 1}
    assert m.reactions["RXN_e"].stoichiometries == stoich


def test_multiple_locations_cytosol_periplasm_all_out() -> None:
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-OUT",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-OUT",
        "RXN-LOCATIONS - CCO-CYTOSOL",
        "RXN-LOCATIONS - CCO-PERIPLASM",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    assert m.compounds["CPD1_c"].compartment == "CYTOSOL"
    assert m.compounds["CPD2_c"].compartment == "CYTOSOL"
    assert not m.reactions["RXN_c"].transmembrane
    stoich = {"CPD1_c": -1, "CPD2_c": 1}
    assert m.reactions["RXN_c"].stoichiometries == stoich
    # Periplasm - the compounds will be created, but the reaction should not
    assert m.compounds["CPD1_p"].compartment == "PERIPLASM"
    assert m.compounds["CPD2_p"].compartment == "PERIPLASM"
    assert not m.reactions["RXN_p"].transmembrane
    stoich = {"CPD1_p": -1, "CPD2_p": 1}
    assert m.reactions["RXN_p"].stoichiometries == stoich
    # Extracellular
    with pytest.raises(KeyError):
        m.compounds["CPD1_e"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_e"]
    with pytest.raises(KeyError):
        m.reactions["RXN_e"]


def test_multiple_locations_cytosol_extracellular_all_out() -> None:
    """This should give both cytosolic and extracellular"""
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-OUT",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-OUT",
        "RXN-LOCATIONS - CCO-CYTOSOL",
        "RXN-LOCATIONS - CCO-EXTRACELLULAR",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    assert m.compounds["CPD1_c"].compartment == "CYTOSOL"
    assert m.compounds["CPD2_c"].compartment == "CYTOSOL"
    assert not m.reactions["RXN_c"].transmembrane
    stoich = {"CPD1_c": -1, "CPD2_c": 1}
    assert m.reactions["RXN_c"].stoichiometries == stoich
    # Periplasm
    with pytest.raises(KeyError):
        m.compounds["CPD1_p"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_p"]
    with pytest.raises(KeyError):
        m.reactions["RXN_p"]
    # Extracellular
    assert m.compounds["CPD1_e"].compartment == "EXTRACELLULAR"
    assert m.compounds["CPD2_e"].compartment == "EXTRACELLULAR"
    assert not m.reactions["RXN_e"].transmembrane
    stoich = {"CPD1_e": -1, "CPD2_e": 1}
    assert m.reactions["RXN_e"].stoichiometries == stoich


def test_fake_transmembrane_location_all_out() -> None:
    """This should give only extracelluar, regardless of the location.
    It just doesn't make any sense to have a transmembrane string
    for just CCO-OUT annotation
    """
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-OUT",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-OUT",
        "RXN-LOCATIONS - CCO-EXTRACELLULAR-CCO-CYTOSOL",  # out - in
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    with pytest.raises(KeyError):
        m.compounds["CPD1_c"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_c"]
    with pytest.raises(KeyError):
        m.reactions["RXN_c"]
    # Periplasm
    with pytest.raises(KeyError):
        m.compounds["CPD1_p"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_p"]
    with pytest.raises(KeyError):
        m.reactions["RXN_p"]
    # Extracellular
    assert m.compounds["CPD1_e"].compartment == "EXTRACELLULAR"
    assert m.compounds["CPD2_e"].compartment == "EXTRACELLULAR"
    assert not m.reactions["RXN_e"].transmembrane
    stoich = {"CPD1_e": -1, "CPD2_e": 1}
    assert m.reactions["RXN_e"].stoichiometries == stoich


def test_no_location_in_out() -> None:
    """Should yield _c_e"""
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-IN",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-OUT",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    assert m.compounds["CPD1_c"].compartment == "CYTOSOL"
    with pytest.raises(KeyError):
        m.compounds["CPD2_c"]
    with pytest.raises(KeyError):
        m.reactions["RXN_c"]
    # Periplasm
    with pytest.raises(KeyError):
        m.compounds["CPD1_p"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_p"]
    with pytest.raises(KeyError):
        m.reactions["RXN_p"]
    # Extracellular
    with pytest.raises(KeyError):
        m.compounds["CPD1_e"]
    assert m.compounds["CPD2_e"].compartment == "EXTRACELLULAR"
    with pytest.raises(KeyError):
        m.reactions["RXN_e"]
    # Cytosol - Periplasm
    with pytest.raises(KeyError):
        m.reactions["RXN_c_p"]
    # Cytosol - Extracellular
    stoich = {"CPD1_c": -1, "CPD2_e": 1}
    assert m.reactions["RXN_c_e"].stoichiometries == stoich
    # Periplasm - Cytosol
    with pytest.raises(KeyError):
        m.reactions["RXN_p_c"]
    # Extracellular - Cytosol
    with pytest.raises(KeyError):
        m.reactions["RXN_e_c"]
    # Extracellular - Periplasm
    with pytest.raises(KeyError):
        m.reactions["RXN_e_p"]
    # Periplasm - Extracellular
    with pytest.raises(KeyError):
        m.reactions["RXN_p_e"]


def test_single_location_cytosol_in_out() -> None:
    """This one is a bit debatable. It will be mapped to
    CCO-CYTOSOL-CCO-CYTOSOL, so it will loose its transmembrane
    information
    Should yield _c
    """
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-IN",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-OUT",
        "RXN-LOCATIONS - CCO-CYTOSOL",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    assert m.compounds["CPD1_c"].compartment == "CYTOSOL"
    assert m.compounds["CPD2_c"].compartment == "CYTOSOL"
    stoich = {"CPD1_c": -1, "CPD2_c": 1}
    assert m.reactions["RXN_c"].stoichiometries == stoich
    assert not m.reactions["RXN_c"].transmembrane
    # Periplasm
    with pytest.raises(KeyError):
        m.compounds["CPD1_p"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_p"]
    with pytest.raises(KeyError):
        m.reactions["RXN_p"]
    # Extracellular
    with pytest.raises(KeyError):
        m.compounds["CPD1_e"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_e"]
    with pytest.raises(KeyError):
        m.reactions["RXN_e"]
    # Cytosol - Periplasm
    with pytest.raises(KeyError):
        m.reactions["RXN_c_p"]
    # Cytosol - Extracellular
    with pytest.raises(KeyError):
        m.reactions["RXN_c_e"]
    # Periplasm - Cytosol
    with pytest.raises(KeyError):
        m.reactions["RXN_p_c"]
    # Extracellular - Periplasm
    with pytest.raises(KeyError):
        m.reactions["RXN_e_p"]
    # Periplasm - Extracellular
    with pytest.raises(KeyError):
        m.reactions["RXN_p_e"]
    # Extracellular - Periplasm
    with pytest.raises(KeyError):
        m.reactions["RXN_e_p"]


def test_single_location_periplasm_in_out() -> None:
    """Should yield _c_e"""
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-IN",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-OUT",
        "RXN-LOCATIONS - CCO-PERIPLASM",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    assert m.compounds["CPD1_c"].compartment == "CYTOSOL"
    with pytest.raises(KeyError):
        m.compounds["CPD2_c"]
    with pytest.raises(KeyError):
        m.reactions["RXN_c"]
    # Periplasm
    with pytest.raises(KeyError):
        m.compounds["CPD1_p"]
    assert m.compounds["CPD2_p"].compartment == "PERIPLASM"
    with pytest.raises(KeyError):
        m.reactions["RXN_p"]
    # Extracellular
    with pytest.raises(KeyError):
        m.compounds["CPD1_e"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_e"]
    with pytest.raises(KeyError):
        m.reactions["RXN_e"]
    # Cytosol - Periplasm
    stoich = {"CPD1_c": -1, "CPD2_p": 1}
    assert m.reactions["RXN_c_p"].stoichiometries == stoich
    assert m.reactions["RXN_c_p"].transmembrane
    # Cytosol - Extracellular
    with pytest.raises(KeyError):
        m.reactions["RXN_c_e"]
    # Periplasm - Cytosol
    with pytest.raises(KeyError):
        m.reactions["RXN_p_c"]
    # Extracellular - Periplasm
    with pytest.raises(KeyError):
        m.reactions["RXN_e_p"]
    # Extracellular - Periplasm
    with pytest.raises(KeyError):
        m.reactions["RXN_e_p"]
    # Periplasm - Extracellular
    with pytest.raises(KeyError):
        m.reactions["RXN_p_e"]


def test_single_location_extracellular_in_out() -> None:
    """Should yield _c_e"""
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-IN",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-OUT",
        "RXN-LOCATIONS - CCO-EXTRACELLULAR",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    assert m.compounds["CPD1_c"].compartment == "CYTOSOL"
    with pytest.raises(KeyError):
        m.compounds["CPD2_c"]
    with pytest.raises(KeyError):
        m.reactions["RXN_c"]
    # Periplasm
    with pytest.raises(KeyError):
        m.compounds["CPD1_p"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_p"]
    with pytest.raises(KeyError):
        m.reactions["RXN_p"]
    # Extracellular
    with pytest.raises(KeyError):
        m.compounds["CPD1_e"]
    assert m.compounds["CPD2_e"].compartment == "EXTRACELLULAR"
    with pytest.raises(KeyError):
        m.reactions["RXN_e"]
    # Cytosol - Periplasm
    with pytest.raises(KeyError):
        m.reactions["RXN_c_p"]
    # Cytosol - Extracellular
    stoich = {"CPD1_c": -1, "CPD2_e": 1}
    assert m.reactions["RXN_c_e"].stoichiometries == stoich
    assert m.reactions["RXN_c_e"].transmembrane
    # Periplasm - Cytosol
    with pytest.raises(KeyError):
        m.reactions["RXN_p_c"]
    # Extracellular - Periplasm
    with pytest.raises(KeyError):
        m.reactions["RXN_e_p"]
    # Extracellular - Periplasm
    with pytest.raises(KeyError):
        m.reactions["RXN_e_p"]
    # Periplasm - Extracellular
    with pytest.raises(KeyError):
        m.reactions["RXN_p_e"]


def test_transmembrane_locations_cytosol_periplasm_in_out() -> None:
    """Should yield _c_p"""
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-IN",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-OUT",
        "RXN-LOCATIONS - CCO-PERIPLASM-CCO-CYTOSOL",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    assert m.compounds["CPD1_c"].compartment == "CYTOSOL"
    with pytest.raises(KeyError):
        m.compounds["CPD1_2"]
    with pytest.raises(KeyError):
        m.reactions["RXN_c"]
    # Periplasm
    with pytest.raises(KeyError):
        m.compounds["CPD1_p"]
    assert m.compounds["CPD2_p"].compartment == "PERIPLASM"
    with pytest.raises(KeyError):
        m.reactions["RXN_p"]
    # Extracellular
    with pytest.raises(KeyError):
        m.compounds["CPD1_e"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_e"]
    with pytest.raises(KeyError):
        m.reactions["RXN_e"]
    # Cytosol - Periplasm
    stoich = {"CPD1_c": -1, "CPD2_p": 1}
    assert m.reactions["RXN_c_p"].stoichiometries == stoich
    assert m.reactions["RXN_c_p"].transmembrane
    # Cytosol - Extracellular
    with pytest.raises(KeyError):
        m.reactions["RXN_c_e"]
    # Periplasm - Cytosol
    with pytest.raises(KeyError):
        m.reactions["RXN_p_c"]
    # Extracellular - Periplasm
    with pytest.raises(KeyError):
        m.reactions["RXN_e_p"]
    # Extracellular - Periplasm
    with pytest.raises(KeyError):
        m.reactions["RXN_e_p"]
    # Periplasm - Extracellular
    with pytest.raises(KeyError):
        m.reactions["RXN_p_e"]


def test_transmembrane_locations_cytosol_extracellular_in_out() -> None:
    """Should yield _c_e"""
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-IN",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-OUT",
        "RXN-LOCATIONS - CCO-EXTRACELLULAR-CCO-CYTOSOL",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    assert m.compounds["CPD1_c"].compartment == "CYTOSOL"
    with pytest.raises(KeyError):
        m.compounds["CPD2_c"]
    with pytest.raises(KeyError):
        m.reactions["RXN_c"]
    # Periplasm
    with pytest.raises(KeyError):
        m.compounds["CPD1_p"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_p"]
    with pytest.raises(KeyError):
        m.reactions["RXN_p"]
    # Extracellular
    with pytest.raises(KeyError):
        m.compounds["CPD1_e"]
    assert m.compounds["CPD2_e"].compartment == "EXTRACELLULAR"
    with pytest.raises(KeyError):
        m.reactions["RXN_e"]
    # Cytosol - Periplasm
    with pytest.raises(KeyError):
        m.reactions["RXN_c_p"]
    # Cytosol - Extracellular
    stoich = {"CPD1_c": -1, "CPD2_e": 1}
    assert m.reactions["RXN_c_e"].stoichiometries == stoich
    assert m.reactions["RXN_c_e"].transmembrane
    # Periplasm - Cytosol
    with pytest.raises(KeyError):
        m.reactions["RXN_p_c"]
    # Extracellular - Periplasm
    with pytest.raises(KeyError):
        m.reactions["RXN_e_p"]
    # Extracellular - Periplasm
    with pytest.raises(KeyError):
        m.reactions["RXN_e_p"]
    # Periplasm - Extracellular
    with pytest.raises(KeyError):
        m.reactions["RXN_p_e"]


def test_transmembrane_locations_periplasm_cytosol_in_out() -> None:
    """Should yield _p_c"""
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-IN",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-OUT",
        "RXN-LOCATIONS - CCO-CYTOSOL-CCO-PERIPLASM",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    with pytest.raises(KeyError):
        m.compounds["CPD1_c"]
    assert m.compounds["CPD2_c"].compartment == "CYTOSOL"
    with pytest.raises(KeyError):
        m.reactions["RXN_c"]
    # Periplasm
    assert m.compounds["CPD1_p"].compartment == "PERIPLASM"
    with pytest.raises(KeyError):
        m.compounds["CPD2_p"]
    with pytest.raises(KeyError):
        m.reactions["RXN_p"]
    # Extracellular
    with pytest.raises(KeyError):
        m.compounds["CPD1_e"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_e"]
    with pytest.raises(KeyError):
        m.reactions["RXN_e"]
    # Cytosol - Periplasm
    with pytest.raises(KeyError):
        m.reactions["RXN_c_p"]
    # Cytosol - Extracellular
    with pytest.raises(KeyError):
        m.reactions["RXN_c_e"]
    # Periplasm - Cytosol
    stoich = {"CPD1_p": -1, "CPD2_c": 1}
    assert m.reactions["RXN_p_c"].stoichiometries == stoich
    assert m.reactions["RXN_p_c"].transmembrane
    # Extracellular - Cytosol
    with pytest.raises(KeyError):
        m.reactions["RXN_e_c"]
    # Extracellular - Periplasm
    with pytest.raises(KeyError):
        m.reactions["RXN_e_p"]
    # Periplasm - Extracellular
    with pytest.raises(KeyError):
        m.reactions["RXN_p_e"]


def test_transmembrane_locations_extracellular_cytosol_in_out() -> None:
    """Should yield _e_c"""
    compound_file = [
        "UNIQUE-ID - CPD1",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
        "UNIQUE-ID - CPD2",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (C 1)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN",
        "LEFT - CPD1",
        "^COMPARTMENT - CCO-IN",
        "RIGHT - CPD2",
        "^COMPARTMENT - CCO-OUT",
        "RXN-LOCATIONS - CCO-CYTOSOL-CCO-EXTRACELLULAR",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    # Cytosol
    with pytest.raises(KeyError):
        m.compounds["CPD1_c"]
    assert m.compounds["CPD2_c"].compartment == "CYTOSOL"
    with pytest.raises(KeyError):
        m.reactions["RXN_c"]
    # Periplasm
    with pytest.raises(KeyError):
        m.compounds["CPD1_p"]
    with pytest.raises(KeyError):
        m.compounds["CPD2_p"]
    with pytest.raises(KeyError):
        m.reactions["RXN_p"]
    # Extracellular
    assert m.compounds["CPD1_e"].compartment == "EXTRACELLULAR"
    with pytest.raises(KeyError):
        m.compounds["CPD2_e"]
    with pytest.raises(KeyError):
        m.reactions["RXN_e"]
    # Cytosol - Periplasm
    with pytest.raises(KeyError):
        m.reactions["RXN_c_p"]
    # Cytosol - Extracellular
    with pytest.raises(KeyError):
        m.reactions["RXN_c_e"]
    # Periplasm - Cytosol
    with pytest.raises(KeyError):
        m.reactions["RXN_p_c"]
    # Extracellular - Cytosol
    stoich = {"CPD1_e": -1, "CPD2_c": 1}
    assert m.reactions["RXN_e_c"].stoichiometries == stoich
    assert m.reactions["RXN_e_c"].transmembrane
    # Extracellular - Periplasm
    with pytest.raises(KeyError):
        m.reactions["RXN_e_p"]
    # Periplasm - Extracellular
    with pytest.raises(KeyError):
        m.reactions["RXN_p_e"]


def test_psii_rxn() -> None:
    compound_file = [
        "UNIQUE-ID - Plastoquinols",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
        "UNIQUE-ID - PROTON",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
        "UNIQUE-ID - OXYGEN-MOLECULE",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
        "UNIQUE-ID - Light",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
        "UNIQUE-ID - PLASTOQUINONE",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
        "UNIQUE-ID - WATER",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
    ]
    reaction_file = [
        "UNIQUE-ID - PSII-RXN",
        "TYPES - Chemical-Reactions",
        "TYPES - Electron-Transfer-Reactions",
        "TYPES - Small-Molecule-Reactions",
        "IN-PATHWAY - PWY-101",
        "LEFT - Plastoquinols",
        "^COEFFICIENT - 2",
        "LEFT - PROTON",
        "^COEFFICIENT - 4",
        "^COMPARTMENT - CCO-IN",
        "LEFT - OXYGEN-MOLECULE",
        "^COMPARTMENT - CCO-IN",
        "REACTION-DIRECTION - PHYSIOL-RIGHT-TO-LEFT",
        "RIGHT - Light",
        "^COMPARTMENT - CCO-CYTOSOL",
        "RIGHT - PLASTOQUINONE",
        "^COEFFICIENT - 2",
        "RIGHT - PROTON",
        "^COEFFICIENT - 4",
        "^COMPARTMENT - CCO-OUT",
        "RIGHT - WATER",
        "^COEFFICIENT - 2",
        "^COMPARTMENT - CCO-IN",
        "RXN-LOCATIONS - CCO-CHL-THY-MEM",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    rxn = m.reactions["PSII-RXN_c_p"]
    stoich = {
        "Light_c": -1,
        "PLASTOQUINONE_c": -2.0,
        "PROTON_c": -4.0,
        "WATER_c": -2.0,
        "Plastoquinols_c": 2.0,
        "PROTON_p": 4.0,
        "OXYGEN-MOLECULE_c": 1,
    }
    assert rxn.stoichiometries == stoich


def test_1_18_1_2_rxn() -> None:
    compound_file = [
        "UNIQUE-ID - NADP",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
        "UNIQUE-ID - PROTON",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
        "UNIQUE-ID - Reduced-ferredoxins",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
        "UNIQUE-ID - Oxidized-ferredoxins",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
        "UNIQUE-ID - NADPH",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
    ]
    reaction_file = [
        "UNIQUE-ID - 1.18.1.2-RXN",
        "TYPES - Electron-Transfer-Reactions",
        "TYPES - Protein-Modification-Reactions",
        "IN-PATHWAY - PWY-101",
        "LEFT - NADP",
        "^COMPARTMENT - CCO-OUT",
        "LEFT - PROTON",
        "^COMPARTMENT - CCO-OUT",
        "LEFT - Reduced-ferredoxins",
        "^COEFFICIENT - 2",
        "^COMPARTMENT - CCO-OUT",
        "REACTION-DIRECTION - REVERSIBLE",
        "RIGHT - Oxidized-ferredoxins",
        "^COEFFICIENT - 2",
        "^COMPARTMENT - CCO-OUT",
        "RIGHT - NADPH",
        "^COMPARTMENT - CCO-OUT",
        "RXN-LOCATIONS - CCO-SIDE-2-CCO-SIDE-1",
        "RXN-LOCATIONS - CCO-EXTRACELLULAR-CCO-CYTOSOL",
        "RXN-LOCATIONS - CCO-CHLOR-STR-CCO-THY-LUM-CYA",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    rxn = m.reactions["1.18.1.2-RXN_c"]
    stoich = {
        "NADP_c": -1,
        "PROTON_c": -1,
        "Reduced-ferredoxins_c": -2.0,
        "Oxidized-ferredoxins_c": 2.0,
        "NADPH_c": 1,
    }
    assert rxn.stoichiometries == stoich


def test_rxn_15479() -> None:
    compound_file = [
        "UNIQUE-ID - Oxidized-Plastocyanins",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
        "UNIQUE-ID - Light",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
        "UNIQUE-ID - Reduced-ferredoxins",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
        "UNIQUE-ID - Oxidized-ferredoxins",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
        "UNIQUE-ID - Plastocyanin-Reduced",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN-15479",
        "TYPES - Electron-Transfer-Reactions",
        "TYPES - Protein-Modification-Reactions",
        "IN-PATHWAY - PWY-101",
        "LEFT - Oxidized-Plastocyanins",
        "^COMPARTMENT - CCO-IN",
        "LEFT - Reduced-ferredoxins",
        "^COMPARTMENT - CCO-OUT",
        "REACTION-DIRECTION - PHYSIOL-RIGHT-TO-LEFT",
        "RIGHT - Light",
        "^COMPARTMENT - CCO-CYTOSOL",
        "RIGHT - Plastocyanin-Reduced",
        "^COMPARTMENT - CCO-IN",
        "RIGHT - Oxidized-ferredoxins",
        "^COMPARTMENT - CCO-OUT",
        "RXN-LOCATIONS - CCO-CHL-THY-MEM",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    rxn = m.reactions["RXN-15479_c"]
    stoich = {
        "Light_c": -1,
        "Plastocyanin-Reduced_c": -1,
        "Oxidized-ferredoxins_c": -1,
        "Oxidized-Plastocyanins_c": 1,
        "Reduced-ferredoxins_c": 1,
    }
    assert rxn.stoichiometries == stoich


def test_plastoquionol_plastocyanin_reductase_rxn() -> None:
    compound_file = [
        "UNIQUE-ID - Plastoquinols",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
        "UNIQUE-ID - Oxidized-Plastocyanins",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
        "UNIQUE-ID - PROTON",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
        "UNIQUE-ID - PLASTOQUINONE",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
        "UNIQUE-ID - Plastocyanin-Reduced",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
    ]
    reaction_file = [
        "UNIQUE-ID - PLASTOQUINOL--PLASTOCYANIN-REDUCTASE-RXN",
        "TYPES - Electron-Transfer-Reactions",
        "TYPES - Protein-Modification-Reactions",
        "IN-PATHWAY - PWY-101",
        "LEFT - Plastoquinols",
        "LEFT - Oxidized-Plastocyanins",
        "^COEFFICIENT - 2",
        "^COMPARTMENT - CCO-IN",
        "LEFT - PROTON",
        "^COEFFICIENT - 2",
        "^COMPARTMENT - CCO-OUT",
        "REACTION-DIRECTION - LEFT-TO-RIGHT",
        "RIGHT - PLASTOQUINONE",
        "RIGHT - Plastocyanin-Reduced",
        "^COEFFICIENT - 2",
        "^COMPARTMENT - CCO-IN",
        "RIGHT - PROTON",
        "^COEFFICIENT - 4",
        "^COMPARTMENT - CCO-IN",
        "RXN-LOCATIONS - CCO-CHL-THY-MEM",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    rxn = m.reactions["PLASTOQUINOL--PLASTOCYANIN-REDUCTASE-RXN_c_p"]
    stoich = {
        "Plastoquinols_c": -1,
        "Oxidized-Plastocyanins_c": -2.0,
        "PROTON_c": -2.0,
        "PLASTOQUINONE_c": 1,
        "Plastocyanin-Reduced_c": 2.0,
        "PROTON_p": 4.0,
    }
    assert rxn.stoichiometries == stoich


def test_no_type() -> None:
    """Expect stoichiometry to be switched"""
    compound_file = [
        "UNIQUE-ID - PROTON",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN1",
        "LEFT - PROTON",
        "^COEFFICIENT - 4",
        "^COMPARTMENT - CCO-IN",
        "REACTION-DIRECTION - REVERSIBLE",
        "RIGHT - PROTON",
        "^COEFFICIENT - 2",
        "^COMPARTMENT - CCO-OUT",
        "RXN-LOCATIONS - CCO-PERIPLASM-CCO-CYTOSOL",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    rxn = m.reactions["RXN1_c_p"]
    stoich = {
        "PROTON_p": -2,
        "PROTON_c": 4,
    }
    assert rxn.stoichiometries == stoich
    assert rxn.bounds == (0, 1000)
    assert not rxn.reversible


def test_tr12() -> None:
    """Disallowed reaction
    reaction type TR-12: Transport Energized by the Membrane Electrochemical Gradient
    Expect stoichiometry to be switched and bounds to be (0, 1000)
    """
    compound_file = [
        "UNIQUE-ID - PROTON",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN1",
        "TYPES - TR-12",
        "LEFT - PROTON",
        "^COEFFICIENT - 4",
        "^COMPARTMENT - CCO-IN",
        "REACTION-DIRECTION - REVERSIBLE",
        "RIGHT - PROTON",
        "^COEFFICIENT - 2",
        "^COMPARTMENT - CCO-OUT",
        "RXN-LOCATIONS - CCO-PERIPLASM-CCO-CYTOSOL",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    rxn = m.reactions["RXN1_c_p"]
    stoich = {
        "PROTON_p": -2,
        "PROTON_c": 4,
    }
    assert rxn.stoichiometries == stoich
    assert rxn.bounds == (0, 1000)
    assert not rxn.reversible


def test_tr13() -> None:
    """Allowed reaction
    reaction type TR-13: Transport Energized by Phosphoanhydride-Bond Hydrolysis
    """
    compound_file = [
        "UNIQUE-ID - PROTON",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN1",
        "TYPES - TR-13",
        "LEFT - PROTON",
        "^COEFFICIENT - 4",
        "^COMPARTMENT - CCO-IN",
        "REACTION-DIRECTION - REVERSIBLE",
        "RIGHT - PROTON",
        "^COEFFICIENT - 2",
        "^COMPARTMENT - CCO-OUT",
        "RXN-LOCATIONS - CCO-PERIPLASM-CCO-CYTOSOL",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    rxn = m.reactions["RXN1_c_p"]
    stoich = {
        "PROTON_c": -4,
        "PROTON_p": 2,
    }
    assert rxn.stoichiometries == stoich
    assert rxn.bounds == (-1000, 1000)
    assert rxn.reversible


def test_tr15() -> None:
    """Allowed reaction
    reaction type TR-15: Transport Energized by Decarboxylation
    """
    compound_file = [
        "UNIQUE-ID - PROTON",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN1",
        "TYPES - TR-15",
        "LEFT - PROTON",
        "^COEFFICIENT - 4",
        "^COMPARTMENT - CCO-IN",
        "REACTION-DIRECTION - REVERSIBLE",
        "RIGHT - PROTON",
        "^COEFFICIENT - 2",
        "^COMPARTMENT - CCO-OUT",
        "RXN-LOCATIONS - CCO-PERIPLASM-CCO-CYTOSOL",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    rxn = m.reactions["RXN1_c_p"]
    stoich = {
        "PROTON_c": -4,
        "PROTON_p": 2,
    }
    assert rxn.stoichiometries == stoich
    assert rxn.bounds == (-1000, 1000)
    assert rxn.reversible


def test_etr() -> None:
    """Allowed reaction"""
    compound_file = [
        "UNIQUE-ID - PROTON",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN1",
        "TYPES - Electron-Transfer-Reactions",
        "LEFT - PROTON",
        "^COEFFICIENT - 4",
        "^COMPARTMENT - CCO-IN",
        "REACTION-DIRECTION - REVERSIBLE",
        "RIGHT - PROTON",
        "^COEFFICIENT - 2",
        "^COMPARTMENT - CCO-OUT",
        "RXN-LOCATIONS - CCO-PERIPLASM-CCO-CYTOSOL",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    rxn = m.reactions["RXN1_c_p"]
    stoich = {
        "PROTON_c": -4,
        "PROTON_p": 2,
    }
    assert rxn.stoichiometries == stoich
    assert rxn.bounds == (-1000, 1000)
    assert rxn.reversible


def test_mpmr() -> None:
    """Allowed reaction"""
    compound_file = [
        "UNIQUE-ID - PROTON",
        "ATOM-CHARGES - (0 0)",
        "CHEMICAL-FORMULA - (X 0)",
    ]
    reaction_file = [
        "UNIQUE-ID - RXN1",
        "TYPES - Membrane-Protein-Modification-Reactions",
        "LEFT - PROTON",
        "^COEFFICIENT - 4",
        "^COMPARTMENT - CCO-IN",
        "REACTION-DIRECTION - REVERSIBLE",
        "RIGHT - PROTON",
        "^COEFFICIENT - 2",
        "^COMPARTMENT - CCO-OUT",
        "RXN-LOCATIONS - CCO-PERIPLASM-CCO-CYTOSOL",
    ]
    m = mock_parsing(compound_file=compound_file, reaction_file=reaction_file)
    rxn = m.reactions["RXN1_c_p"]
    stoich = {
        "PROTON_c": -4,
        "PROTON_p": 2,
    }
    assert rxn.stoichiometries == stoich
    assert rxn.bounds == (-1000, 1000)
    assert rxn.reversible
