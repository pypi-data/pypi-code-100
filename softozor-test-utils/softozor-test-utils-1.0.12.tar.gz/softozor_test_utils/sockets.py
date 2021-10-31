import socket

from .timing import wait_until


def can_open_socket(host, port, timeout_in_sec=5.0):
    try:
        with socket.create_connection((host, port), timeout=timeout_in_sec):
            return True
    except OSError:
        return False


def host_has_port_open(host, port, timeout_in_sec=120, period_in_sec=5):
    try:
        wait_until(lambda: can_open_socket(host, port),
                   timeout_in_sec=timeout_in_sec, period_in_sec=period_in_sec)
        return True
    except TimeoutError:
        return False
