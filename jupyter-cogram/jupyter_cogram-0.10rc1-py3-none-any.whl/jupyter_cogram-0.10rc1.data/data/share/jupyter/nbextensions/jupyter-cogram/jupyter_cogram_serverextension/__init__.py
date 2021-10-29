import logging

from notebook.utils import url_path_join

from jupyter_cogram.jupyter_cogram_serverextension.server import (
    JupyterCogramConfigHandler,
    JupyterCogramEventHandler,
    AsyncJupyterCogramHandler,
    JupyterCogramTokenHandler,
    JupyterCogramVersionHandler,
    JupyterUpgradeCogramHandler,
    JupyterCogramLaunchHandler,
)
from jupyter_cogram.jupyter_cogram_serverextension.utils import debug_mode

if debug_mode:
    logging.basicConfig(level=logging.DEBUG)

logger: logging.Logger = logging.getLogger(__name__)


def load_jupyter_server_extension(nb_server_app) -> None:
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication):
        handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    host_pattern = ".*$"
    web_app.add_handlers(
        host_pattern,
        [
            (url_path_join(web_app.settings["base_url"], uri), handler)
            for uri, handler in [
                ("/config", JupyterCogramConfigHandler),
                ("/event", JupyterCogramEventHandler),
                ("/cogram", AsyncJupyterCogramHandler),
                ("/token", JupyterCogramTokenHandler),
                ("/checkVersion", JupyterCogramVersionHandler),
                ("/upgrade", JupyterUpgradeCogramHandler),
                ("/launch", JupyterCogramLaunchHandler),
            ]
        ],
    )
    logger.debug("loaded_jupyter_server_extension: jupyter-cogram")
