# IF_server.py
#
# Copyright 2020 Eiichi Inohira
# This software may be modified and distributed under the terms
# of the MIT license
#
# For python 3

import socketserver
import xmlrpc.server

class ThreadingXMLRPCServer(socketserver.ThreadingMixIn, xmlrpc.server.SimpleXMLRPCServer):
    """ThreadingXMLRPCServer
    """
    pass

class IF_server:
    """IF_Server
    """
    def __init__(self, port):
        self._server = ThreadingXMLRPCServer(
            ("0.0.0.0", port), logRequests=False)

    def run(self, _IF):
        """IF_Server
        """
        self._server.register_instance(_IF)
        self._server.register_introspection_functions()
        # print("server running")
        self._server.serve_forever()
