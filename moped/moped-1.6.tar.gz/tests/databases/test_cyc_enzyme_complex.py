from __future__ import annotations

from typing import Dict, Set, cast

from moped.databases.cyc import (
    ParseEnzyme,
    ParseReaction,
    _check_for_monomer,
    _get_enzrnx_to_monomer_mapping,
    _get_enzrnx_to_sequence_mapping,
    _map_reactions_to_kinetic_parameters,
    _map_reactions_to_sequences,
)


def test_check_for_monomers_single_layer() -> None:
    enzrxn_to_monomer: Dict[str, Set[str]] = {}
    enzrxn = "ENZRXN-CPLX-1"
    enzrxns: Dict[str, ParseEnzyme] = {
        "ENZRXN-CPLX-1": ParseEnzyme(id="ENZRXN-CPLX-1", enzyme="CPLX-1"),
    }
    monomers = {"MONOMER-1"}
    complexes = {
        "CPLX-1": {"MONOMER-1"},
    }
    _check_for_monomer(
        enzrxn=enzrxn,
        protein=cast(str, enzrxns[enzrxn].enzyme),
        monomers=monomers,
        complexes=complexes,
        enzrxn_to_monomer=enzrxn_to_monomer,
    )
    assert enzrxn_to_monomer == {"ENZRXN-CPLX-1": {"MONOMER-1"}}


def test_check_for_monomers_single_layer_two_monomers() -> None:
    enzrxn_to_monomer: Dict[str, Set[str]] = {}
    enzrxns: Dict[str, ParseEnzyme] = {
        "ENZRXN-CPLX-1": ParseEnzyme(id="ENZRXN-CPLX-1", enzyme="CPLX-1"),
    }
    monomers = {"MONOMER-1", "MONOMER-2"}
    complexes = {
        "CPLX-1": {"MONOMER-1", "MONOMER-2"},
    }
    enzrxn = "ENZRXN-CPLX-1"
    protein = cast(str, enzrxns[enzrxn].enzyme)
    _check_for_monomer(
        enzrxn=enzrxn,
        protein=protein,
        monomers=monomers,
        complexes=complexes,
        enzrxn_to_monomer=enzrxn_to_monomer,
    )
    assert enzrxn_to_monomer == {"ENZRXN-CPLX-1": {"MONOMER-1", "MONOMER-2"}}


def test_check_for_monomers_single_layer_two_monomers_one_missing() -> None:
    enzrxn_to_monomer: Dict[str, Set[str]] = {}
    enzrxns: Dict[str, ParseEnzyme] = {
        "ENZRXN-CPLX-1": ParseEnzyme(id="ENZRXN-CPLX-1", enzyme="CPLX-1"),
    }
    monomers = {"MONOMER-1"}
    complexes = {
        "CPLX-1": {"MONOMER-1", "MONOMER-2"},
    }
    enzrxn = "ENZRXN-CPLX-1"
    protein = cast(str, enzrxns[enzrxn].enzyme)
    _check_for_monomer(
        enzrxn=enzrxn,
        protein=protein,
        monomers=monomers,
        complexes=complexes,
        enzrxn_to_monomer=enzrxn_to_monomer,
    )
    assert enzrxn_to_monomer == {"ENZRXN-CPLX-1": {"MONOMER-1"}}


def test_check_for_monomers_two_layers() -> None:
    enzrxns: Dict[str, ParseEnzyme] = {
        "ENZRXN-CPLX-1": ParseEnzyme(id="ENZRXN-CPLX-1", enzyme="CPLX-2"),
    }

    enzrxn_to_monomer: Dict[str, Set[str]] = {}
    monomers = {"MONOMER-1", "MONOMER-2"}
    complexes = {
        "CPLX-1": {"MONOMER-2"},
        "CPLX-2": {"CPLX-1", "MONOMER-1"},
    }

    enzrxn = "ENZRXN-CPLX-1"
    protein = cast(str, enzrxns[enzrxn].enzyme)

    _check_for_monomer(
        enzrxn=enzrxn,
        protein=protein,
        monomers=monomers,
        complexes=complexes,
        enzrxn_to_monomer=enzrxn_to_monomer,
    )
    assert enzrxn_to_monomer == {"ENZRXN-CPLX-1": {"MONOMER-1", "MONOMER-2"}}


def test_get_enzrnx_to_monomer_mapping() -> None:
    enzrxns: Dict[str, ParseEnzyme] = {
        "ENZRXN-MONO-1": ParseEnzyme(id="ENZRXN-MONO-1", enzyme="MONOMER-1"),
        "ENZRXN-CPLX-1": ParseEnzyme(id="ENZRXN-CPLX-1", enzyme="CPLX-2"),
    }
    monomers = {"MONOMER-1", "MONOMER-2"}
    complexes = {
        "CPLX-1": {"MONOMER-2"},
        "CPLX-2": {"CPLX-1", "MONOMER-1"},
    }
    assert _get_enzrnx_to_monomer_mapping(enzrxns=enzrxns, monomers=monomers, complexes=complexes) == {
        "ENZRXN-MONO-1": {"MONOMER-1"},
        "ENZRXN-CPLX-1": {"MONOMER-1", "MONOMER-2"},
    }


def test_get_enzrnx_to_sequence_mapping() -> None:
    enzrxn_to_monomer = {
        "ENZRXN-MONO-1": {"MONOMER-1"},
        "ENZRXN-CPLX-1": {"MONOMER-2", "MONOMER-3", "MONOMER-MISSING"},
    }
    sequences = {
        "MONOMER-1": "ATGC",
        "MONOMER-2": "TGCA",
        "MONOMER-3": "GCAT",
    }

    assert _get_enzrnx_to_sequence_mapping(enzrxn_to_monomer=enzrxn_to_monomer, sequences=sequences) == {
        "ENZRXN-MONO-1": {"MONOMER-1": "ATGC"},
        "ENZRXN-CPLX-1": {"MONOMER-3": "GCAT", "MONOMER-2": "TGCA"},
    }


def test_map_reactions_to_sequences() -> None:
    enzrxn_to_monomer = {
        "ENZRXN-MONO-1": {"MONOMER-1"},
        "ENZRXN-CPLX-1": {"MONOMER-2", "MONOMER-3"},
    }

    enzrxn_to_sequences = {
        "ENZRXN-MONO-1": {"MONOMER-1": "ATGC"},
        "ENZRXN-CPLX-1": {"MONOMER-2": "TGCA", "MONOMER-3": "GCAT"},
    }

    reactions: Dict[str, ParseReaction] = {
        "RXN-1": ParseReaction(id="RXN-1", base_id="RXN-1", enzymes={"ENZRXN-MONO-1"}),
        "RXN-2": ParseReaction(id="RXN-2", base_id="RXN-2", enzymes={"ENZRXN-CPLX-1"}),
        "RXN-MISSING-1": ParseReaction(
            id="RXN-MISSING-1", base_id="RXN-MISSING-1", enzymes={"ENZRXN-MISSING"}
        ),
        "RXN-MISSING-2": ParseReaction(id="RXN-MISSING-2", base_id="RXN-MISSING-2"),
    }

    _map_reactions_to_sequences(
        reactions=reactions,
        enzrxn_to_monomer=enzrxn_to_monomer,
        enzrxn_to_seq=enzrxn_to_sequences,
    )

    rxn = reactions["RXN-1"]
    assert rxn.enzymes == {"ENZRXN-MONO-1"}
    assert rxn.sequences == {"MONOMER-1": "ATGC"}
    assert rxn.monomers == {"ENZRXN-MONO-1": {"MONOMER-1"}}

    rxn = reactions["RXN-2"]
    assert rxn.enzymes == {"ENZRXN-CPLX-1"}
    assert rxn.sequences == {"MONOMER-2": "TGCA", "MONOMER-3": "GCAT"}
    assert rxn.monomers == {"ENZRXN-CPLX-1": {"MONOMER-3", "MONOMER-2"}}

    rxn = reactions["RXN-MISSING-1"]
    assert rxn.enzymes == {"ENZRXN-MISSING"}
    assert rxn.sequences == {}
    assert rxn.monomers == {"ENZRXN-MISSING": set()}

    rxn = reactions["RXN-MISSING-2"]
    assert rxn.enzymes == set()
    assert rxn.sequences == {}
    assert rxn.monomers == {}


def test_map_reactions_to_kinetic_parameters() -> None:
    reactions: Dict[str, ParseReaction] = {
        "RXN-1": ParseReaction(id="RXN-1", base_id="RXN-1", enzymes={"ENZRXN-MONO-1"}),
        "RXN-2": ParseReaction(id="RXN-2", base_id="RXN-2", enzymes={"ENZRXN-CPLX-1"}),
        "RXN-MISSING-1": ParseReaction(
            id="RXN-MISSING-1", base_id="RXN-MISSING-1", enzymes={"ENZRXN-MISSING"}
        ),
        "RXN-MISSING-2": ParseReaction(id="RXN-MISSING-2", base_id="RXN-MISSING-2"),
    }

    enzrxns: Dict[str, ParseEnzyme] = {
        "ENZRXN-MONO-1": ParseEnzyme(
            id="ENZRXN-MONO-1",
            enzyme="MONOMER-1",
            km={"key": 1.0},
            vmax={"key": 2.0},
        ),
        "ENZRXN-CPLX-1": ParseEnzyme(
            id="ENZRXN-CPLX-1",
            enzyme="CPLX-2",
            kcat={"key": 1.0},
        ),
    }

    _map_reactions_to_kinetic_parameters(
        reactions=reactions,
        enzrxns=enzrxns,
    )

    rxn = reactions["RXN-1"]
    assert rxn.enzymes == {"ENZRXN-MONO-1"}
    assert rxn.enzrxns == {"ENZRXN-MONO-1": {"km": {"key": 1.0}, "vmax": {"key": 2.0}}}

    rxn = reactions["RXN-2"]
    assert rxn.enzymes == {"ENZRXN-CPLX-1"}
    assert rxn.enzrxns == {"ENZRXN-CPLX-1": {"kcat": {"key": 1.0}}}

    rxn = reactions["RXN-MISSING-1"]
    assert rxn.enzymes == {"ENZRXN-MISSING"}
    assert rxn.enzrxns == {}

    rxn = reactions["RXN-MISSING-2"]
    assert rxn.enzymes == set()
    assert rxn.enzrxns == {}
