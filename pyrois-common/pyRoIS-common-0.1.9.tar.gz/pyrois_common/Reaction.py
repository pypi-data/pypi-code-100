# Reaction.py
#
# Copyright 2019 Ryota Higashi
# Copyright 2021 Eiichi Inohira
# This software may be modified and distributed under the terms
# of the MIT license
#
# For python3
# For HRI Component

"""Reaction
"""

import sys
import queue
import time
from datetime import datetime
import threading
import xmlrpc.client

from pyrois import RoIS_Common, RoIS_HRI, IF_server

class Command(RoIS_Common.Command):
    """Command
    """
    def __init__(self, c):
        self._component = c

    def start(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        return status

    def stop(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        return status

    def suspend(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        return status

    def resume(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        return status

    def set_parameter(self, reaction_ref):
        arg = [reaction_ref]
        self.parameter_queue.put(arg)
        self.Reaction_Ref = reaction_ref

        th = threading.Thread(target=self.execute, daemon=True)
        th.start()
        status = RoIS_HRI.ReturnCode_t.OK.value
        return status


class Query(RoIS_Common.Query):
    """Query
    """
    def __init__(self, c):
        self._component = c

    def component_status(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        with self._lock:
            c_status = self.c_status
        return (status, c_status)
    
    def get_parameter(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        self.c_status = RoIS_Common.Component_Status.READY.value
        return (status, self.Available_Reactions, self.Reaction_Ref)
    

class Event(RoIS_Common.Event):
    """Event
    """
    def __init__(self, c):
        self._component = c
        self.event_queue = queue.Queue()


class Reaction(Event, Command, Query):
    """Reaction
    """
    def __init__(self, c, lock=None):
        super().__init__(c)
        self._component = c
        if lock is None:
            self._lock = threading.Lock()
        else:
            self._lock = lock
        
        self.c_status = RoIS_Common.Component_Status.READY.value
        self.parameter_queue = queue.Queue()
        
        self.Reaction_Ref = ""
        self.Available_Reactions = set("")

    def execute(self):  # dummy
        """execute component
        """
        arg = self.parameter_queue.get()
        with self._lock:
            self.c_status = RoIS_Common.Component_Status.BUSY.value

        time.sleep(1)

        with self._lock:
            self.c_status = RoIS_Common.Component_Status.READY.value


class component:
    """component
    """
    def __init__(self):
        self._state = False


def event_dispatch(r):
    """event_dispatch
    """


def example_r(port):
    """example_r
    """
    c = component()
    r = Reaction(c)

    # start the timer to dispatch events
    t = threading.Timer(0.1, event_dispatch, args=(r,))
    t.start()

    # start the XML-RPC server
    IF_server.IF_server(port).run(r)

if __name__ == '__main__':
    example_r(8012)