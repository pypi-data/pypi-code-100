# Face_Localization.py
#
# Copyright 2019 Ryota Higashi
# Copyright 2021 Eiichi Inohira
## This software may be modified and distributed under the terms
# of the MIT license
#
# For python3
# For HRI Component

"""Face_Detection
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

    def set_parameter(self, detection_threshold, minimum_interval):
        arg = [detection_threshold, minimum_interval]
        self.parameter_queue.put(arg)
        self.Detection_Threshold = detection_threshold
        self.Minimum_Interval = minimum_interval

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
        return (status, self.Detection_Threshold, self.Minimum_Interval)
    

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

    def face_localized(self, timestamp, face_ref, position_data):
        """face_localization
        """
        msg = xmlrpc.client.dumps((timestamp, face_ref, position_data), 'face_localized')
        self.event_queue.put(msg)


class Face_Localization(Event, Command, Query):
    """Face_Localization
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
        
        self.Detection_Threshold = 1000
        self.Minimum_Interval = 20

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


def event_dispatch(fl):
    """event_dispatch
    """
    time.sleep(17)
    fl.face_localized(datetime.now().isoformat(), [""], [""])
    time.sleep(0.1)
    fl.face_localized(datetime.now().isoformat(), [""], [""])


def example_fl(port):
    """example_pd
    """
    c = component()
    fl = Face_Localization(c,lock=None)

    # start the timer to dispatch events
    t = threading.Timer(0.1, event_dispatch, args=(fl,))
    t.start()

    # start the XML-RPC server
    IF_server.IF_server(port).run(fl)

if __name__ == '__main__':
    example_fl(8006)