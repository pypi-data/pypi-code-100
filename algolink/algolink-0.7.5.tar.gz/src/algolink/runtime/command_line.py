from .. import config
from .interface import InterfaceLoader
from .server import Server
from ..utils.log import rlogger


def start_runtime(loader=None, server=None):
    """
    Starts AlgoLink runtime for given (optional) loader and (optional) server

    :param loader: loader of model to start AlgoLink runtime for,
        if not given class specified in :attr:`.config.Runtime.LOADER` is used
    :param server: server to use for AlgoLink runtime, default is a flask-based server,
        if not given class specified in :attr:`.config.Runtime.SERVER` is used
    :return: nothing
    """

    if not isinstance(server, Server):
        server = config.Runtime.SERVER
        server = Server.get(server)

    if not isinstance(loader, InterfaceLoader):
        loader = config.Runtime.LOADER
        loader = InterfaceLoader.get(loader)

    rlogger.info('Starting AlgoLink runtime with loader %s and server %s ...',
                 type(loader).__name__,
                 type(server).__name__)
    server.start(loader)
