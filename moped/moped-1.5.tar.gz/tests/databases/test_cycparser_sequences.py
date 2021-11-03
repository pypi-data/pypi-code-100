from __future__ import annotations

from pathlib import Path
from typing import Dict, List
from unittest import mock

from moped.databases.cyc import Cyc, SequenceParser

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


def read_mock_file(file: List[str]) -> Dict[str, str]:
    with mock.patch("builtins.open", mock.mock_open(read_data="")):
        SP = SequenceParser(Path(""))
        SP.file = file
        return SP.parse()


def test_read_multiple() -> None:
    sequences = read_mock_file(
        [
            ">gnl|META|HS10525-MONOMER Serine--pyruvate aminotransferase (Homo sapiens)",
            "MASHED",
            ">gnl|META|HS10520-MONOMER alpha-(1,3)-fucosyltransferase 9 (Homo sapiens)",
            "POTATOES",
        ]
    )
    assert sequences["HS10525-MONOMER"] == "MASHED"
    assert sequences["HS10520-MONOMER"] == "POTATOES"


def test_cyc_parse() -> None:
    compounds, reactions, compartments = Cyc(
        pgdb_path=TESTCYC_PATH,
        compartment_map=COMPARTMENT_MAP,
        parse_sequences=True,
        type_map={},
    ).parse()
    assert True


def test_cyc_parse_no_sequences() -> None:
    compounds, reactions, compartments = Cyc(
        pgdb_path=TESTCYC_WO_SEQ_PATH,
        compartment_map=COMPARTMENT_MAP,
        parse_sequences=True,
        type_map={},
    ).parse()
    assert True
