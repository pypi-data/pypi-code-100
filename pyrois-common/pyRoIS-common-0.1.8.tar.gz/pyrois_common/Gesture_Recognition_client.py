# Gesture_Recognition_Client.py
#
# Copyright 2019 Ryota Higashi
# This software may be modified and distributed under the terms
# of the MIT license
#
# For python3
# For HRI Engine

"""Gesture_Recognition_Client
"""

import threading
# import logging
import xmlrpc.client

from pyrois import RoIS_Common, RoIS_HRI


class Command(RoIS_Common.Command):
    """Command
    """
    def __init__(self, uri):
        self._uri = uri
        self._proxy = xmlrpc.client.ServerProxy(self._uri)

    def start(self):
        status = RoIS_HRI.ReturnCode_t(self._proxy.start())
        return status

    def stop(self):
        status = RoIS_HRI.ReturnCode_t(self._proxy.stop())
        return status

    def suspend(self):
        status = RoIS_HRI.ReturnCode_t(self._proxy.suspend())
        return status

    def resume(self):
        status = RoIS_HRI.ReturnCode_t(self._proxy.resume())
        return status
    

class Query(RoIS_Common.Query):
    """Query
    """
    def __init__(self, uri):
        self._uri = uri
        self._proxy = xmlrpc.client.ServerProxy(self._uri)

    def component_status(self):
        (status, c_status) = self._proxy.component_status()
        return (RoIS_HRI.ReturnCode_t(status), RoIS_Common.Component_Status(c_status))
    
    def get_parameter(self):
        (status, recognizable_gestures) = self._proxy.get_parameter()
        return (RoIS_HRI.ReturnCode_t(status), recognizable_gestures)


class Event(RoIS_Common.Event):
    """Event
    """
    def __init__(self, uri):
        self._uri = uri
        self._e_proxy = xmlrpc.client.ServerProxy(self._uri)
        self.events = []
        # if logger is not None:
        #     self.logger = logger
                
    def start_th(self):
        self.th = threading.Thread(target=self.event_loop, daemon=True)
        self.th.start()

    def event_loop(self):
        """event_loop
        """
        while True:
            try:
                self.poll_event()
            except ConnectionRefusedError:
                break

    def poll_event(self):
        """poll_event
        """
        msg = self._e_proxy.poll_event()
        (params, methodname) = xmlrpc.client.loads(msg)
        #self.logger.debug('poll_event: '+methodname)
        # print(params,methodname)
        if methodname == 'gesture_recognized':
            self.gesture_recognized(params[0], params[1])

    def gesture_recognized(self, timestamp, gesture_ref):
        self.events.append((timestamp,gesture_ref))
        # print("gesture_recognized",timestamp, gesture_ref)
        if self.q is not None:
            self.q.put(("gesture_recognized",timestamp, gesture_ref))
        # self.logger.debug('received completed event'
        #                 + command_id
        #                 + RoIS_Service.Completed_Status(status).name)


class Gesture_Recognition_Client(Command, Query, Event):
    """Gesture_Recognition_Client
    """
    def __init__(self, uri, q=None):
        self._uri = uri
        self._proxy = xmlrpc.client.ServerProxy(self._uri)
        self._e_proxy = xmlrpc.client.ServerProxy(self._uri)
        self.events = []
        self.q = q
        self.start_th()