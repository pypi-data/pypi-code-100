# unittest.py
#
# Copyright 2018 Eiichi Inohira
# This software may be modified and distributed under the terms
# of the MIT license
#
# for python 3

"""unittest
"""

import time
import threading
from multiprocessing import Process, Queue
import unittest
import http
import xmlrpc.client
import sysconfig
import logging
import logging.handlers
from datetime import datetime

from . import RoIS_HRI, RoIS_Common, RoIS_Service
from . import Service_Application_IF, Service_Application_Base_example
from . import HRI_Engine_client, HRI_Engine_example
from . import Person_Detection_client, Person_Detection
from . import IF_server

def test_engine(port):
    """test_engine
    """
    IF_server.IF_server(port).run(HRI_Engine_example.IF(HRI_Engine_example.MyHRIE()))

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

def example_sa(port):
    """example_sa
    """
    sa = Service_Application_Base_example.Service_Application_Base()

    # start the timer to dispatch events
    t = threading.Timer(0.1, event_dispatch, args=(sa,))
    t.start()

    # start the XML-RPC server
    IF_server.IF_server(port).run(sa)

def example_sa_IF(url, q):
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


def example_pd(port):
    """example_pd
    """
    c = Person_Detection.component()
    pd = Person_Detection.Person_Detection(c)

    # start the timer to dispatch events
    t = threading.Timer(0.1, pd_event_dispatch, args=(pd,))
    t.start()

    # start the XML-RPC server
    IF_server.IF_server(port).run(pd)

class TestServericeApplicationIF(unittest.TestCase):
    """TestServericeApplicationIF
    """
    def setUp(self):
        # start the server process
        self.ps = Process(target=example_sa, args=(8000,))
        self.ps.start()

    def test_IF(self):
        """ test_IF
        """

        q = Queue()
        # start the client process
        pc = Process(target=example_sa_IF, args=("http://127.0.0.1:8000/", q))
        pc.start()

        time.sleep(1)

        num_events = 0
        while not q.empty():
            msg = q.get()
            num_events += 1
            # print(msg.message)

        if pc.is_alive():
            pc.terminate()

        return self.assertEqual(num_events, 3)

    def tearDown(self):
        # terminate the server process
        if self.ps.is_alive():
            self.ps.terminate()
            while self.ps.is_alive():
                time.sleep(0.1)

class TestHRIEngineIF_integrated(unittest.TestCase):
    """TestHRIEngineIF_integrated
    """
    def setUp(self):
        # start the server process
        self.ps = Process(target=test_engine, args=(8002,))
        self.ps.start()

    def test_IF(self):
        """test_IF
        """

        try:
            a = HRI_Engine_client.IF("http://127.0.0.1:8002/")
            res = [
                a.connect(),
                a.connect(),
                a.get_profile(""),
                a.get_error_detail("0", ""),

                a.search(""),
                a.bind(""),
                a.bind_any(""),
                a.release(""),
                a.get_parameter(""),
                a.set_parameter("", ""),
                a.execute(""),
                a.get_command_result("", ""),

                a.query("", ""),

                a.subscribe("", ""),
                a.unsubscribe(""),
                a.get_event_detail("", ""),

                a.disconnect(),
                a.disconnect(),
                a.bind('')]
        except xmlrpc.client.ProtocolError as err:
            print(err)

        return self.assertEqual(res,
                                [RoIS_HRI.ReturnCode_t.OK,
                                 RoIS_HRI.ReturnCode_t.ERROR,
                                 (RoIS_HRI.ReturnCode_t.OK, "Unsupported"),
                                 (RoIS_HRI.ReturnCode_t.OK, "None"),

                                 (RoIS_HRI.ReturnCode_t.OK, ["None"]),
                                 RoIS_HRI.ReturnCode_t.OK,
                                 (RoIS_HRI.ReturnCode_t.OK, ["None"]),
                                 RoIS_HRI.ReturnCode_t.OK,
                                 (RoIS_HRI.ReturnCode_t.OK, ["None"]),
                                 (RoIS_HRI.ReturnCode_t.OK, "0"),
                                 RoIS_HRI.ReturnCode_t.OK,
                                 (RoIS_HRI.ReturnCode_t.OK, ["None"]),

                                 (RoIS_HRI.ReturnCode_t.OK, ["None"]),

                                 (RoIS_HRI.ReturnCode_t.OK, "0"),
                                 RoIS_HRI.ReturnCode_t.OK,
                                 (RoIS_HRI.ReturnCode_t.OK, ["None"]),

                                 RoIS_HRI.ReturnCode_t.OK,
                                 RoIS_HRI.ReturnCode_t.ERROR,
                                 RoIS_HRI.ReturnCode_t.OK])

    def tearDown(self):
        # terminate the server process
        if self.ps.is_alive():
            self.ps.terminate()

class TestPD(unittest.TestCase):
    """TestPD
    """

    def setUp(self):
        # start the server process
        self.ps = Process(target=example_pd, args=(8003,))
        self.ps.start()

    def test_IF(self):
        """test_IF
        """
        time.sleep(0.2)
        a = Person_Detection_client.Person_Detection_Client("http://127.0.0.1:8003/")
        try:
            res = [
                a.start(),
                a.stop(),
                a.suspend(),
                a.resume(),
                a.component_status(),
                len(a.events)]
        except xmlrpc.client.ProtocolError as err:
            print(err)

        # a.__del__()

        return self.assertEqual(res,
                                [
                                    RoIS_HRI.ReturnCode_t.OK,
                                    RoIS_HRI.ReturnCode_t.OK,
                                    RoIS_HRI.ReturnCode_t.OK,
                                    RoIS_HRI.ReturnCode_t.OK,
                                    (RoIS_HRI.ReturnCode_t.OK, RoIS_Common.Component_Status.UNINITIALIZED),
                                    2])

    def tearDown(self):
        # terminate the server process
        if self.ps.is_alive():
            self.ps.terminate()
            time.sleep(0.1)


if __name__ == '__main__':
    print("python", sysconfig.get_python_version())
    print("platform:", sysconfig.get_platform())
    unittest.main()
