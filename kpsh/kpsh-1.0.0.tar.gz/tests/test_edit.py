import os
import string

import pytest

from kpsh.commands import CommandError


@pytest.fixture
def kpbig(kp_factory):
    return kp_factory("db_argon2_kdbx4_pass_big.kdbx", password="foobar")


@pytest.fixture
def shared_kpbig(shared_kp_factory):
    data = shared_kp_factory("db_argon2_kdbx4_pass_big.kdbx", password="foobar")
    data.ioh.print.reset_mock()
    return data


def test_edit_nothing(kpbig, th):
    expected = th.fields("foo", kpbig.kp).copy()
    th.cmd("edit foo", kpbig.kp, kpbig.ioh)
    assert th.fields("foo", kpbig.kp) == expected


@pytest.mark.parametrize(
    "field,switch,value",
    [
        ("username", "--username", "editeduser"),
        ("password", "--password", "editedpassword"),
        ("url", "--url", "editeturl"),
        ("autotype_sequence", "--autotype-sequence", "{TAB}{TAB}{TAB}"),
    ],
)
def test_edit_fields(kpbig, th, field, switch, value):
    expected = th.fields("foo", kpbig.kp).copy()
    assert expected[field] != value
    expected[field] = value

    th.cmd(f"edit foo {switch} {value}", kpbig.kp, kpbig.ioh)
    assert th.fields("foo", kpbig.kp) == expected


@pytest.mark.parametrize(
    "path", ["foo", "group/entry", "'group/subgroup/other entry'", "other/foo"]
)
def test_edit_fields_paths(kpbig, th, path):
    expected = th.fields(path, kpbig.kp).copy()
    expected["url"] = "newurl"

    th.cmd(f"edit {path} -U newurl", kpbig.kp, kpbig.ioh)
    assert th.fields(path, kpbig.kp) == expected


def test_edit_many_fields(kpbig, th):
    expected = th.fields("foo", kpbig.kp).copy()
    expected["username"] = "euser"
    expected["url"] = "eurl"
    expected["password"] = "epwd"

    th.cmd(f"edit foo -p epwd -U eurl -u euser ", kpbig.kp, kpbig.ioh)
    assert th.fields("foo", kpbig.kp) == expected


def test_edit_password_interactively(kpbig, th):
    expected = th.fields("foo", kpbig.kp).copy()
    expected["password"] = "editedpassword"
    kpbig.ioh.prompt.return_value = expected["password"]

    th.cmd(f"edit foo --askpass", kpbig.kp, kpbig.ioh)
    assert th.fields("foo", kpbig.kp) == expected


@pytest.mark.parametrize(
    "field,switch",
    [
        ("username", "--username"),
        ("url", "--url"),
        ("autotype_sequence", "--autotype-sequence"),
    ],
)
def test_edit_unset_fields(kpbig, th, field, switch):
    th.cmd(f"edit foo {switch} ''", kpbig.kp, kpbig.ioh)
    assert not th.fields("foo", kpbig.kp).get(field)


def test_edit_generate_password(kpbig, th):
    th.cmd(f"edit foo --pw-gen -l 32", kpbig.kp, kpbig.ioh)
    fields = th.fields("foo", kpbig.kp)
    assert len(fields["password"]) == 32


@pytest.mark.parametrize(
    "arg,chset",
    [
        ("--letters", string.ascii_letters),
        ("--digits", string.digits),
        ("--punctuation", string.punctuation),
        ("--characters abc", ["a", "b", "c"]),
    ],
)
def test_edit_generate_password_character_sets(kpbig, th, arg, chset):
    th.cmd(f"edit foo --pw-gen -l 100 {arg}", kpbig.kp, kpbig.ioh)

    fields = th.fields("foo", kpbig.kp)
    assert len(fields["password"]) == 100

    for ch in fields["password"]:
        assert (
            ch in chset
        ), f"'{ch}' is in set of letters allowed for generated password"


def test_edit_add_notes(kpbig, th):
    existing = th.fields("foo", kpbig.kp)["notes"]

    th.cmd("edit foo --note 'note 1'", kpbig.kp, kpbig.ioh)
    expected = existing + ["note 1"]
    assert th.fields("foo", kpbig.kp)["notes"] == expected

    th.cmd("edit foo --note 'note 2' --note 'note 3'", kpbig.kp, kpbig.ioh)
    expected = existing + ["note 1", "note 2", "note 3"]
    assert th.fields("foo", kpbig.kp)["notes"] == expected


@pytest.mark.parametrize(
    "pattern,expected",
    [
        ("1", ["2", "3", "4", "5"]),
        ("2", ["1", "3", "4", "5"]),
        ("5", ["1", "2", "3", "4"]),
        ("6", ["1", "2", "3", "4", "5"]),
        ("2-6", ["1"]),
    ],
)
def test_delete_notes(kpbig, th, pattern, expected):
    th.cmd("add tabula_rasa -p pwd -n1 -n2 -n3 -n4 -n5", kpbig.kp, kpbig.ioh)
    th.cmd(f"edit tabula_rasa --delete-note {pattern}", kpbig.kp, kpbig.ioh)
    assert th.fields("tabula_rasa", kpbig.kp)["notes"] == expected


@pytest.mark.parametrize("pattern", ["*", "1-5", "1-6"])
def test_delete_all_notes(kpbig, th, pattern):
    th.cmd("add tabula_rasa -p pwd -n1 -n2 -n3 -n4 -n5", kpbig.kp, kpbig.ioh)
    th.cmd(f"edit tabula_rasa --delete-note {pattern}", kpbig.kp, kpbig.ioh)
    assert "notes" not in th.fields("tabula_rasa", kpbig.kp)


@pytest.mark.parametrize(
    "pattern", ["0", "a", "0-1", "1-", "-", "-0", "-1", ",", "**", "1*"]
)
def test_delete_notes_incorrect_argument(shared_kpbig, th, pattern):
    th.cmd("edit foo -n1 -n2 -n3 -n4 -n5", shared_kpbig.kp, shared_kpbig.ioh)
    expected = th.fields("foo", shared_kpbig.kp).copy()

    cmd = f"edit foo --delete-note {pattern}"
    with pytest.raises(CommandError):
        th.cmd(cmd, shared_kpbig.kp, shared_kpbig.ioh)

    assert th.fields("foo", shared_kpbig.kp) == expected


def test_edit_add_delete_together(kpbig, th):
    existing = th.fields("foo", kpbig.kp)["notes"]
    assert existing

    th.cmd("edit foo -N * -n 'note 1'", kpbig.kp, kpbig.ioh)
    expected = ["note 1"]
    assert th.fields("foo", kpbig.kp)["notes"] == expected


def test_edit_detect_file_modification(kpbig, th, kp_open):
    def modify_db_and_answer_password(text, is_password):
        assert is_password is True
        db = kpbig.args.db
        curr = os.stat(db)
        os.utime(db, (curr.st_atime, curr.st_mtime + 100))
        return "pwd"

    expected_unchanged = th.fields("foo", kpbig.kp).copy()

    kpbig.ioh.prompt.side_effect = modify_db_and_answer_password
    th.cmd(f"edit foo --askpass", kpbig.kp, kpbig.ioh)

    assert kpbig.kp.db != kpbig.args.db
    assert os.path.exists(kpbig.args.db)
    assert os.path.exists(kpbig.kp.db)

    oldkp = kp_open(kpbig.args.db, password="foobar")
    assert th.fields("foo", oldkp.kp) == expected_unchanged

    newkp_fields = th.fields("foo", kpbig.kp)
    assert newkp_fields
    assert newkp_fields["password"] == "pwd"


@pytest.mark.parametrize("path", ["'missing path'", "missing", "foo/missing"])
def test_edit_not_existing_path(shared_kpbig, th, path):
    assert path not in shared_kpbig.kp.entries
    with pytest.raises(CommandError):
        th.cmd(f"edit {path} -p pwd", shared_kpbig.kp, shared_kpbig.ioh)
