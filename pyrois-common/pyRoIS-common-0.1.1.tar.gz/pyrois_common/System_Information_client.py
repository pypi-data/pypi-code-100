# System_Information_Client.py
#
# Copyright 2019 Ryota Higashi
# This software may be modified and distributed under the terms
# of the MIT license
#
# For python3
# For HRI Engine

"""System_Information_Client
"""

import threading
# import logging
import xmlrpc.client

from pyrois import RoIS_Common, RoIS_HRI


class Query(RoIS_Common.Query):
    """Query
    """
    def __init__(self, uri):
        self._uri = uri
        self._proxy = xmlrpc.client.ServerProxy(self._uri)

    def robot_position(self):
        (status, timestamp, robot_ref, position_data) = self._proxy.robot_position()
        return(RoIS_HRI.ReturnCode_t(status), timestamp, robot_ref, position_data)

    def engine_status(self):
        (status, e_status, operable_time) = self._proxy.engine_status()
        return (RoIS_HRI.ReturnCode_t(status), RoIS_Common.Component_Status(e_status), operable_time)


class System_Information_Client(Query):
    """System_Information_Client
    """
    def __init__(self, uri):
        self._uri = uri
        self._proxy = xmlrpc.client.ServerProxy(self._uri)