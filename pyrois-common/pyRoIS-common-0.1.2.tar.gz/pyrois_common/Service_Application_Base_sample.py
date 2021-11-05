# Service_Application_Base_example.py
#
# Copyright 2017 Eiichi Inohira
# Copyright 2019 Ryota Higashi
# This software may be modified and distributed under the terms
# of the MIT license
#
# for python 3
# for HRI Engine

"""Service_Application_Base_example
"""

import sys
import queue
import time
import threading
import logging

from pyrois import RoIS_Service

import socketserver
import xmlrpc.server

class ThreadingXMLRPCServer(socketserver.ThreadingMixIn, xmlrpc.server.SimpleXMLRPCServer):
    """ThreadingXMLRPCServer
    """
    pass


class Service_Application_Base(RoIS_Service.Service_Application_Base):
    """Service_Application_Base
    """
    def __init__(self, logger=None):
        self.event_queue = queue.Queue()
        if logger is not None:
            self.logger = logger

    def poll_event(self):
        """poll_event
        """
        # print("invoked poll")
        self.logger.info("invoked poll")
        msg = self.event_queue.get()
        return msg

    def completed(self, command_id, status):
        # print('completed')
        self.logger.info('***completed***')
        msg = xmlrpc.client.dumps((command_id, status), 'completed')
        self.event_queue.put(msg)

    def notify_error(self, error_id, error_type):
        # print('notify_error')
        self.logger.info('***notify_error***')
        msg = xmlrpc.client.dumps((error_id, error_type), 'notify_error')
        self.event_queue.put(msg)

    def notify_event(self, event_id, event_type, subscribe_id, expire):
        # print('notify_event')
        self.logger.info('***notify_event***')
        msg = xmlrpc.client.dumps(
            (event_id, event_type, subscribe_id, expire), 'notify_event')
        self.event_queue.put(msg)




# def example_sa(port):
#     """example_sa
#     """
#     logger = logging.getLogger('Service_Application_Base_for_sub_HRI_engine')
#     logger.setLevel(logging.DEBUG)
#     # ch = logging.StreamHandler()
#     ch = logging.FileHandler('event_notification_test.log') 
#     ch.setLevel(logging.DEBUG)
#     formatter = logging.Formatter(
#         '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     ch.setFormatter(formatter)
#     logger.addHandler(ch)

#     sa = Service_Application_Base(logger=logger)

#     # start the timer to dispatch events
#     # t = threading.Timer(5, event_dispatch, args=(sa,))
#     # t.start()

#     # start the XML-RPC server
#     server = ThreadingXMLRPCServer(("0.0.0.0", port), logRequests=False)
#     server.register_instance(sa)
#     server.register_introspection_functions()
#     server.register_multicall_functions()
#     # print("server running")
#     server.serve_forever()


# if __name__ == '__main__':
#     example_sa(8016)
