import sys


def is_jupyter_server_running():
    return "ipykernel" in sys.modules
