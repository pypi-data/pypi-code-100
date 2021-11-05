# test_main_sub_engine3.py
#
# Copyright 2020 Ryota Higashi
# Copyright 2021 Eiichi Inohira
#
# This software may be modified and distributed under the terms
# of the MIT license
#
# for python 3

"""unittest サブエンジンが存在しない場合のテスト
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
        > A.4 HRI Engine Profile (p.102 (PDF:p.115)) reference
<-->

<rois:HRIEngineProfile gml:id="engine_profile"
    xmlns:rois="http://www.omg.org/spec/RoIS/20151201"
    xmlns:gml="http://www.opengis.net/gml/3.2">
    <gml:identifier>urn:x-rois:def:HRIEngine:Kyutech::main</gml:identifier>
    <gml:name>main</gml:name>
    <rois:HRIComponent>urn:x-rois:def:HRIComponent:Kyutech:main:PersonDetection</rois:HRIComponent>
    <rois:HRIComponent>urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization</rois:HRIComponent>
    <rois:HRIComponent>urn:x-rois:def:HRIComponent:Kyutech:main:SystemInformation</rois:HRIComponent>
</rois:HRIEngineProfile>"""
     
comp_profile = """<?xml version="1.0" encoding="UTF-8"?>
<!-->
Robotic Interaction Service Framework Version 1.2
    > 9.3 XML PSM : System Information (p.85 (PDF:p.98))
<-->

<rois:HRIComponentProfile gml:id="component_profile"
    xmlns:rois="http://www.omg.org/spec/RoIS/20151201"
    xmlns:ns2="http://www.w3.org/1999/xlink"
    xmlns:gml="http://www.opengis.net/gml/3.2"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <gml:identifier codeSpace="urn:ietf:rfc:2141">
        urn:x-rois:def:component:OMG::SystemInformation</gml:identifier>
    <gml:name>system_info</gml:name>
    <!-- ===== Query Messages ===== -->
    <rois:MessageProfile rois:name="robot_position" xsi:type="rois:QueryMessageProfileType">
        <rois:Results rois:description="position of robot or its parts in comma seperateddouble values [x, y, th]" 
            rois:name="position_data">
            <rois:data_type_ref rois:code="String[]"/>
        </rois:Results>
        <rois:Results rois:description="List of robot IDs" rois:name="robot_ref">
            <rois:data_type_ref rois:code="RoISIdentifier[]"/>
        </rois:Results>
        <rois:Results rois:description="timestamp of measurement" rois:name="timestamp">
            <rois:data_type_ref rois:code="DateTime"/>
        </rois:Results>
    </rois:MessageProfile>
    <rois:MessageProfile rois:name="engine_status"
        xsi:type="rois:QueryMessageProfileType">
        <rois:Results rois:description="Operable time of the HRI Engine that includes this basic component" 
            rois:name="operable_time">
            <rois:data_type_ref rois:code="DateTime"/>
        </rois:Results>
        <rois:Results rois:description="Status information of this engine" rois:name="status">
            <rois:data_type_ref rois:code="Component_Status"/>
        </rois:Results>
    </rois:MessageProfile>
</rois:HRIComponentProfile>"""

right_event_result = {
    (('main-6', RoIS_Service.Completed_Status.OK), 'completed'), # completed
    (('main-1', 'person_localized', '1'), 'notify_event'),
    (('main-2', 'person_localized', '1'), 'notify_event'),
    (('main-3', 'person_detected', '2'), 'notify_event'),
    (('main-4', 'person_detected', '2'), 'notify_event')
}

right_command_result = [
    RoIS_HRI.ReturnCode_t.OK,
    
    (RoIS_HRI.ReturnCode_t.OK, eng_profile),
    
    (RoIS_HRI.ReturnCode_t.OK, [comp_profile]),

    (RoIS_HRI.ReturnCode_t.OK,["urn:x-rois:def:HRIComponent:Kyutech:main:PersonDetection",
    "urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization",
    "urn:x-rois:def:HRIComponent:Kyutech:main:SystemInformation"
    ]),

    RoIS_HRI.ReturnCode_t.OK, # bind:PersonDetection
    RoIS_HRI.ReturnCode_t.OK, # bind:PersonLocalization
    RoIS_HRI.ReturnCode_t.OK, # bind:SystemInformation

    (RoIS_HRI.ReturnCode_t.OK,[1000,20]), # get_parameter:PersonLocalization
    (RoIS_HRI.ReturnCode_t.OK,"main-6"), # set_parameter:PersonLocalization

    (RoIS_HRI.ReturnCode_t.OK,"1"), # subscribe:PersonLocalizationn
    (RoIS_HRI.ReturnCode_t.OK,"2"), # subscribe:PersonDetection
    (RoIS_HRI.ReturnCode_t.OK,['Bind(urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization):Success']), # get_command_result
    
    
    (RoIS_HRI.ReturnCode_t.OK,[100,10]), # get_parameter:PersonLocalization
    RoIS_HRI.ReturnCode_t.OK # disconnect
    ]

def test_sa(q):
    i = HRI_Engine_client_sample.IF("http://127.0.0.1:8016")
    res = [
        i.connect(),
        i.get_profile(""),
        i.query("SystemInformation",""),
        i.search(""),
        i.bind('urn:x-rois:def:HRIComponent:Kyutech:main:PersonDetection'),
        i.bind('urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization'),
        i.bind('urn:x-rois:def:HRIComponent:Kyutech:main:SystemInformation'),
        i.get_parameter('urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization'),
        i.set_parameter('urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization',[100,10]),
        i.subscribe("person_localized",""),
        i.subscribe("person_detected",""),
        i.get_command_result("main-3","")
    ]
        
    s_e = set()
    for x in range(5):
        e = i.get_event()
        s_e.add((e[0][:3],e[1]))
    
    res.extend([i.get_parameter('urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization'),
        i.disconnect()
    ])

    r = 0
    if s_e != right_event_result:
        print('event results were wrong')
        print(s_e - right_event_result)
        r=1
    if res != right_command_result:
        for x, y in zip(res,right_command_result):
            if x != y:
                print('*', x, y)
        r+=10
    q.put(r)
    # print('sa finished')
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
            Process(target=HRI_Engine_sample.test_engine, args=(8016,"tests/engine_profile/engine_profile_3", "client_info1", None, None,)),
            Process(target=Person_Detection.example_pd, args=(8002,)),
            Process(target=Person_Localization.example_pl, args=(8003,)),
            Process(target=System_Information.example_si, args=(8001,))
            ]
        
        for x in reversed(self.ps[1:]):
            x.start()
            time.sleep(0.5)

        time.sleep(5.0)
        

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