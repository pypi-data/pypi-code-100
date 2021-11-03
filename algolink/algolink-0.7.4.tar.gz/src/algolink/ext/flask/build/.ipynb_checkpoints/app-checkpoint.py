from algolink import start_runtime
from algolink.ext.flask import server

start_runtime()

app = server.current_app

__all__ = ['app']
