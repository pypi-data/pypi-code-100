# Service_Application_Base_example.py
#
# Copyright 2017 Eiichi Inohira
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

from . import RoIS_Service

import xmlrpc.client

class Service_Application_Base(RoIS_Service.Service_Application_Base):
    """Service_Application_Base
    """
    def __init__(self):
        self.event_queue = queue.Queue()

    def poll_event(self):
        """poll_event
        """
        msg = self.event_queue.get()
        return msg

    def completed(self, command_id, status):
        msg = xmlrpc.client.dumps((command_id, status), 'completed')
        self.event_queue.put(msg)

    def notify_error(self, error_id, error_type):
        msg = xmlrpc.client.dumps((error_id, error_type), 'notify_error')
        self.event_queue.put(msg)

    def notify_event(self, event_id, event_type, subscribe_id, expire):
        msg = xmlrpc.client.dumps(
            (event_id, event_type, subscribe_id, expire), 'notify_event')
        self.event_queue.put(msg)


if __name__ == '__main__':
    pass
