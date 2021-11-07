import random

import psutil


def unused_port_number(start=49152, shuffle=True) -> int:
    """
    get unused port number.

    :type start: int
    :param start:
    :type shuffle: bool
    :param shuffle:
    :return:
    """
    _ports = [_c.laddr.port for _c in psutil.net_connections() if
              _c.status == 'LISTEN']

    _target = list(range(start, 65536))

    if shuffle:
        random.shuffle(_target)

    for _ in _target:
        if _ not in set(_ports):
            return _

    raise OverflowError("Could not found free port in this environment.")

# EOF
