# Move.py
#
# Copyright 2019 Ryota Higashi
# Copyright 2021 Eiichi Inohira
# This software may be modified and distributed under the terms
# of the MIT license
#
# For python3
# For HRI Component

"""Move
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

    def set_parameter(self, line, curve, time):
        arg = [line, curve, time]
        self.parameter_queue.put(arg)
        self.Line = line
        self.Curve = curve
        self.Time = time

        self.th = threading.Thread(target=self.execute, daemon=True)
        self.th.start()
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
        return (status, self.Line, self.Curve, self.Time)
    

class Event(RoIS_Common.Event):
    """Event
    """
    def __init__(self, c):
        self._component = c
        self.event_queue = queue.Queue()

    # def poll_event(self):
    #     """poll_event
    #     """
    #     msg = self.event_queue.get()
    #     return msg


class Move(Event, Command, Query):
    """Move
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

        self.Line = [""]
        self.Curve = [""]
        self.Time = 10
    
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


def event_dispatch(m):
    """event_dispatch
    """


def example_m(port):
    """example_m
    """
    c = component()
    m = Move(c)
    # start the timer to dispatch events
    t = threading.Timer(0.1, event_dispatch, args=(m,))
    t.start()

    # start the XML-RPC server
    IF_server.IF_server(port).run(m)

if __name__ == '__main__':
    example_m(8015)