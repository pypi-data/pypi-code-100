# Person_Identification.py
#
# Copyright 2019 Ryota Higashi
# Copyright 2021 Eiichi Inohira
# This software may be modified and distributed under the terms
# of the MIT license
#
# For python3
# For HRI Component

"""Person_Identification
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


class Query(RoIS_Common.Query):
    """Query
    """
    def __init__(self, c):
        self._component = c

    def component_status(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        c_status = self.c_status
        return (status, c_status)
    

class Event(RoIS_Common.Event):
    """Event
    """
    def __init__(self, c):
        self._component = c
        self.event_queue = queue.Queue()

    def poll_event(self):
        """poll_event
        """
        msg = self.event_queue.get()
        return msg

    def person_identified(self, timestamp, person_ref):
        """person_identification
        """
        msg = xmlrpc.client.dumps((timestamp, person_ref), 'person_identified')
        self.event_queue.put(msg)


class Person_Identification(Event, Command, Query):
    """Person_Identification
    """
    def __init__(self, c):
        super().__init__(c)
        self._component = c
        self.c_status = RoIS_Common.Component_Status.READY.value


class component:
    """component
    """
    def __init__(self):
        self._state = False


def event_dispatch(pi):
    """event_dispatch
    """
    time.sleep(15)
    pi.person_identified(datetime.now().isoformat(), [""])
    time.sleep(1)
    pi.person_identified(datetime.now().isoformat(), [""])


def example_pi(port):
    """example_pi
    """
    c = component()
    pi = Person_Identification(c)

    # start the timer to dispatch events
    t = threading.Timer(0.1, event_dispatch, args=(pi,))
    t.start()

    # start the XML-RPC server
    IF_server.IF_server(port).run(pi)

if __name__ == '__main__':
    example_pi(8004)