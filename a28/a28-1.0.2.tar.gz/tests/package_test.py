# vim: encoding=utf-8 ts=4 et sts=4 sw=4 tw=79 fileformat=unix nu wm=2
import argparse
import utils
from a28.package import generate_jsondata


def test_a28_package_no_param():
    command = ['a28', 'package']
    out, err, exitcode = utils.capture(command)
    assert exitcode == 2
    assert out == b''
    message = b'usage: a28 package [-h] {init,build,install,publish} ...'
    assert err[0:len(message)] == message


def test_a28_init_no_param():
    command = ['a28', 'package', 'init']
    out, err, exitcode = utils.capture(command)
    assert exitcode == 2
    assert out == b''
    message = b'usage: a28 package init [-h] -s SCOPE -n NAME -t'
    assert err[0:len(message)] == message


def test_a28_build_no_param():
    command = ['a28', 'package', 'build']
    out, err, exitcode = utils.capture(command)
    assert exitcode == 2
    assert out == b''
    message = b'usage: a28 package build [-h] --src SRC [--dest DEST]'
    assert err[0:len(message)] == message


def test_a28_install_no_param():
    command = ['a28', 'package', 'install']
    out, err, exitcode = utils.capture(command)
    assert exitcode == 2
    assert out == b''
    message = b'usage: a28 package install [-h] --pkg PKG'
    assert err[0:len(message)] == message


def test_generate_jsondata_without_args():
    result = generate_jsondata(
        scope="foo", name="bar", identifier="1234", schema="234",
        args=argparse.Namespace(bin="", script="")
    )

    assert result == {
        'description': '234 package created using the A28 command by foo.',
        'identifier': '1234',
        'name': '@foo/bar',
        'version': '0.1.0'
    }


def test_generate_jsondata_with_bin():
    result = generate_jsondata(
        scope="foo", name="bar", identifier="1234", schema="234",
        args=argparse.Namespace(bin="in the bin", script="")
    )

    assert result == {
        'description': '234 package created using the A28 command by foo.',
        'identifier': '1234',
        'name': '@foo/bar',
        'version': '0.1.0',
        'bin': {}
    }


def test_generate_jsondata_with_bin_and_script():
    result = generate_jsondata(
        scope="foo", name="bar", identifier="1234", schema="234",
        args=argparse.Namespace(bin="in the bin", script="the script")
    )

    assert result == {
        'description': '234 package created using the A28 command by foo.',
        'identifier': '1234',
        'name': '@foo/bar',
        'version': '0.1.0',
        'bin': {},
        'scripts': {}
    }
