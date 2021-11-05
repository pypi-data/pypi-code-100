# test_main_sub_engine2.py
#
# Copyright 2020 Ryota Higashi
# Copyright 2021 Eiichi Inohira
#
# This software may be modified and distributed under the terms
# of the MIT license
#
# for python 3

"""unittest
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
<-->

<rois:HRIEngineProfile gml:id="engine_profile"
    xmlns:rois="http://www.omg.org/spec/RoIS/20151201"
    xmlns:gml="http://www.opengis.net/gml/3.2">
    <gml:identifier>urn:x-rois:def:HRIEngine:Kyutech::main</gml:identifier>
    <gml:name>MainHRI</gml:name>
    <rois:HRIComponent>urn:x-rois:def:HRIComponent:Kyutech:main:PersonDetection</rois:HRIComponent>
    <rois:SubProfile>
        <gml:identifier>urn:x-rois:def:HRIEngine:Kyutech::sub01</gml:identifier>
        <gml:name>SubEng01</gml:name>
        <rois:HRIComponent>urn:x-rois:def:HRIComponent:Kyutech:sub01:PersonIdentification</rois:HRIComponent>
        <rois:HRIComponent>urn:x-rois:def:HRIComponent:Kyutech:sub01:SpeechSynthesis</rois:HRIComponent>
        <rois:HRIComponent>urn:x-rois:def:HRIComponent:Kyutech:sub01:Follow</rois:HRIComponent>
    </rois:SubProfile>
</rois:HRIEngineProfile>"""

        
comp_profile = """<?xml version="1.0" encoding="UTF-8"?>

<rois:HRIComponentProfile
    gml:id="component_profile"
    xmlns:rois="http://www.omg.org/spec/RoIS/20151201"
    xmlns:ns2="http://www.w3.org/1999/xlink"
    xmlns:gml="http://www.opengis.net/gml/3.2"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <gml:identifier codeSpace="urn:ietf:rfc:2141">
        urn:x-rois:def:component:OMG::SpeechSynthesis</gml:identifier>
    <gml:name>speech_synthesizer</gml:name>
    
    <!-- ===== Sub Component Profiles ===== -->
    <rois:SubComponentProfile>
        urn:x-rois:def:Component:OMG::RoISCommon</rois:SubComponentProfile>
    
    <!-- ===== Query Messages ===== -->
    <rois:MessageProfile rois:name="synthesizable_languages"
        xsi:type="rois:QueryMessageProfileType">
        <rois:Results rois:description="list of available languages" rois:name="languages">
            <rois:data_type_ref rois:code="string[]"/>
        </rois:Results>
    </rois:MessageProfile>
    <rois:MessageProfile rois:name="available_voices"
        xsi:type="rois:QueryMessageProfileType">
        <rois:Results rois:description="list of available voice characters"
            rois:name="characters">
            <rois:data_type_ref rois:code="string[]"/>
        </rois:Results>
    </rois:MessageProfile>
    
    <!-- ===== Parameter Profiles ===== -->
    <rois:ParameterProfile rois:description="speech text in plain text"
        rois:name="speech_text">
        <rois:data_type_ref rois:code="string"/>
    </rois:ParameterProfile>
    <rois:ParameterProfile rois:description="speech text in SSML text"
        rois:name="ssml_text">
        <rois:data_type_ref rois:code="string"/>
    </rois:ParameterProfile>
    <rois:ParameterProfile rois:description="Volume" rois:name="volume"
        rois:default_value="50">
        <rois:data_type_ref rois:code="int"/>
    </rois:ParameterProfile>
    <rois:ParameterProfile rois:description="Language of the speech" rois:name="language"
        rois:default_value="en">
        <rois:data_type_ref rois:code="string"/>
    </rois:ParameterProfile>
    <rois:ParameterProfile rois:description="character of the voice" rois:name="character"
        rois:default_value="default">
        <rois:data_type_ref rois:code="string"/>
    </rois:ParameterProfile>
</rois:HRIComponentProfile>"""

right_event_result = {
    (('sub01-6', RoIS_Service.Completed_Status.OK), 'completed'), # completed
    (('sub01-7', RoIS_Service.Completed_Status.OK), 'completed'), # completed
    (('main-1', 'person_detected', '1'), 'notify_event'),
    (('main-2', 'person_detected', '1'), 'notify_event'),
    (('sub01-1', 'person_identified', '2'), 'notify_event'),
    (('sub01-2', 'person_identified', '2'), 'notify_event')
    }

right_command_result = [
    RoIS_HRI.ReturnCode_t.OK,
    
    (RoIS_HRI.ReturnCode_t.OK, eng_profile),
    
    # (RoIS_HRI.ReturnCode_t.OK, ['<?xml version="1.0" encoding="UTF-8"?>\n\n<rois:HRIComponentProfile\n    gml:id="component_profile"\n    xmlns:rois="http://www.omg.org/spec/RoIS/20151201"\n    xmlns:ns2="http://www.w3.org/1999/xlink"\n    xmlns:gml="http://www.opengis.net/gml/3.2"\n    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n    <gml:identifier codeSpace="urn:ietf:rfc:2141">\n        urn:x-rois:def:component:OMG::SpeechSynthesis</gml:identifier>\n    <gml:name>speech_synthesizer</gml:name>\n    \n    <!-- ===== Sub Component Profiles ===== -->\n    <rois:SubComponentProfile>\n        urn:x-rois:def:Component:OMG::RoISCommon</rois:SubComponentProfile>\n    \n    <!-- ===== Query Messages ===== -->\n    <rois:MessageProfile rois:name="synthesizable_languages"\n        xsi:type="rois:QueryMessageProfileType">\n        <rois:Results rois:description="list of available languages" rois:name="languages">\n            <rois:data_type_ref rois:code="string[]"/>\n        </rois:Results>\n    </rois:MessageProfile>\n    <rois:MessageProfile rois:name="available_voices"\n        xsi:type="rois:QueryMessageProfileType">\n        <rois:Results rois:description="list of available voice characters"\n            rois:name="characters">\n            <rois:data_type_ref rois:code="string[]"/>\n        </rois:Results>\n    </rois:MessageProfile>\n    \n    <!-- ===== Parameter Profiles ===== -->\n    <rois:ParameterProfile rois:description="speech text in plain text"\n        rois:name="speech_text">\n        <rois:data_type_ref rois:code="string"/>\n    </rois:ParameterProfile>\n    <rois:ParameterProfile rois:description="speech text in SSML text"\n        rois:name="ssml_text">\n        <rois:data_type_ref rois:code="string"/>\n    </rois:ParameterProfile>\n    <rois:ParameterProfile rois:description="Volume" rois:name="volume"\n        rois:default_value="50">\n        <rois:data_type_ref rois:code="int"/>\n    </rois:ParameterProfile>\n    <rois:ParameterProfile rois:description="Language of the speech" rois:name="language"\n        rois:default_value="en">\n        <rois:data_type_ref rois:code="string"/>\n    </rois:ParameterProfile>\n    <rois:ParameterProfile rois:description="character of the voice" rois:name="character"\n        rois:default_value="default">\n        <rois:data_type_ref rois:code="string"/>\n    </rois:ParameterProfile>\n</rois:HRIComponentProfile>']),
    (RoIS_HRI.ReturnCode_t.OK, [comp_profile]),

    (RoIS_HRI.ReturnCode_t.OK,['urn:x-rois:def:HRIComponent:Kyutech:main:PersonDetection',
    'urn:x-rois:def:HRIComponent:Kyutech:sub01:PersonIdentification', 
    'urn:x-rois:def:HRIComponent:Kyutech:sub01:SpeechSynthesis', 
    'urn:x-rois:def:HRIComponent:Kyutech:sub01:Follow', 
    # 'urn:x-rois:def:HRIComponent:Kyutech:sub02:FaceDetection', 
    # 'urn:x-rois:def:HRIComponent:Kyutech:sub02:FaceLocalization', 
    # 'urn:x-rois:def:HRIComponent:Kyutech:sub02:Navigation', 
    # 'urn:x-rois:def:HRIComponent:Kyutech:sub03:PersonDetection', 
    # 'urn:x-rois:def:HRIComponent:Kyutech:sub03:Move'
    ]),

    RoIS_HRI.ReturnCode_t.OK, # bind:PersonDetection
    RoIS_HRI.ReturnCode_t.OK, # bind:PersonIdentification
    RoIS_HRI.ReturnCode_t.OK, # bind:SpeechSynthesis
    RoIS_HRI.ReturnCode_t.OK, # bind:Follow
    # RoIS_HRI.ReturnCode_t.OK, # bind:FaceDetection
    # RoIS_HRI.ReturnCode_t.OK, # bind:FaceLocalization
    # RoIS_HRI.ReturnCode_t.OK, # bind:Navigation
    # RoIS_HRI.ReturnCode_t.OK, # release:Follow
    (RoIS_HRI.ReturnCode_t.OK,['', '', 10, '', '', '', '']), # get_parameter:SpeechSynthesis
    (RoIS_HRI.ReturnCode_t.OK,["",1000,10]), # get_parameter:Follow
    (RoIS_HRI.ReturnCode_t.OK,"sub01-6"), # set_parameter:SpeechSynthesis
    (RoIS_HRI.ReturnCode_t.OK,"sub01-7"), # set_parameter:Follow
    (RoIS_HRI.ReturnCode_t.OK,"1"), # subscribe:PersonDetection
    (RoIS_HRI.ReturnCode_t.OK,"2"), # subscribe:PersonIdentification
    # RoIS_HRI.ReturnCode_t.OK, # unsubscribe
    # (RoIS_HRI.ReturnCode_t.OK,"2"), # subscribe
    (RoIS_HRI.ReturnCode_t.OK,["Bind(urn:x-rois:def:HRIComponent:Kyutech:sub01:PersonIdentification):Success"]), # get_command_result
    RoIS_HRI.ReturnCode_t.OK # disconnect
    ]

def kill_ps(ps):
    # terminate the server process
    for x in ps:
        x.kill()
        time.sleep(0.5)

def test_sa(q):
    i = HRI_Engine_client_sample.IF("http://127.0.0.1:8016")
    res = [
        i.connect(),
        i.get_profile(""),
        i.query("SpeechSynthesis",""),
        i.search(""),
        i.bind('urn:x-rois:def:HRIComponent:Kyutech:main:PersonDetection'),
        i.bind('urn:x-rois:def:HRIComponent:Kyutech:sub01:PersonIdentification'),
        i.bind('urn:x-rois:def:HRIComponent:Kyutech:sub01:SpeechSynthesis'),
        i.bind('urn:x-rois:def:HRIComponent:Kyutech:sub01:Follow'),
        # i.bind('urn:x-rois:def:HRIComponent:Kyutech:sub02:FaceDetection'),
        # i.bind('urn:x-rois:def:HRIComponent:Kyutech:sub02:FaceLocalization'),
        # i.bind('urn:x-rois:def:HRIComponent:Kyutech:sub02:Navigation'),
        # i.release('urn:x-rois:def:HRIComponent:Kyutech:sub01:Follow'),
        i.get_parameter('urn:x-rois:def:HRIComponent:Kyutech:sub01:SpeechSynthesis'),
        i.get_parameter('urn:x-rois:def:HRIComponent:Kyutech:sub01:Follow'),
        i.set_parameter('urn:x-rois:def:HRIComponent:Kyutech:sub01:SpeechSynthesis',["","",1,"",""]),
        i.set_parameter('urn:x-rois:def:HRIComponent:Kyutech:sub01:Follow',["",1,1]),
        i.subscribe("person_detected",""),
        i.subscribe("person_identified",""),
        # i.unsubscribe("1"),
        # i.subscribe("person_detected",""),
        i.get_command_result("sub01-1",""),
        i.disconnect()
        ]
    
    s_e = set()
    for x in range(6):
        e = i.get_event()
        s_e.add((e[0][:3],e[1]))

    r = 0
    if s_e != right_event_result:
        print('event results were wrong')
        print(s_e - right_event_result)
        r=1
    if res != right_command_result:
        print(res)
        r+=10
    q.put(r)
    # print('sa finished')
    return r

class Main_Sub_Engine_test(unittest.TestCase):    
    maxDiff = None
    
    def setUp(self):
        """ setUP
        """

        # start the server process
        self.q = Queue()
        self.ps = [Process(target=test_sa, args=(self.q,)),
            Process(target=HRI_Engine_sample.test_engine, args=(8016,"tests/engine_profile/engine_profile_2_1", "client_info2", None, None,)),
            Process(target=HRI_Engine_sample.test_engine, args=(8017,"tests/engine_profile/engine_profile_2_1", "client_info2", "urn:x-rois:def:HRIEngine:Kyutech::sub01", None,)),
            # Process(target=HRI_Engine_sample.test_engine, args=(8018,"engine_profile_2", "x-rois:def:HRIEngine:Kyutech::SubEng02", "component_client_info", None,)),
            Process(target=Person_Detection.example_pd, args=(8002,)),
            # Process(target=Face_Detection.example_fd, args=(8005,)),
            # Process(target=Face_Localization.example_fl, args=(8006,)),
            # Process(target=Navigation.example_n, args=(8013,)),
            Process(target=Person_Identification.example_pi, args=(8004,)),
            Process(target=Speech_Synthesis.example_ss, args=(8011,)),
            Process(target=Follow.example_f, args=(8014,))
            ]
        
        for x in reversed(self.ps[1:]):
            x.start()
            # print(x.pid)
            time.sleep(0.5)

        time.sleep(5.0)

    def test_main_sub_engine(self):
        """ test_test_main_sub_engine
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