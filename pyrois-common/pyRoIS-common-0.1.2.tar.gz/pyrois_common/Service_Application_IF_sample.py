# Service_Application_IF.py
#
# Copyright 2017 Eiichi Inohira
# This software may be modified and distributed under the terms
# of the MIT license
#
# for python 3
# for Service Application

"""Service_Application_IF_for_Sub_HRI_Engine
"""


import xmlrpc.client
import threading
import logging
import logging.handlers

import queue
import time

from pyrois import RoIS_Service,RoIS_Common

class Service_Application_IF(RoIS_Service.Service_Application_Base):
    """Service_Application_IF
    """
    def __init__(self, uri, logger=None, event_queue=None):
        self._uri_sa = uri
        self._proxy_sa = xmlrpc.client.ServerProxy(self._uri_sa)
        self.logger = logger
        if event_queue is not None:
            self.event_q = event_queue
        else:
            self.event_q = queue.Queue()
        self.t = threading.Thread(target=self.poll_event,daemon=True)
        self.t.start()

        self.logger.info("Service_Application_IF_sample.Service_Application_IF(): complete init")


    def poll_event(self):
        """poll_event
        """
        # print("sa: poll_event")
        while True:
            try:
                msg = self._proxy_sa.poll_event()
                # print("sa: try poll_event")
            except ConnectionRefusedError:
                # print("sa: error poll_event")
                self.logger.debug("poll_event: xmlrpc error")
                return
            (params, methodname) = xmlrpc.client.loads(msg)
            self.logger.info('poll_event: '+methodname)
            if methodname == 'completed' and len(params) == 2:
                self.completed(*params)
            elif methodname == 'notify_error' and len(params) == 2:
                self.notify_error(*params)
            elif methodname == 'notify_event' and len(params) == 4:
                self.notify_event(*params)
            else:
                self.logger.error("poll_event: received unknown event or wrong number of parameters")
    
    def get_event(self,timeout=None):
        (params, methodname) = self.event_q.get(timeout=timeout)
        return (params, methodname)

    def completed(self, command_id, status):
        s = RoIS_Service.Completed_Status(status)
        self.event_q.put(((command_id, s), 'completed'))
        self.logger.info('received completed event: {} {}'.format(command_id, RoIS_Service.Completed_Status(status).name))

    def notify_error(self, error_id, error_type):
        e = RoIS_Service.ErrorType(error_type)
        self.event_q.put(((error_id, e), 'notify_error'))
        self.logger.info('received error event: {} {}'.format(error_id, RoIS_Service.ErrorType(error_type).name))

    def notify_event(self, event_id, event_type, subscribe_id, expire):
        self.event_q.put(((event_id, event_type, subscribe_id, expire), 'notify_event'))
        self.logger.info('received event: {} {} {} {}'.format(event_id,event_type,subscribe_id,expire))


# def example_sa_IF(url, q):
#     try:
#         logger = logging.getLogger('Service_Application_IF_for_sub_HRI_engine')
#         logger.setLevel(logging.DEBUG)
#         # ch = logging.handlers.QueueHandler(q)
#         # ch = logging.StreamHandler()
#         ch = logging.FileHandler('event_notification_test.log')
#         ch.setLevel(logging.DEBUG)
#         formatter = logging.Formatter(
#             '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#         ch.setFormatter(formatter)
#         logger.addHandler(ch)
#         a = Service_Application_IF(url, logger=logger)
#         time.sleep(20)
#     except KeyboardInterrupt:
#         print("Interrupted")


# if __name__ == '__main__':
#     q = queue.Queue()
#     example_sa_IF('http://127.0.0.1:8016',q)
#     time.sleep(60)

