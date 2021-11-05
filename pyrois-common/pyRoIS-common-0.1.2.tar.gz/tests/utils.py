import time
import threading
from multiprocessing import Process, Queue
import unittest
import http
import xmlrpc.client
import logging
import logging.handlers
from datetime import datetime

from pyrois import RoIS_HRI, RoIS_Common, RoIS_Service
from pyrois import Service_Application_IF, Service_Application_Base_sample
from pyrois import HRI_Engine_client, HRI_Engine_sample
from pyrois import Person_Detection_client, Person_Detection
from pyrois import IF_server

def test_engine(port):
    """test_engine
    """
    IF_server.IF_server(port).run(HRI_Engine_sample.IF(HRI_Engine_sample.MyHRIE()))

def event_dispatch(sa):
    """event_dispatch
    """
    sa.completed("0", RoIS_Service.Completed_Status.OK.value)
    time.sleep(0.1)
    sa.notify_error("1", RoIS_Service.ErrorType.ENGINE_INTERNAL_ERROR.value)
    time.sleep(0.1)
    sa.notify_event("2", "sensor", "0", "2100-01-01T00:00:01+09:00")

# def event_dispatch_long(sa):
#     sa.completed("0", RoIS_Service.Completed_Status.OK.value)
#     time.sleep(1)
#     sa.notify_error("0", RoIS_Service.ErrorType.ENGINE_INTERNAL_ERROR.value)
#     time.sleep(60)
#     sa.notify_event("0", "sensor", "0", "2100-01-01T00:00:01+09:00")

def sample_sa(port):
    """sample_sa
    """
    sa = Service_Application_Base_sample.Service_Application_Base()

    # start the timer to dispatch events
    t = threading.Timer(0.1, event_dispatch, args=(sa,))
    t.start()

    # start the XML-RPC server
    IF_server.IF_server(port).run(sa)

def sample_sa_IF(url, q):
    try:
        logger = logging.getLogger('Service_Application_IF')
        logger.setLevel(logging.DEBUG)
        ch = logging.handlers.QueueHandler(q)
        # ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        a = Service_Application_IF.Service_Application_IF(url, logger=logger)
        while True:
            time.sleep(5)
        print("Finished")
    except KeyboardInterrupt:
        print("Interrupted")

def pd_event_dispatch(pd):
    """event_dispatch
    """
    pd.person_detected(datetime.now().isoformat(), 1)
    time.sleep(0.1)
    pd.person_detected(datetime.now().isoformat(), 1)


def sample_pd(port):
    """sample_pd
    """
    c = Person_Detection.component()
    pd = Person_Detection.Person_Detection(c)

    # start the timer to dispatch events
    t = threading.Timer(0.1, pd_event_dispatch, args=(pd,))
    t.start()

    # start the XML-RPC server
    IF_server.IF_server(port).run(pd)