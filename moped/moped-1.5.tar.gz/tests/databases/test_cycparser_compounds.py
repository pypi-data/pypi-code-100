from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple
from unittest import mock

from moped.databases.cyc import CompoundParser, ParseCompound

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


def read_mock_file(file: List[str]) -> Tuple[Dict[str, ParseCompound], Dict[str, List[str]]]:
    with mock.patch(
        "moped.databases.cyc._open_file_and_remove_comments",
        mock.Mock(return_value=("", 0)),
    ):
        CP = CompoundParser(Path(""), {})
        CP.file = file
        cpds, types = CP.parse()
        return cpds, types


def test_create_compound() -> None:
    cpds, types = read_mock_file(["UNIQUE-ID - cpd1"])
    assert cpds["cpd1_c"].id == "cpd1_c"


def test_create_default_compartment() -> None:
    cpds, types = read_mock_file(["UNIQUE-ID - cpd1"])
    assert cpds["cpd1_c"].compartment == "CYTOSOL"


def test_create_default_charge() -> None:
    cpds, types = read_mock_file(["UNIQUE-ID - cpd1"])
    assert cpds["cpd1_c"].charge == 0


def test_add_cpd_type_single() -> None:
    cpds, types = read_mock_file(["UNIQUE-ID - cpd1", "TYPES - LIGNAN"])
    assert cpds["cpd1_c"].types == ["LIGNAN"]
    assert types == {"LIGNAN_c": ["cpd1_c"]}


def test_add_cpd_type_double() -> None:
    cpds, types = read_mock_file(["UNIQUE-ID - cpd1", "TYPES - LIGNAN", "TYPES - Toxins"])
    assert cpds["cpd1_c"].types == ["LIGNAN", "Toxins"]
    assert types == {"Toxins_c": ["cpd1_c"]}


def test_atom_charges_neg() -> None:
    cpds, types = read_mock_file(
        [
            "UNIQUE-ID - cpd1",
            "ATOM-CHARGES - (0 -1)",
        ]
    )
    assert cpds["cpd1_c"].charge == -1.0


def test_atom_charges_pos() -> None:
    cpds, types = read_mock_file(
        [
            "UNIQUE-ID - cpd1",
            "ATOM-CHARGES - (0 1)",
        ]
    )
    assert cpds["cpd1_c"].charge == 1.0


def test_formula_single() -> None:
    cpds, types = read_mock_file(
        [
            "UNIQUE-ID - cpd1",
            "CHEMICAL-FORMULA - (C 1)",
        ]
    )
    assert cpds["cpd1_c"].formula == {"C": 1}


def test_formula_multiple() -> None:
    cpds, types = read_mock_file(
        [
            "UNIQUE-ID - cpd1",
            "CHEMICAL-FORMULA - (C 6)",
            "CHEMICAL-FORMULA - (H 12)",
            "CHEMICAL-FORMULA - (O 6)",
        ]
    )
    assert cpds["cpd1_c"].formula == {"C": 6, "H": 12, "O": 6}


def test_formula_two_letters() -> None:
    cpds, types = read_mock_file(["UNIQUE-ID - cpd1", "CHEMICAL-FORMULA - (He 1)"])
    assert cpds["cpd1_c"].formula == {"He": 1}


def test_formula_multiple_two_letters() -> None:
    cpds, types = read_mock_file(
        [
            "UNIQUE-ID - cpd1",
            "CHEMICAL-FORMULA - (C 6)",
            "CHEMICAL-FORMULA - (He 12)",
            "CHEMICAL-FORMULA - (O 6)",
        ]
    )
    assert cpds["cpd1_c"].formula == {"C": 6, "He": 12, "O": 6}


def test_smiles() -> None:
    cpds, types = read_mock_file(["UNIQUE-ID - cpd1", "SMILES - COC1"])
    assert cpds["cpd1_c"].smiles == "COC1"


def test_atom_charges_pos_and_neg() -> None:
    cpds, types = read_mock_file(
        [
            "UNIQUE-ID - cpd1",
            "ATOM-CHARGES - (0 -1)",
            "ATOM-CHARGES - (1 1)",
        ]
    )
    assert cpds["cpd1_c"].charge == 0
