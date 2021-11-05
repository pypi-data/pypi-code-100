# vim: encoding=utf-8 ts=4 et sts=4 sw=4 tw=79 fileformat=unix nu wm=2
import subprocess
from pathlib import Path
import utils


def test_a28_system_no_param():
    command = ['a28', 'system']
    out, err, exitcode = utils.capture(command)
    assert exitcode == 2
    assert out == b''
    message = b'usage: a28 system [-h] [-p PATH] {exists,clean,path} ...'
    assert err[0:len(message)] == message


def test_a28_exists_no_param_no_config(tmp_path: Path):
    d = tmp_path / 'configuration'
    command = ['a28', 'system', f'--path={d}', 'exists']
    out, _, exitcode = utils.capture(command)
    assert exitcode == 0
    message = b'No configuration exists at '
    message_len = len(message)
    assert out[0:message_len] == message


def test_a28_exists_no_param_config(tmp_path: Path):
    d = tmp_path / 'configuration'
    d.mkdir()
    command = ['a28', 'system', f'--path={d}', 'exists']
    out, _, exitcode = utils.capture(command)
    assert exitcode == 0
    message = b'Configuration exists at '
    message_len = len(message)
    assert out[0:message_len] == message


def test_a28_clean_no_param_no_config(tmp_path: Path):
    d = tmp_path / 'configuration_clean'
    command = ['a28', 'system', f'--path={d}', 'clean', '-f']
    out, _, exitcode = utils.capture(command)
    assert exitcode == 1
    message = b'No configuration to clean at '
    message_len = len(message)
    assert out[0:message_len] == message


def test_a28_clean_no_param_config(tmp_path: Path):
    d = tmp_path / 'configuration_clean'
    d.mkdir()
    command = ['a28', 'system', f'--path={d}', 'clean', '-f']
    out, _, exitcode = utils.capture(command)
    assert exitcode == 0
    message = b'Deleted all files and directories in '
    message_len = len(message)
    assert out[0:message_len] == message


def test_a28_path_minimal(tmp_path: Path):
    d = tmp_path / 'configuration_path'
    command = ['a28', 'system', f'--path={d}', 'path', '--minimal']
    out, _, exitcode = utils.capture(command)
    assert exitcode == 0
    message = d.__bytes__()
    assert out[0:len(message)] == message


def test_a28_path_no_minimal(tmp_path: Path):
    d = tmp_path / 'configuration_path'
    command = ['a28', 'system', f'--path={d}', 'path']
    out, _, exitcode = utils.capture(command)
    assert exitcode == 0
    message = b'Configuration path set to "' + d.__bytes__() + b'".\n'
    assert out[0:len(message)] == message
