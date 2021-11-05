# Reaction_Client.py
#
# Copyright 2019 Ryota Higashi
# This software may be modified and distributed under the terms
# of the MIT license
#
# For python3
# For HRI Engine

"""Reaction_Client
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

    def set_parameter(self, reaction_ref):
        s = self._proxy.set_parameter(reaction_ref)
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
        (status, available_reactions, reaction_ref) = self._proxy.get_parameter()
        return (RoIS_HRI.ReturnCode_t(status), available_reactions, reaction_ref)


class Event(RoIS_Common.Event):
    """Event
    """
    def __init__(self, uri):
        self._uri = uri
        self._e_proxy = xmlrpc.client.ServerProxy(self._uri)
        self.events = []
        # if logger is not None:
        #     self.logger = logger


class Reaction_Client(Command, Query, Event):
    """Reaction_Client
    """
    def __init__(self, uri):
        self._uri = uri
        self._proxy = xmlrpc.client.ServerProxy(self._uri)
        self._e_proxy = xmlrpc.client.ServerProxy(self._uri)
        self.events = []
        # self.start_th()