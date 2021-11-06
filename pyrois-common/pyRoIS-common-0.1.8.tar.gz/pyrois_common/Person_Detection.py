# Person_Detection.py
#
# Copyright 2018 Eiichi Inohira
# Copyright 2019 Ryota Higashi
# This software may be modified and distributed under the terms
# of the MIT license
#
# For python3
# For HRI Component

"""Person_Detection
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

    def person_detected(self, timestamp, number):
        """person_detected
        """
        msg = xmlrpc.client.dumps((timestamp, number), 'person_detected')
        self.event_queue.put(msg)

class Person_Detection(Event, Command, Query):
    """Person_Detection
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


def event_dispatch(pd):
    """event_dispatch
    """
    time.sleep(12)
    for x in range(2):
        pd.person_detected(datetime.now().isoformat(), x)
        time.sleep(1)

def example_pd(port):
    """example_pd
    """
    c = component()
    pd = Person_Detection(c)

    # start the timer to dispatch events
    t = threading.Timer(0.1, event_dispatch, args=(pd,))
    t.start()

    # start the XML-RPC server
    IF_server.IF_server(port).run(pd)

if __name__ == '__main__':
    example_pd(8002)