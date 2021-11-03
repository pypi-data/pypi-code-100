import utils


def test_a28_no_param():
    command = ['a28']
    out, err, exitcode = utils.capture(command)
    assert exitcode == 2
    assert out == b''
    message = b'usage: a28 [-h] [-v] {api,package,pkg,system,sys,account}'
    assert err[0:len(message)] == message


def test_a28_version_param():
    command = ['a28', '-v']
    out, err, exitcode = utils.capture(command)
    assert exitcode == 0
    message = b'a28 version '
    assert out[0:len(message)] == message
    message = b''
    assert err[0:len(message)] == message
