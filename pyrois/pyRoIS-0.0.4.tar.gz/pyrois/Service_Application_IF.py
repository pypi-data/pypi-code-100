# Service_Application_IF.py
#
# Copyright 2017 Eiichi Inohira
# This software may be modified and distributed under the terms
# of the MIT license
#
# for python 3
# for Service Application

"""Service_Application_IF
"""

import xmlrpc.client
import threading
import time
from . import RoIS_Service


class Service_Application_IF(RoIS_Service.Service_Application_Base):
    """Service_Application_IF
    """
    def __init__(self, uri, logger=None):
        self._uri = uri
        self._e_proxy = xmlrpc.client.ServerProxy(self._uri,verbose=False)
        if logger is not None:
            self.logger = logger
        self.th = threading.Thread(target=self.poll_event)
        self.th.start()

    def poll_event(self):
        """poll_event
        """
        while True:
            try:
                msg = self._e_proxy.poll_event()
            except:
                print('xmlrpc error')
                return
            (params, methodname) = xmlrpc.client.loads(msg)
            if methodname == 'completed' and len(params) == 2:
                self.completed(*params)
            elif methodname == 'notify_error' and len(params) == 2:
                self.notify_error(*params)
            elif methodname == 'notify_event' and len(params) == 4:
                self.notify_event(*params)
            else:
                print("received unknown event or wrong number of parameters")

    def completed(self, command_id, status):
        self.logger.debug('received completed event'
                          + command_id
                          + RoIS_Service.Completed_Status(status).name)

    def notify_error(self, error_id, error_type):
        self.logger.debug('received error event'
                          + error_id
                          + RoIS_Service.ErrorType(error_type).name)

    def notify_event(self, event_id, event_type, subscribe_id, expire):
        self.logger.debug('received event'
                          + event_id
                          + event_type
                          + subscribe_id
                          + expire)


if __name__ == '__main__':
    pass
