# System_Information.py
#
# Copyright 2019 Ryota Higashi
# Copyright 2021 Eiichi Inohira
# This software may be modified and distributed under the terms
# of the MIT license
#
# For python3
# For HRI Component

"""System_Information
"""

import sys
import queue
import time
from datetime import datetime
import threading
import xmlrpc.client

from pyrois import RoIS_Common, RoIS_HRI, IF_server

class Query(RoIS_Common.Query):
    """Query
    """
    def __init__(self, c):
        self._component = c
    
    def robot_position(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        timestamp = "2100-01-01T00:00:01+09:00"
        robot_ref = ["urn:x-rois:def:HRIComponent:Kyutech::robot1"]  # codebook, version
        position_data = ["33°53′41″", "130°50′30″"]
        return(status, timestamp, robot_ref, position_data)

    def engine_status(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        e_status = RoIS_Common.Component_Status.READY.value
        operable_time = ["2100-01-01T00:00:01+09:00","2100-01-01T00:00:01+09:00"]
        return (status, e_status, operable_time)


class System_Information(Query):
    """System_Information
    """
    def __init__(self, c):
        self._component = c


class component:
    """component
    """
    def __init__(self):
        self._state = False


def event_dispatch(pd):
    """event_dispatch
    """

def example_si(port):
    """example_si
    """
    c = component()
    si = System_Information(c)

    # start the timer to dispatch events
    # t = threading.Timer(0.1, event_dispatch, args=(si,))
    # t.start()

    # start the XML-RPC server
    IF_server.IF_server(port).run(si)

if __name__ == '__main__':
    example_si(8001)


