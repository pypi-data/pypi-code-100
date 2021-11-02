import pytest
from unittest.mock import call


@pytest.fixture
def shared_kpbig(shared_kp_factory):
    data = shared_kp_factory("db_argon2_kdbx4_pass_big.kdbx", password="foobar")
    data.ioh.print.reset_mock()
    return data


full_ls = [
    call("foo"),
    call("group/entry"),
    call("group/subgroup/entry"),
    call("group/subgroup/other entry"),
    call("other/foo"),
]

group_ls = [
    call("group/entry"),
    call("group/subgroup/entry"),
    call("group/subgroup/other entry"),
]


@pytest.mark.parametrize(
    "glob,expected_prints",
    [
        ("", full_ls),
        ("*", full_ls),
        ("foo", [call("foo")]),
        ("foobar", []),
        ("f*", [call("foo")]),
        ("group/*", group_ls),
    ],
)
def test_ls_glob(shared_kpbig, glob, expected_prints, th):
    th.cmd(f"ls {glob}", shared_kpbig.kp, shared_kpbig.ioh)
    shared_kpbig.ioh.print.assert_has_calls(expected_prints)


def test_show(shared_kpbig, th):
    th.cmd("show foo", shared_kpbig.kp, shared_kpbig.ioh)
    shared_kpbig.ioh.print.assert_has_calls(
        [
            call("path: foo"),
            call("username: myuser"),
            call("password: mypass"),
            call("url: http://example.com"),
            call("autotype_sequence: {USER}{PASSWORD}"),
            call("notes[1]: first note"),
            call("notes[2]: second note"),
        ]
    )


def test_show_n(shared_kpbig, th):
    th.cmd("show foo -n", shared_kpbig.kp, shared_kpbig.ioh)
    shared_kpbig.ioh.print.assert_has_calls(
        [
            call("foo"),
            call("myuser"),
            call("mypass"),
            call("http://example.com"),
            call("{USER}{PASSWORD}"),
            call("first note"),
            call("second note"),
        ]
    )


@pytest.mark.parametrize(
    "field,lines",
    [
        ("path", ["foo"]),
        ("username", ["myuser"]),
        ("password", ["mypass"]),
        ("url", ["http://example.com"]),
        ("autotype_sequence", ["{USER}{PASSWORD}"]),
        ("notes", ["first note", "second note"]),
    ],
)
def test_show_field(shared_kpbig, field, lines, th):
    th.cmd(f"show foo {field}", shared_kpbig.kp, shared_kpbig.ioh)
    expected_calls = (
        [call(f"{field}: {lines[0]}")]
        if len(lines) == 1
        else [call(f"{field}[{i+1}]: {line}") for i, line in enumerate(lines)]
    )
    shared_kpbig.ioh.print.assert_has_calls(expected_calls)

    shared_kpbig.ioh.print.reset_mock()
    th.cmd(f"show -n foo {field}", shared_kpbig.kp, shared_kpbig.ioh)
    expected_calls = [call(line) for line in lines]
    shared_kpbig.ioh.print.assert_has_calls(expected_calls)


def test_show_many_fields_different_order(shared_kpbig, th):
    th.cmd(f"show foo url path", shared_kpbig.kp, shared_kpbig.ioh)
    shared_kpbig.ioh.print.assert_has_calls(
        [call("url: http://example.com"), call("path: foo")]
    )


def test_db(shared_kpbig, th):
    th.cmd("db", shared_kpbig.kp, shared_kpbig.ioh)
    shared_kpbig.ioh.print.assert_has_calls(
        [call(shared_kpbig.args.db), call("Locked: False")]
    )


def test_echo(shared_kpbig, th):
    msg = "foo bar baz"
    th.cmd(f"echo '{msg}'", shared_kpbig.kp, shared_kpbig.ioh)
    shared_kpbig.ioh.print.assert_has_calls([call(msg)])
