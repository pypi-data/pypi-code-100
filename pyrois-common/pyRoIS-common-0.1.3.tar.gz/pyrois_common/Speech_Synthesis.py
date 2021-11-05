# Speech_Synthesis.py
#
# Copyright 2019 Ryota Higashi
# Copyright 2021 Eiichi Inohira
# This software may be modified and distributed under the terms
# of the MIT license
#
# For python3
# For HRI Component

"""Speech_Synthesis
"""

import sys
import queue
import time
from datetime import datetime
import threading
import logging
import xmlrpc.client

from . import Component_Sample
from pyrois import RoIS_Common, RoIS_HRI, IF_server

class Command(RoIS_Common.Command):
    """Command
    """
    def __init__(self, c):
        self._component = c
        
    def start(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        self.c_status = RoIS_Common.Component_Status.BUSY.value
        return status

    def stop(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        self.c_status = RoIS_Common.Component_Status.UNINITIALIZED.value
        return status

    def suspend(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        self.c_status = RoIS_Common.Component_Status.READY.value
        return status

    def resume(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        self.c_status = RoIS_Common.Component_Status.BUSY.value
        return status
    
    def set_parameter(self, speech_text, SSML_text, volume, languages, character):
        arg = [speech_text, SSML_text, volume, languages, character]
        self.parameter_queue.put(arg)
        self.Speech_Text = speech_text
        self.SSML_Text = SSML_text
        self.Volume = volume
        self.Languages = languages
        self.Character = character
        # self.logger.info("Speech_Synthesis set_parameter")
        
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
        #print(c_status)
        # self.logger.info("component_satus:{}".format(c_status))
        return (status, c_status)

    def get_parameter(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        self.c_status = RoIS_Common.Component_Status.READY.value
        return (status, self.Speech_Text, self.SSML_Text,
            self.Volume, self.Languages, self.Character,
            self.Synthesizable_Languages, self.Synthesizable_Characters)
    

class Event(RoIS_Common.Event):
    """Event
    """
    def __init__(self, c):
        self._component = c
        self.event_queue = queue.Queue()

    # def poll_event(self):
    #     """poll_event
    #     """
    #     msg = self.event_queue.get()
    #     return msg


class Speech_Synthesis(Event, Command, Query):
    """Speech_Synthesis
    """
    def __init__(self, c, lock=None):
        if lock is None:
            self._lock = threading.Lock()
        else:
            self._lock = lock
        
        self._component = c
        self.c_status = RoIS_Common.Component_Status.READY.value
        
        self.Speech_Text = ""
        self.SSML_Text = ""
        self.Volume = 10
        self.Languages = ""
        self.Character = ""
        self.Synthesizable_Languages = ("")
        self.Synthesizable_Characters = ("")
        self.parameter_queue = queue.Queue()
        self.comp = Component_Sample.Component_Sample()

        # self.logger = logging.getLogger('Speech_Synthesis_server')
        # self.logger.setLevel(logging.DEBUG)
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
        # self.fh = logging.FileHandler('Speech_Synthesis(many_components_test).log')    # 場合によって変える
        # self.fh.setLevel(logging.DEBUG)
        # self.fh.setFormatter(formatter)
        # self.logger.addHandler(self.fh)

        # self.ch = logging.StreamHandler()
        # self.ch.setLevel(logging.INFO)
        # self.ch.setFormatter(formatter)
        # self.logger.addHandler(self.ch)

        # self.logger.debug("\n\n*****************\n")
        # self.logger.debug("Speech_Synthesis_Server running")

    def execute(self):
        #while True:
        arg = self.parameter_queue.get()
        with self._lock:
            self.c_status = RoIS_Common.Component_Status.BUSY.value
    
        # y = self.comp.Speech_Synthesis(*arg)
        # with self._lock:
        #    self.c_status = y

        # self.logger.info("Speech_Synthesis speech_now")
        time.sleep(1)
        with self._lock:
            self.c_status = RoIS_Common.Component_Status.READY.value


class component:
    """component
    """
    def __init__(self):
        self._state = False


def event_dispatch(ss):
    """event_dispatch
    """


def example_ss(port):
    """example_ss
    """
    c = component()
    lock = threading.Lock()
    ss = Speech_Synthesis(c,lock)

    # start the timer to dispatch events
    # t = threading.Timer(0.1, event_dispatch, args=(ss,))
    # t.start()

    # start the XML-RPC server
    IF_server.IF_server(port).run(ss)

if __name__ == '__main__':
    example_ss(8011)