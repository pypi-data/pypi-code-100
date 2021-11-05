from __future__ import annotations

from pathlib import Path
from typing import Dict, List
from unittest import mock

from moped.databases.cyc import ParseReaction, ReactionParser

TESTCYC_PATH = Path(__file__).parent / "testcyc"
TESTCYC_WO_SEQ_PATH = Path(__file__).parent / "testcyc_without_sequences"

COMPARTMENT_MAP = {
    "CYTOSOL": "CYTOSOL",
    "IN": "CYTOSOL",
    "UNKNOWN-SPACE": "CYTOSOL",
    "SIDE-1": "CYTOSOL",
    "SIDE-2": "PERIPLASM",
    "EXTRACELLULAR": "EXTRACELLULAR",
    "CHL-THY-MEM": "PERIPLASM",
    "CHLOR-STR": "PERIPLASM",
    "CHROM-STR": "PERIPLASM",
    "GOLGI-LUM": "CYTOSOL",
    "LYS-LUM": "CYTOSOL",
    "MIT-IM-SPC": "PERIPLASM",
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
    "OUT": "EXTRACELLULAR",
}


def read_mock_file(file: List[str]) -> Dict[str, ParseReaction]:
    with mock.patch(
        "moped.databases.cyc._open_file_and_remove_comments",
        mock.Mock(return_value=("", 0)),
    ):
        RP = ReactionParser(Path(""), {})
        RP.file = file
        rxns = RP.parse()
        return rxns


def test_create_reaction() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001"])
    assert rxns["RXN001"].id == "RXN001"


def test_set_ec_number() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "EC-NUMBER - EC-3.5.4.32"])
    assert rxns["RXN001"].ec == "EC-3.5.4.32"


def test_add_single_pathway() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "IN-PATHWAY - PWY-7623"])
    assert rxns["RXN001"].pathways == {"PWY-7623"}


def test_add_multiple_pathways() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "IN-PATHWAY - PWY-0001", "IN-PATHWAY - PWY-0002"])
    assert rxns["RXN001"].pathways == {"PWY-0001", "PWY-0002"}


def test_add_single_enzyme() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "ENZYMATIC-REACTION - ENZRXN-23486"])
    assert rxns["RXN001"].enzymes == {"ENZRXN-23486"}


def test_default_reversibility() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001"])
    assert rxns["RXN001"].reversible is False


def test_irreversible() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "REACTION-DIRECTION - LEFT-TO-RIGHT"])
    assert rxns["RXN001"].reversible is False


def test_reversible() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "REACTION-DIRECTION - REVERSIBLE"])
    assert rxns["RXN001"].reversible is True


def test_default_direction() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001"])
    assert rxns["RXN001"].direction == "LEFT-TO-RIGHT"


def test_set_direction_left_to_right() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "REACTION-DIRECTION - LEFT-TO-RIGHT"])
    assert rxns["RXN001"].direction == "LEFT-TO-RIGHT"


def test_set_direction_right_to_left() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "REACTION-DIRECTION - RIGHT-TO-LEFT"])
    assert rxns["RXN001"].direction == "RIGHT-TO-LEFT"


def test_set_direction_reversible() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "REACTION-DIRECTION - REVERSIBLE"])
    assert rxns["RXN001"].direction == "REVERSIBLE"


def test_add_direction_reversible() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "REACTION-DIRECTION - REVERSIBLE"])
    assert rxns["RXN001"].direction == "REVERSIBLE"


def test_add_location_default() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001"])
    assert rxns["RXN001"].locations == []


def test_add_location_cytosol() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "RXN-LOCATIONS - CCO-CYTOSOL"])
    assert rxns["RXN001"].locations == ["CCO-CYTOSOL"]


def test_add_location_extracellular() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "RXN-LOCATIONS - CCO-EXTRACELLULAR"])
    assert rxns["RXN001"].locations == ["CCO-EXTRACELLULAR"]


def test_add_location_periplasm() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "RXN-LOCATIONS - CCO-PERIPLASM"])
    assert rxns["RXN001"].locations == ["CCO-PERIPLASM"]


def test_add_location_cci() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "RXN-LOCATIONS - CCI-PERIPLASM"])
    assert rxns["RXN001"].locations == ["CCO-PERIPLASM"]


def test_add_location_nil() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "RXN-LOCATIONS - NIL"])
    assert rxns["RXN001"].locations == []


def test_add_location_other() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "RXN-LOCATIONS - CCO-SIDE1"])
    assert rxns["RXN001"].locations == ["CCO-SIDE1"]


def test_add_substrate_default_stoichiometry() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "LEFT - cpd1"])
    assert rxns["RXN001"].substrates == {"cpd1_c": -1}
    assert rxns["RXN001"].products == {}


def test_add_multiple_substrates() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "LEFT - cpd1", "LEFT - cpd2"])
    assert rxns["RXN001"].substrates == {"cpd1_c": -1, "cpd2_c": -1}
    assert rxns["RXN001"].products == {}


def test_add_product_default_stoichiometry() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "RIGHT - cpd1"])
    assert rxns["RXN001"].substrates == {}
    assert rxns["RXN001"].products == {"cpd1_c": 1}


def test_add_multiple_products() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "RIGHT - cpd1", "RIGHT - cpd2"])
    assert rxns["RXN001"].substrates == {}
    assert rxns["RXN001"].products == {"cpd1_c": 1, "cpd2_c": 1}


def test_add_substrates_and_products() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "LEFT - cpd1", "RIGHT - cpd1"])
    assert rxns["RXN001"].substrates == {"cpd1_c": -1}
    assert rxns["RXN001"].products == {"cpd1_c": 1}


def test_set_substrate_coefficient_one() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "LEFT - cpd1", "^COEFFICIENT - 1"])
    assert rxns["RXN001"].substrates == {"cpd1_c": -1.0}
    assert rxns["RXN001"].products == {}


def test_set_substrate_coefficient_two() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "LEFT - cpd1", "^COEFFICIENT - 2"])
    assert rxns["RXN001"].substrates == {"cpd1_c": -2.0}
    assert rxns["RXN001"].products == {}


def test_set_substrate_coefficient_variable() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "LEFT - cpd1", "^COEFFICIENT - n"])
    assert rxns["RXN001"].substrates == {"cpd1_c": -1.0}
    assert rxns["RXN001"].products == {}


def test_set_product_coefficient_one() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "RIGHT - cpd1", "^COEFFICIENT - 1"])
    assert rxns["RXN001"].substrates == {}
    assert rxns["RXN001"].products == {"cpd1_c": 1.0}


def test_set_product_coefficient_two() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "RIGHT - cpd1", "^COEFFICIENT - 2"])
    assert rxns["RXN001"].substrates == {}
    assert rxns["RXN001"].products == {"cpd1_c": 2.0}


def test_set_product_coefficient_variable() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "RIGHT - cpd1", "^COEFFICIENT - n"])
    assert rxns["RXN001"].substrates == {}
    assert rxns["RXN001"].products == {"cpd1_c": 1.0}


def test_set_substrate_compartment_default() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "LEFT - cpd1"])
    assert rxns["RXN001"].substrates == {"cpd1_c": -1.0}
    assert rxns["RXN001"].substrate_compartments == {"cpd1_c": "CCO-IN"}


def test_set_substrate_compartment_in() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "LEFT - cpd1", "^COMPARTMENT - CCO-IN"])
    assert rxns["RXN001"].substrate_compartments == {"cpd1_c": "CCO-IN"}


def test_set_substrate_compartment_out() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "LEFT - cpd1", "^COMPARTMENT - CCO-OUT"])
    assert rxns["RXN001"].substrate_compartments == {"cpd1_c": "CCO-OUT"}


def test_set_substrate_compartment_middle() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "LEFT - cpd1", "^COMPARTMENT - CCO-MIDDLE"])
    assert rxns["RXN001"].substrate_compartments == {"cpd1_c": "CCO-OUT"}


def test_set_substrate_compartment_other() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "LEFT - cpd1", "^COMPARTMENT - UNKNOWN"])
    assert rxns["RXN001"].substrate_compartments == {"cpd1_c": "CCO-IN"}


def test_set_product_compartment_default() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "RIGHT - cpd1"])
    assert rxns["RXN001"].product_compartments == {"cpd1_c": "CCO-IN"}


def test_set_product_compartment_in() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "RIGHT - cpd1", "^COMPARTMENT - CCO-IN"])
    assert rxns["RXN001"].product_compartments == {"cpd1_c": "CCO-IN"}


def test_set_product_compartment_out() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "RIGHT - cpd1", "^COMPARTMENT - CCO-OUT"])
    assert rxns["RXN001"].product_compartments == {"cpd1_c": "CCO-OUT"}


def test_set_product_compartment_middle() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "RIGHT - cpd1", "^COMPARTMENT - CCO-MIDDLE"])
    assert rxns["RXN001"].product_compartments == {"cpd1_c": "CCO-OUT"}


def test_set_product_compartment_other() -> None:
    rxns = read_mock_file(["UNIQUE-ID - RXN001", "RIGHT - cpd1", "^COMPARTMENT - UNKNOWN"])
    assert rxns["RXN001"].product_compartments == {"cpd1_c": "CCO-IN"}
