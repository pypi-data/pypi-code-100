# Sound_Localization_Client.py
#
# Copyright 2019 Ryota Higashi
# This software may be modified and distributed under the terms
# of the MIT license
#
# For python3
# For HRI Engine

"""Sound_Localization_Client
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

    def set_parameter(self, detection_threshold, minimum_interval):
        s = self._proxy.set_parameter(detection_threshold, minimum_interval)
        status = RoIS_HRI.ReturnCode_t(s)
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
        (status, detection_threshold, minimum_interval) = self._proxy.get_parameter()
        return (RoIS_HRI.ReturnCode_t(status), detection_threshold, minimum_interval)


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
        if methodname == 'sound_localized':
            self.sound_localized(params[0], params[1], params[2])

    def sound_localized(self, timestamp, sound_ref, position_data):
        self.events.append((timestamp,sound_ref,position_data))
        # print("sound_localized",timestamp, sound_ref, position_data)
        if self.q is not None:
            self.q.put(("sound_localized",timestamp, sound_ref, position_data))
        # self.logger.debug('received completed event'
        #                 + command_id
        #                 + RoIS_Service.Completed_Status(status).name)


class Sound_Localization_Client(Command, Query, Event):
    """Sound_localization_Client
    """
    def __init__(self, uri, q=None):
        self._uri = uri
        self._proxy = xmlrpc.client.ServerProxy(self._uri)
        self._e_proxy = xmlrpc.client.ServerProxy(self._uri)
        self.events = []
        self.q = q
        self.start_th()