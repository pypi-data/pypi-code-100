from moped import Reaction


def test_initialize_id() -> None:
    assert Reaction("RXN001").id == "RXN001"


def test_initialize_name() -> None:
    rxn = Reaction("RXN001", name="Reaction")
    assert rxn.name == "Reaction"


def test_initialize_stoichiometries() -> None:
    rxn = Reaction("RXN001", stoichiometries={"X": -1, "Y": 1})
    assert rxn.stoichiometries == {"X": -1, "Y": 1}


def test_initialize_bounds() -> None:
    rxn = Reaction("RXN001", bounds=(-1000, 1000))
    assert rxn.bounds == (-1000, 1000)


def test_initialize_reversible_default() -> None:
    rxn = Reaction("RXN001")
    assert rxn.reversible is False


def test_initialize_reversible_true() -> None:
    rxn = Reaction("RXN001", reversible=True)
    assert rxn.reversible is True


def test_initialize_reversible_false() -> None:
    rxn = Reaction("RXN001", reversible=False)
    assert rxn.reversible is False


def test_initialize_gibbs0() -> None:
    rxn = Reaction("RXN001", gibbs0=1)
    assert rxn.gibbs0 == 1


def test_initialize_ec() -> None:
    rxn = Reaction("RXN001", ec="123")
    assert rxn.ec == "123"


def test_initialize_pathways() -> None:
    rxn = Reaction("RXN001", pathways={"PWY-101"})
    assert rxn.pathways == {"PWY-101"}


def test_transmembrane_both_none() -> None:
    rxn = Reaction(
        id="RXN001_c",
        base_id="RXN001",
        stoichiometries={"X": -1, "Y": 1},
    )
    assert not rxn.transmembrane


def test_transmembrane_both_cytosol() -> None:
    rxn = Reaction(
        id="RXN001_c",
        base_id="RXN001",
        stoichiometries={"X_c": -1, "Y_c": 1},
    )
    assert not rxn.transmembrane


def test_transmembrane_different_compartments() -> None:
    rxn = Reaction(
        id="RXN001_c",
        base_id="RXN001",
        stoichiometries={"X_c": -1, "Y_p": 1},
    )
    assert rxn.transmembrane


def test_iter() -> None:
    rxn = Reaction(
        id="RXN001_c",
        base_id="RXN001",
        stoichiometries={"X_c": -1, "Y_c": 1},
        bounds=(-1000, 1000),
        reversible=True,
        gibbs0=1,
        ec="123",
        pathways={"PWY-101"},
    )
    assert dict(rxn) == {
        "id": "RXN001_c",
        "base_id": "RXN001",
        "stoichiometries": {"X_c": -1, "Y_c": 1},
        "bounds": (-1000, 1000),
        "reversible": True,
        "gibbs0": 1,
        "ec": "123",
        "pathways": {"PWY-101"},
    }


def test_hash() -> None:
    rxn = Reaction(id="RXN001_c")
    assert hash(rxn) == hash("RXN001_c")


def test_comparisons() -> None:
    rxn1 = Reaction(id="RXN001_c")
    rxn2 = Reaction(id="RXN002_c")
    assert rxn1 == rxn1
    assert rxn1 != rxn2
    assert rxn1 <= rxn2
    assert rxn1 < rxn2
    assert rxn2 >= rxn1
    assert rxn2 > rxn1


def test_str() -> None:
    rxn = Reaction(
        id="RXN001_c",
        base_id="RXN001",
        stoichiometries={"X_c": -1, "Y_c": 1},
        bounds=(-1000, 1000),
        reversible=True,
        gibbs0=1,
        ec="123",
        pathways={"PWY-101"},
    )

    assert str(rxn).split("\n") == [
        "Reaction <RXN001_c>",
        "    id: RXN001_c",
        "    base_id: RXN001",
        "    stoichiometries: {'X_c': -1, 'Y_c': 1}",
        "    bounds: (-1000, 1000)",
        "    reversible: True",
        "    gibbs0: 1",
        "    ec: 123",
        "    pathways: {'PWY-101'}",
    ]


def test_repr() -> None:
    rxn = Reaction(
        id="RXN001_c",
        base_id="RXN001",
        stoichiometries={"X_c": -1, "Y_c": 1},
        bounds=(-1000, 1000),
        reversible=True,
        gibbs0=1,
        ec="123",
        pathways={"PWY-101"},
    )

    assert repr(rxn).split(", ") == [
        "Reaction(id='RXN001_c'",
        "base_id='RXN001'",
        "stoichiometries={'X_c': -1",
        "'Y_c': 1}",
        "bounds=(-1000",
        "1000)",
        "reversible=True",
        "gibbs0=1",
        "ec='123'",
        "pathways={'PWY-101'})",
    ]


def test_reverse_stoichiometries_stoichiometries() -> None:
    rxn = Reaction("RXN001", stoichiometries={"X": -1, "Y": 1})
    rxn.reverse_stoichiometry()
    assert rxn.stoichiometries == {"X": 1, "Y": -1}


def test_reverse_stoichiometries_bounds() -> None:
    rxn = Reaction("RXN001", stoichiometries={"X": -1, "Y_e": 1}, bounds=(-50, 100))
    rxn.reverse_stoichiometry()
    assert rxn.bounds == (-100, 50)


def test_reverse_stoichiometries_gibbs0() -> None:
    rxn = Reaction("RXN001", stoichiometries={"X": -1, "Y_e": 1}, gibbs0=-1)
    rxn.reverse_stoichiometry()
    assert rxn.gibbs0 == 1


def test_replace_substrate() -> None:
    v = Reaction("v", stoichiometries={"x": -1, "y": 1})
    v.replace_compound("x", "x1")
    assert v.stoichiometries == {"x1": -1, "y": 1}


def test_replace_product() -> None:
    v = Reaction("v", stoichiometries={"x": -1, "y": 1})
    v.replace_compound("y", "y1")
    assert v.stoichiometries == {"x": -1, "y1": 1}


def test_reaction_reversibility_from_bounds_max() -> None:
    r = Reaction(id="rxn", stoichiometries={"x": -1, "y": 1}, bounds=(-1000, 1000))
    assert r.reversible


def test_reaction_reversibility_from_bounds_upper_one() -> None:
    r = Reaction(id="rxn", stoichiometries={"x": -1, "y": 1}, bounds=(-1, 1))
    assert r.reversible


def test_reaction_reversibility_from_bounds_lower_one() -> None:
    r = Reaction(id="rxn", stoichiometries={"x": -1, "y": 1}, bounds=(-1, 1))
    assert r.reversible


def test_reaction_reversibility_from_bounds_upper_zero() -> None:
    r = Reaction(id="rxn", stoichiometries={"x": -1, "y": 1}, bounds=(-1000, 0))
    assert not r.reversible


def test_reaction_reversibility_from_bounds_lower_zero() -> None:
    r = Reaction(id="rxn", stoichiometries={"x": -1, "y": 1}, bounds=(0, 1000))
    assert not r.reversible


def test_reaction_make_reversible_upper_max() -> None:
    r = Reaction(id="rxn", stoichiometries={"x": -1, "y": 1}, bounds=(0, 1000))
    r.make_reversible()
    assert r.reversible
    assert r.bounds == (-1000, 1000)


def test_reaction_make_reversible_lower_max() -> None:
    r = Reaction(id="rxn", stoichiometries={"x": -1, "y": 1}, bounds=(-1000, 0))
    r.make_reversible()
    assert r.reversible
    assert r.bounds == (-1000, 1000)


def test_reaction_make_reversible_upper_one() -> None:
    r = Reaction(id="rxn", stoichiometries={"x": -1, "y": 1}, bounds=(0, 1))
    r.make_reversible()
    assert r.reversible
    assert r.bounds == (-1, 1)


def test_reaction_make_reversible_lower_one() -> None:
    r = Reaction(id="rxn", stoichiometries={"x": -1, "y": 1}, bounds=(-1, 0))
    r.make_reversible()
    assert r.reversible
    assert r.bounds == (-1, 1)


def test_reaction_make_reversible_already_reversible_max() -> None:
    r = Reaction(id="rxn", stoichiometries={"x": -1, "y": 1}, bounds=(-1000, 1000))
    r.make_reversible()
    assert r.reversible
    assert r.bounds == (-1000, 1000)


def test_reaction_make_reversible_already_reversible_lower_one() -> None:
    r = Reaction(id="rxn", stoichiometries={"x": -1, "y": 1}, bounds=(-1, 1000))
    r.make_reversible()
    assert r.reversible
    assert r.bounds == (-1, 1000)


def test_reaction_make_reversible_already_reversible_upper_one() -> None:
    r = Reaction(id="rxn", stoichiometries={"x": -1, "y": 1}, bounds=(-1000, 1))
    r.make_reversible()
    assert r.reversible
    assert r.bounds == (-1000, 1)


def test_reaction_make_irreversible_upper_max() -> None:
    r = Reaction(id="rxn", stoichiometries={"x": -1, "y": 1}, bounds=(0, 1000))
    r.make_irreversible()
    assert not r.reversible
    assert r.bounds == (0, 1000)


def test_reaction_make_irreversible_lower_max() -> None:
    r = Reaction(id="rxn", stoichiometries={"x": -1, "y": 1}, bounds=(-1000, 0))
    r.make_irreversible()
    assert not r.reversible
    assert r.bounds == (-1000, 0)


def test_reaction_make_irreversible_upper_one() -> None:
    r = Reaction(id="rxn", stoichiometries={"x": -1, "y": 1}, bounds=(0, 1))
    r.make_irreversible()
    assert not r.reversible
    assert r.bounds == (0, 1)


def test_reaction_make_irreversible_lower_one() -> None:
    r = Reaction(id="rxn", stoichiometries={"x": -1, "y": 1}, bounds=(-1, 0))
    r.make_irreversible()
    assert not r.reversible
    assert r.bounds == (-1, 0)


def test_reaction_make_irreversible_reversible_max() -> None:
    r = Reaction(id="rxn", stoichiometries={"x": -1, "y": 1}, bounds=(-1000, 1000))
    r.make_irreversible()
    assert not r.reversible
    assert r.bounds == (0, 1000)


def test_reaction_make_irreversible_reversible_lower_one() -> None:
    r = Reaction(id="rxn", stoichiometries={"x": -1, "y": 1}, bounds=(-1, 1000))
    r.make_irreversible()
    assert not r.reversible
    assert r.bounds == (0, 1000)


def test_reaction_make_irreversible_reversible_upper_one() -> None:
    r = Reaction(id="rxn", stoichiometries={"x": -1, "y": 1}, bounds=(-1000, 1))
    r.make_irreversible()
    assert not r.reversible
    assert r.bounds == (0, 1)
