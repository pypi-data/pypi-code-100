from contextlib import contextmanager
import ctypes
import io
import os, sys
import tempfile


libc = ctypes.CDLL(None)
try:
    c_stdout = ctypes.c_void_p.in_dll(libc, 'stdout')
except ValueError as e:
    # If 'stdout' doesn't work try this.
    # On Mac OS X the symbol for standard output in C is '__stdoutp' which is needed for mac users to run this locally
    c_stdout = ctypes.c_void_p.in_dll(libc, '__stdoutp')


@contextmanager
def redirect_stdout2devnull():
    devnull = open(os.devnull, 'wb')

    try:
        stdout_fd = sys.stdout.fileno()
    except ValueError:
        redirect = False
    else:
        redirect = True

        # Flush both the C-level stdout and sys.stdout to print everything that's currently in the buffers
        libc.fflush(c_stdout)
        sys.stdout.flush()

        devnull_fd = devnull.fileno()
        saved_stdout_fd = os.dup(stdout_fd)

        # Make the file descriptor of stdout point to the same file as devnull
        os.dup2(devnull_fd, stdout_fd)

    yield

    if redirect:
        # Change back so that the file descriptor of stdout points to the original file
        os.dup2(saved_stdout_fd, stdout_fd)
        os.close(saved_stdout_fd)
