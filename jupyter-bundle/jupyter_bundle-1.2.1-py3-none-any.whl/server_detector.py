import IPython


def is_jupyter_server_running():
    return IPython.get_ipython().__class__.__name__ == "ZMQInteractiveShell"
