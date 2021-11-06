# unittest_main_sub_engine4.py
#
# Copyright 2020 Ryota Higashi
# This software may be modified and distributed under the terms
# of the MIT license
#
# for python 3

"""unittest サブエンジンが複数存在する時のテスト
"""

import time
from multiprocessing import Process, Queue
import unittest
import xmlrpc.client
import sys
import re
import logging
import platform
import atexit

from pyrois import RoIS_HRI, RoIS_Common, RoIS_Service
from pyrois_common import HRI_Engine_sample, HRI_Engine_client_sample

from pyrois_common import System_Information
from pyrois_common import Person_Detection
from pyrois_common import Person_Localization
from pyrois_common import Person_Identification
from pyrois_common import Face_Detection
from pyrois_common import Face_Localization
from pyrois_common import Sound_Detection
from pyrois_common import Sound_Localization
from pyrois_common import Speech_Recognition
from pyrois_common import Gesture_Recognition
from pyrois_common import Speech_Synthesis
from pyrois_common import Reaction
from pyrois_common import Navigation
from pyrois_common import Follow
from pyrois_common import Move

eng_profile = """<?xml version="1.0" encoding="UTF-8"?>
<!-->
Robotic Interaction Service Framework Version 1.2
    > Annex A: Examples of Profile in XML
        > A.4 HRI Engine Profile (p.103 (PDF:p.116)) reference
<-->

<rois:HRIEngineProfile gml:id="engine_profile"
    xmlns:rois="http://www.omg.org/spec/RoIS/20151201"
    xmlns:gml="http://www.opengis.net/gml/3.2">
    <gml:identifier>urn:x-rois:def:HRIEngine:Kyutech::main</gml:identifier>
    <gml:name>main</gml:name>
    <rois:SubProfile>
        <gml:identifier>urn:x-rois:def:HRIEngine:Kyutech::sub01</gml:identifier>
        <gml:name>sub01</gml:name>
        <rois:HRIComponent>urn:x-rois:def:HRIComponent:Kyutech:sub01:PersonDetection</rois:HRIComponent>
        <rois:HRIComponent>urn:x-rois:def:HRIComponent:Kyutech:sub01:PersonIdentification</rois:HRIComponent>
        <rois:HRIComponent>urn:x-rois:def:HRIComponent:Kyutech:sub01:SpeechSynthesis</rois:HRIComponent>
        <rois:HRIComponent>urn:x-rois:def:HRIComponent:Kyutech:sub01:Follow</rois:HRIComponent>
    </rois:SubProfile>
    <rois:SubProfile>
        <gml:identifier>urn:x-rois:def:HRIEngine:Kyutech::sub02</gml:identifier>
        <gml:name>sub02</gml:name>
        <rois:HRIComponent>urn:x-rois:def:HRIComponent:Kyutech:sub02:FaceDetection</rois:HRIComponent>
        <rois:HRIComponent>urn:x-rois:def:HRIComponent:Kyutech:sub02:FaceLocalization</rois:HRIComponent>
        <rois:HRIComponent>urn:x-rois:def:HRIComponent:Kyutech:sub02:Navigation</rois:HRIComponent>
    </rois:SubProfile>
    <rois:SubProfile>
        <gml:identifier>urn:x-rois:def:HRIEngine:Kyutech::sub03</gml:identifier>
        <gml:name>sub03</gml:name>
        <rois:HRIComponent>urn:x-rois:def:HRIComponent:Kyutech:sub03:PersonDetection</rois:HRIComponent>
        <rois:HRIComponent>urn:x-rois:def:HRIComponent:Kyutech:sub03:Move</rois:HRIComponent>
    </rois:SubProfile>
</rois:HRIEngineProfile>"""

right_event_result = {
    (('sub01-6', RoIS_Service.Completed_Status.OK), 'completed'), # completed
    (('sub02-5', RoIS_Service.Completed_Status.OK), 'completed'), # completed
    (('sub03-3', RoIS_Service.Completed_Status.OK), 'completed'), # completed
    
    (('sub01-1', 'person_detected', '1'), 'notify_event'),
    (('sub01-2', 'person_detected', '1'), 'notify_event'),
    (('sub01-3', 'person_identified', '2'), 'notify_event'),
    (('sub01-4', 'person_identified', '2'), 'notify_event'),
    (('sub02-1', 'face_localized', '4'), 'notify_event'),
    (('sub02-2', 'face_localized', '4'), 'notify_event'),
    (('sub02-3', 'face_detected', '3'), 'notify_event'),
    (('sub02-4', 'face_detected', '3'), 'notify_event'),
    (('sub03-1', 'person_detected', '1'), 'notify_event'),
    (('sub03-2', 'person_detected', '1'), 'notify_event')
}

right_event_detail = [
    (RoIS_HRI.ReturnCode_t.OK,'person_detected'),
    (RoIS_HRI.ReturnCode_t.OK,'person_detected'),
    (RoIS_HRI.ReturnCode_t.OK,'person_identified'),
    (RoIS_HRI.ReturnCode_t.OK,'person_identified'),
    
    (RoIS_HRI.ReturnCode_t.OK,'face_localized'),
    (RoIS_HRI.ReturnCode_t.OK,'face_localized'),
    (RoIS_HRI.ReturnCode_t.OK,'face_detected'),
    (RoIS_HRI.ReturnCode_t.OK,'face_detected'),
    
    (RoIS_HRI.ReturnCode_t.OK,'person_detected'),
    (RoIS_HRI.ReturnCode_t.OK,'person_detected')
]

right_command_result = [

    RoIS_HRI.ReturnCode_t.OK,
    
    (RoIS_HRI.ReturnCode_t.OK, eng_profile),
    

    (RoIS_HRI.ReturnCode_t.OK,['urn:x-rois:def:HRIComponent:Kyutech:sub01:PersonDetection',
    'urn:x-rois:def:HRIComponent:Kyutech:sub01:PersonIdentification', 
    'urn:x-rois:def:HRIComponent:Kyutech:sub01:SpeechSynthesis', 
    'urn:x-rois:def:HRIComponent:Kyutech:sub01:Follow', 
    'urn:x-rois:def:HRIComponent:Kyutech:sub02:FaceDetection', 
    'urn:x-rois:def:HRIComponent:Kyutech:sub02:FaceLocalization', 
    'urn:x-rois:def:HRIComponent:Kyutech:sub02:Navigation', 
    'urn:x-rois:def:HRIComponent:Kyutech:sub03:PersonDetection', 
    'urn:x-rois:def:HRIComponent:Kyutech:sub03:Move'
    ]),

    RoIS_HRI.ReturnCode_t.OK, # bind:PersonDetection
    RoIS_HRI.ReturnCode_t.OK, # bind:PersonIdentification
    RoIS_HRI.ReturnCode_t.OK, # bind:SpeechSynthesis
    RoIS_HRI.ReturnCode_t.OK, # bind:Follow
    RoIS_HRI.ReturnCode_t.OK, # bind:FaceDetection
    RoIS_HRI.ReturnCode_t.OK, # bind:FaceLocalization
    RoIS_HRI.ReturnCode_t.OK, # bind:Navigation
    RoIS_HRI.ReturnCode_t.OK, # bind:PersonDetection
    RoIS_HRI.ReturnCode_t.OK, # bind:Move

    (RoIS_HRI.ReturnCode_t.OK,"1"), # subscribe:PersonDetection
    (RoIS_HRI.ReturnCode_t.OK,"2"), # subscribe:PersonIdentification
    (RoIS_HRI.ReturnCode_t.OK,"3"), # subscribe:FaceDetection
    (RoIS_HRI.ReturnCode_t.OK,"4"), # subscribe:FaceLocalization
    
    (RoIS_HRI.ReturnCode_t.OK,['', '', 10, '', '', '', '']), # get_parameter:SpeechSynthesis
    (RoIS_HRI.ReturnCode_t.OK,"sub01-6"), # set_parameter:Follow
    (RoIS_HRI.ReturnCode_t.OK,[1000,20]), # get_parameter:FaceLocalization
    (RoIS_HRI.ReturnCode_t.OK,"sub02-5"), # set_parameter:Navigation
    (RoIS_HRI.ReturnCode_t.OK,"sub03-3"), # set_parameter:Move
    
    (RoIS_HRI.ReturnCode_t.OK,['Bind(urn:x-rois:def:HRIComponent:Kyutech:sub01:Follow):Success']), # get_command_result(sub01-4)
    (RoIS_HRI.ReturnCode_t.OK,['Bind(urn:x-rois:def:HRIComponent:Kyutech:sub02:Navigation):Success']), # get_command_result(sub02-3)
    (RoIS_HRI.ReturnCode_t.OK,['Set_parameter(urn:x-rois:def:HRIComponent:Kyutech:sub03:Move)']), # get_command_result(sub03-3)

    ]

def test_sa(q):
    i = HRI_Engine_client_sample.IF("http://127.0.0.1:8016")
    res = [
        i.connect(),
        i.get_profile(""),
        i.search(""),
        i.bind('urn:x-rois:def:HRIComponent:Kyutech:sub01:PersonDetection'),
        i.bind('urn:x-rois:def:HRIComponent:Kyutech:sub01:PersonIdentification'),
        i.bind('urn:x-rois:def:HRIComponent:Kyutech:sub01:SpeechSynthesis'),
        i.bind('urn:x-rois:def:HRIComponent:Kyutech:sub01:Follow'),
        i.bind('urn:x-rois:def:HRIComponent:Kyutech:sub02:FaceDetection'),
        i.bind('urn:x-rois:def:HRIComponent:Kyutech:sub02:FaceLocalization'),
        i.bind('urn:x-rois:def:HRIComponent:Kyutech:sub02:Navigation'),
        i.bind('urn:x-rois:def:HRIComponent:Kyutech:sub03:PersonDetection'),
        i.bind('urn:x-rois:def:HRIComponent:Kyutech:sub03:Move'),
        
        i.subscribe("person_detected",""),
        i.subscribe("person_identified",""),
        i.subscribe("face_detected",""),
        i.subscribe("face_localized",""),
        
        i.get_parameter('urn:x-rois:def:HRIComponent:Kyutech:sub01:SpeechSynthesis'),
        i.set_parameter('urn:x-rois:def:HRIComponent:Kyutech:sub01:Follow',["",1,1]),
        i.get_parameter('urn:x-rois:def:HRIComponent:Kyutech:sub02:FaceLocalization'),
        i.set_parameter('urn:x-rois:def:HRIComponent:Kyutech:sub02:Navigation',[["xx","yy"],100,"aaa"]),
        i.set_parameter('urn:x-rois:def:HRIComponent:Kyutech:sub03:Move',[["line"],["curve"],1]),

        i.get_command_result("sub01-4",""),
        i.get_command_result("sub02-3",""),
        i.get_command_result("sub03-3","")
    ]

    r = 0

    s_e = set()
    for x in range(13):
        e = i.get_event()
        s_e.add((e[0][:3],e[1]))

    # self.assertEqual(s_e,event_result)

    l_ev = []
    ev = [
        i.get_event_detail("sub01-1",""),
        i.get_event_detail("sub01-2",""),
        i.get_event_detail("sub01-3",""),
        i.get_event_detail("sub01-4",""),
        i.get_event_detail("sub02-1",""),
        i.get_event_detail("sub02-2",""),
        i.get_event_detail("sub02-3",""),
        i.get_event_detail("sub02-4",""),
        i.get_event_detail("sub03-1",""),
        i.get_event_detail("sub03-2","")
    ]
    for y in ev:
        l_ev.append((y[0],y[1][0]))
    
    # self.assertEqual(l_ev,event_detail)

    fin = i.disconnect()

    if s_e != right_event_result:
        print('event results were wrong')
        print(s_e - right_event_result)
        print(s_e)
        r=1
    if l_ev != right_event_detail:
        print('event details were wrong')
        print(s_e - right_event_result)
        r+=10
    if res != right_command_result:
        for x, y in zip(res,right_command_result):
            if x != y:
                print('*', x, y)
        r+=100
    q.put(r)
    
    return r

def kill_ps(ps):
    # terminate the server process
    for x in ps:
        x.kill()
        time.sleep(0.5)

class Main_Sub_Engine_test(unittest.TestCase):    
    maxDiff = None
    
    def setUp(self):
        """ setUP
        """

        # start the server process
        self.q = Queue()
        self.ps = [Process(target=test_sa, args=(self.q,)),
            Process(target=HRI_Engine_sample.test_engine, args=(8016,"tests/engine_profile/engine_profile_2_2", "client_info3", None, None,)),
            Process(target=HRI_Engine_sample.test_engine, args=(8017,"tests/engine_profile/engine_profile_2_2", "client_info3", "urn:x-rois:def:HRIEngine:Kyutech::sub01", None,)),
            Process(target=HRI_Engine_sample.test_engine, args=(8018,"tests/engine_profile/engine_profile_2_2", "client_info3", "urn:x-rois:def:HRIEngine:Kyutech::sub02", None,)),
            Process(target=HRI_Engine_sample.test_engine, args=(8019,"tests/engine_profile/engine_profile_2_2", "client_info3", "urn:x-rois:def:HRIEngine:Kyutech::sub03", None,)),
            
            Process(target=Person_Detection.example_pd, args=(8002,)),
            Process(target=Person_Identification.example_pi, args=(8004,)),
            Process(target=Speech_Synthesis.example_ss, args=(8011,)),
            Process(target=Follow.example_f, args=(8014,)),
            
            Process(target=Face_Detection.example_fd, args=(8005,)),
            Process(target=Face_Localization.example_fl, args=(8006,)),
            Process(target=Navigation.example_n, args=(8013,)),

            Process(target=Person_Detection.example_pd, args=(8022,)),
            Process(target=Move.example_m, args=(8035,))
            ]
        # self.ps.reverse()
        
        for x in reversed(self.ps[1:]):
            x.start()
            time.sleep(0.5)

        time.sleep(3.0)
        

    def test_IF(self):
        """ test_IF
        """
        self.ps[0].start()
        r = self.q.get(60)
        return self.assertEqual(r,0)

    def tearDown(self):
        """ tearDown
        """
        atexit.register(kill_ps, self.ps)


if __name__ == '__main__':
    # ip = sys.argv
    # if len(ip) > 1:
    #     m = re.search(r'(\d+)\.(\d+)\.(\d+)\.(\d+)',ip[1])
    # else:
    #     m = None
    # if m and len(m.groups()) == 4:
    #     ser_uri = "http://" + ip[1] +":8000"
    #     print("server_url == " + ser_uri + "\n")
    #     del sys.argv[1]
    # else:
    #     ser_uri = "http://127.0.0.1:8000"
    #     print("server_url == " + ser_uri + "\n")
    #     if len(ip) > 1 and ip[1][0] != '-':
    #         del sys.argv[1]

    unittest.main()