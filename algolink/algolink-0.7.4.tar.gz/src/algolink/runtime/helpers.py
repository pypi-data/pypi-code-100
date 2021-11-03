from ..core.objects import Model
from ..runtime.command_line import start_runtime
from ..runtime.interface import Interface
from ..runtime.interface.ml_model import ModelLoader, model_interface
from ..runtime.server import Server
from ..utils.importing import module_importable


def run_model_server(model: Model, server: Server = None):
    """
    :func:`.start_runtime` wrapper helper which starts AlgoLink runtime for given model and (optional) server

    :param model: model to start AlgoLink runtime for
    :param server: server to use for AlgoLink runtime, default is a flask-based server
    :return: nothing
    """

    if server is None:
        if module_importable('aiohttp') and module_importable('aiohttp_swagger'):
            from ..ext.aiohttp import AIOHTTPServer
            server = AIOHTTPServer()
        elif module_importable('flask') and module_importable('flasgger'):
            from ..ext.flask import FlaskServer
            server = FlaskServer()
        else:
            raise RuntimeError('You need to install flask and flasgger to use test flask server')

    class DummyLoader(ModelLoader):
        def load(self) -> Interface:
            model.ensure_loaded()
            return model_interface(model)

    start_runtime(DummyLoader(), server)
