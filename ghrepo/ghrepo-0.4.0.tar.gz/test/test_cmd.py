import json
from pathlib import Path
import subprocess
import sys
from typing import List
from _pytest.capture import CaptureFixture
import pytest
from pytest_mock import MockerFixture
from ghrepo import GHRepo
from ghrepo.__main__ import main

THIS_DIR = str(Path(__file__).parent)


def test_command(
    capsys: CaptureFixture[str],
    local_repo: str,
    mocker: MockerFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(THIS_DIR)
    monkeypatch.setattr(sys, "argv", ["ghrepo"])
    spy = mocker.spy(subprocess, "run")
    main()
    spy.assert_called_once_with(
        ["git", "remote", "get-url", "origin"],
        cwd=None,
        stdout=subprocess.PIPE,
        universal_newlines=True,
        check=True,
    )
    out, err = capsys.readouterr()
    assert out.strip() == local_repo
    assert err == ""


def test_command_json_dir(
    capsys: CaptureFixture[str], local_repo: str, mocker: MockerFixture
) -> None:
    owner, _, name = local_repo.partition("/")
    r = GHRepo(owner, name)
    spy = mocker.spy(subprocess, "run")
    main(["--json", THIS_DIR])
    spy.assert_called_once_with(
        ["git", "remote", "get-url", "origin"],
        cwd=THIS_DIR,
        stdout=subprocess.PIPE,
        universal_newlines=True,
        check=True,
    )
    out, err = capsys.readouterr()
    assert json.loads(out) == {
        "owner": owner,
        "name": name,
        "fullname": local_repo,
        "api_url": r.api_url,
        "clone_url": r.clone_url,
        "git_url": r.git_url,
        "html_url": r.html_url,
        "ssh_url": r.ssh_url,
    }
    assert err == ""


@pytest.mark.parametrize("opts", [[], ["--json"]])
def test_command_non_repo(
    opts: List[str], capsys: CaptureFixture[str], tmp_path: Path
) -> None:
    with pytest.raises(SystemExit) as excinfo:
        main(opts + [str(tmp_path)])
    assert isinstance(excinfo.value.args[0], int)
    out, err = capsys.readouterr()
    assert out == ""
    assert err == ""


@pytest.mark.parametrize("opts", [[], ["--json"]])
def test_command_bad_url(
    opts: List[str], capsys: CaptureFixture[str], mocker: MockerFixture
) -> None:
    m = mocker.patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["git", "remote", "get-url", "origin"],
            returncode=0,
            stdout="git@gist.github.com:cee837802578a4fc8854df60529af98c.git\n",
            stderr=None,
        ),
    )
    with pytest.raises(SystemExit) as excinfo:
        main(opts)
    assert excinfo.value.args == (
        "ghrepo: Invalid GitHub URL:"
        " 'git@gist.github.com:cee837802578a4fc8854df60529af98c.git'",
    )
    m.assert_called_once_with(
        ["git", "remote", "get-url", "origin"],
        cwd=None,
        stdout=subprocess.PIPE,
        universal_newlines=True,
        check=True,
    )
    out, err = capsys.readouterr()
    assert out == ""
    assert err == ""


def test_command_remote(capsys: CaptureFixture[str], mocker: MockerFixture) -> None:
    m = mocker.patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["git", "remote", "get-url", "upstream"],
            returncode=0,
            stdout="git@github.com:jwodder/daemail.git\n",
            stderr=None,
        ),
    )
    main(["--remote", "upstream"])
    m.assert_called_once_with(
        ["git", "remote", "get-url", "upstream"],
        cwd=None,
        stdout=subprocess.PIPE,
        universal_newlines=True,
        check=True,
    )
    out, err = capsys.readouterr()
    assert out == "jwodder/daemail\n"
    assert err == ""
