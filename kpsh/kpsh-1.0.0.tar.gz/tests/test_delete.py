import pytest


@pytest.fixture
def kpbig(kp_factory):
    return kp_factory("db_argon2_kdbx4_pass_big.kdbx", password="foobar")


def test_delete(kpbig, th):
    expected = kpbig.kp.entries.copy()
    del expected["foo"]

    assert "foo" in kpbig.kp.entries
    th.cmd("delete foo", kpbig.kp, kpbig.ioh)
    assert kpbig.kp.entries == expected


def test_dont_delete_missing_entry(kpbig, th):
    expected = kpbig.kp.entries.copy()

    th.cmd(f"delete somethingwhichdoesntexist", kpbig.kp, kpbig.ioh)
    assert kpbig.kp.entries == expected


def test_delete_subgroup(kpbig, th):
    expected = kpbig.kp.entries.copy()
    del expected["other/foo"]

    th.cmd("delete other/foo", kpbig.kp, kpbig.ioh)
    assert kpbig.kp.entries == expected


def test_delete_many(kpbig, th):
    expected = kpbig.kp.entries.copy()
    del expected["foo"]
    del expected["other/foo"]
    del expected["group/subgroup/other entry"]

    th.cmd("delete foo other/foo 'group/subgroup/other entry'", kpbig.kp, kpbig.ioh)
    assert kpbig.kp.entries == expected
