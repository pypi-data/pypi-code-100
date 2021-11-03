from __future__ import annotations

from pathlib import Path
from typing import Dict, List
from unittest import mock

from moped.databases.cyc import EnzymeParser, ParseEnzyme

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


def read_mock_file(file: List[str]) -> Dict[str, ParseEnzyme]:
    with mock.patch(
        "moped.databases.cyc._open_file_and_remove_comments",
        mock.Mock(return_value=("", 0)),
    ):
        EP = EnzymeParser(Path(""))
        EP.file = file
        return EP.parse()


def test_read_single() -> None:
    enzrxns = read_mock_file(["UNIQUE-ID - ENZRXN-13149", "ENZYME - MONOMER-17831"])
    assert enzrxns["ENZRXN-13149"].enzyme == "MONOMER-17831"
