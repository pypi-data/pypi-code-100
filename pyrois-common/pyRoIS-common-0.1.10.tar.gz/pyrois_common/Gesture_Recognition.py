# Gesture_Recognition.py
#
# Copyright 2019 Ryota Higashi
# Copyright 2021 Eiichi Inohira
# This software may be modified and distributed under the terms
# of the MIT license
#
# For python3
# For HRI Component

"""Gesture_Recognition
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
        with self._lock:
            c_status = self.c_status
        return (status, c_status)
    
    def get_parameter(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        return (status, self.Recognizable_Gestures)
    

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

    def gesture_recognized(self, timestamp, gesture_ref):
        """gesture_recognition
        """
        msg = xmlrpc.client.dumps((timestamp, gesture_ref), 'gesture_recognized')
        self.event_queue.put(msg)


class Gesture_Recognition(Event, Command, Query):
    """Gesture_Recognition
    """
    def __init__(self, c, lock=None):
        super().__init__(c)
        self._component = c
        if lock is None:
            self._lock = threading.Lock()
        else:
            self._lock = lock
        self.c_status = RoIS_Common.Component_Status.READY.value
        self.Recognizable_Gestures = set("")


class component:
    """component
    """
    def __init__(self):
        self._state = False


def event_dispatch(gr):
    """event_dispatch
    """
    # gr.gesture_recognized(datetime.now().isoformat(), [""])
    # time.sleep(0.1)
    # gr.gesture_recognized(datetime.now().isoformat(), [""])


def example_gr(port):
    """example_gr
    """
    c = component()
    gr = Gesture_Recognition(c, lock=None)

    # start the timer to dispatch events
    t = threading.Timer(0.1, event_dispatch, args=(gr,))
    t.start()

    # start the XML-RPC server
    IF_server.IF_server(port).run(gr)

if __name__ == '__main__':
    example_gr(8010)