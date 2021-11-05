from __future__ import annotations

from pathlib import Path

from moped.databases.cyc import _remove_top_comments, _rename

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


def test_remove_top_comments() -> None:
    file = [
        "# Species: MetaCyc",
        "# Database: MetaCyc",
        "# Version: 23.0",
        "# File Name: reactions.dat",
        "# Date and time generated: November 20, 2018, 14:01:26",
        "#",
        "# Attributes:",
        "#    UNIQUE-ID",
        "#    TYPES",
        "#    COMMON-NAME",
        "#    ATOM-MAPPINGS",
        "#    SYSTEMATIC-NAME",
        "#    TAXONOMIC-RANGE",
        "#",
        "UNIQUE-ID - RXN-19177",
    ]

    file, idx = _remove_top_comments(file)
    assert ["UNIQUE-ID - RXN-19177"] == file
    assert idx == 14


def test_rename() -> None:
    assert "O-methylbergaptol" == _rename("<i>O</i>-methylbergaptol")
    assert "N2-acetyl-ornithine" == _rename("<i>N<sup>2</sup></i>-acetyl-ornithine")
    assert "SePO3" == _rename("SePO<sub>3</sub>")
    assert "UDP-2,4-diacetamido-2,4,6-trideoxy-alpha-D-glucopyranose" == _rename(
        "UDP-2,4-diacetamido-2,4,6-trideoxy-&alpha;-D-glucopyranose"
    )
    assert "Glucopyranose" == _rename("|Glucopyranose|")
