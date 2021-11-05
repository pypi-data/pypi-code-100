# unittest_main_sub_engine3.py
#
# Copyright 2020 Ryota Higashi
# Copyright 2021 Eiichi Inohira
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
from datetime import datetime
import json

from pyrois import RoIS_HRI, RoIS_Common, RoIS_Service
from pyrois_common import HRI_Engine_sample, HRI_Engine_client_sample
from pyrois_common import command_message
from pyrois_common import System_Information, Person_Detection, Person_Localization, Person_Identification
from pyrois_common import Face_Detection, Face_Localization, Sound_Detection, Sound_Localization
from pyrois_common import Speech_Recognition, Gesture_Recognition, Speech_Synthesis
from pyrois_common import Reaction, Navigation, Follow, Move

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


command_unit_list1 = """{
    "command_unit_list": [
        {
            "component_ref": "urn:x-rois:def:HRIComponent:Kyutech:sub01:SpeechSynthesis",
            "command_type": "set_parameter",
            "command_id": "",
            "arguments": {
                "parameters": [
                    {
                        "name": "speech_text",
                        "data_type_ref": {
                            "codebook_reference": "",
                            "version": ""
                        },
                        "value": "aaa"
                    },
                    {
                        "name": "SSML_text",
                        "data_type_ref": {
                            "codebook_reference": "",
                            "version": ""
                        },
                        "value": "ssml"
                    },
                    {
                        "name": "volume",
                        "data_type_ref": {
                            "codebook_reference": "",
                            "version": ""
                        },
                        "value": 50
                    },
                    {
                        "name": "languages",
                        "data_type_ref": {
                            "codebook_reference": "",
                            "version": ""
                        },
                        "value": "japanese"
                    },
                    {
                        "name": "character",
                        "data_type_ref": {
                            "codebook_reference": "",
                            "version": ""
                        },
                        "value": "m1"
                    }
                ]
            },
            "delay_time": 0
        },
        {
            "component_ref": "urn:x-rois:def:HRIComponent:Kyutech:sub01:SpeechSynthesis",
            "command_type": "get_parameter",
            "command_id": "",
            "arguments": {
                "parameters": [
                    {
                        "name": "",
                        "data_type_ref": {
                            "codebook_reference": "",
                            "version": ""
                        },
                        "value": ""
                    }
                ]
            },
            "delay_time": 0
        },
        {
            "branch_list": [
                {
                    "command_list": [
                        {
                            "component_ref": "urn:x-rois:def:HRIComponent:Kyutech:sub02:FaceLocalization",
                            "command_type": "set_parameter",
                            "command_id": "",
                            "arguments": {
                                "parameters": [
                                    {
                                        "name": "detection_threshold",
                                        "data_type_ref": {
                                            "codebook_reference": "",
                                            "version": ""
                                        },
                                        "value": 3
                                    },
                                    {
                                        "name": "minimum_interval",
                                        "data_type_ref": {
                                            "codebook_reference": "",
                                            "version": ""
                                        },
                                        "value": 2
                                    }
                                ]
                            },
                            "delay_time": 3000
                        },
                        {
                            "component_ref": "urn:x-rois:def:HRIComponent:Kyutech:sub02:Navigation",
                            "command_type": "set_parameter",
                            "command_id": "",
                            "arguments": {
                                "parameters": [
                                    {
                                        "name": "target_position",
                                        "data_type_ref": {
                                            "codebook_reference": "",
                                            "version": ""
                                        },
                                        "value": [
                                            100.0,
                                            200.0
                                        ]
                                    },
                                    {
                                        "name": "time_limit",
                                        "data_type_ref": {
                                            "codebook_reference": "",
                                            "version": ""
                                        },
                                        "value": 60000
                                    },
                                    {
                                        "name": "routing_policy",
                                        "data_type_ref": {
                                            "codebook_reference": "",
                                            "version": ""
                                        },
                                        "value": "time priority"
                                    }
                                ]
                            },
                            "delay_time": 4000
                        }
                    ]
                },
                {
                    "command_list": [
                        {
                            "component_ref": "urn:x-rois:def:HRIComponent:Kyutech:sub03:Move",
                            "command_type": "set_parameter",
                            "command_id": "",
                            "arguments": {
                                "parameters": [
                                    {
                                        "name": "line",
                                        "data_type_ref": {
                                            "codebook_reference": "",
                                            "version": ""
                                        },
                                        "value": [
                                            1000,
                                            360
                                        ]
                                    },
                                    {
                                        "name": "curve",
                                        "data_type_ref": {
                                            "codebook_reference": "",
                                            "version": ""
                                        },
                                        "value": [
                                            1000,
                                            90
                                        ]
                                    },
                                    {
                                        "name": "time",
                                        "data_type_ref": {
                                            "codebook_reference": "",
                                            "version": ""
                                        },
                                        "value": 1000
                                    }
                                ]
                            },
                            "delay_time": 5000
                        }
                    ]
                },
                {
                    "command_list": [
                        {
                            "component_ref": "urn:x-rois:def:HRIComponent:Kyutech:sub03:Move",
                            "command_type": "set_parameter",
                            "command_id": "",
                            "arguments": {
                                "parameters": [
                                    {
                                        "name": "line",
                                        "data_type_ref": {
                                            "codebook_reference": "",
                                            "version": ""
                                        },
                                        "value": [
                                            1000,
                                            360
                                        ]
                                    },
                                    {
                                        "name": "curve",
                                        "data_type_ref": {
                                            "codebook_reference": "",
                                            "version": ""
                                        },
                                        "value": [
                                            1000,
                                            90
                                        ]
                                    },
                                    {
                                        "name": "time",
                                        "data_type_ref": {
                                            "codebook_reference": "",
                                            "version": ""
                                        },
                                        "value": 1000
                                    }
                                ]
                            },
                            "delay_time": 5000
                        }
                    ]
                }
            ],
            "delay_time": 0
        },
        {
            "component_ref": "urn:x-rois:def:HRIComponent:Kyutech:sub01:Follow",
            "command_type": "set_parameter",
            "command_id": "",
            "arguments": {
                "parameters": [
                    {
                        "name": "target_object_ref",
                        "data_type_ref": {
                            "codebook_reference": "",
                            "version": ""
                        },
                        "value": "human1"
                    },
                    {
                        "name": "distance",
                        "data_type_ref": {
                            "codebook_reference": "",
                            "version": ""
                        },
                        "value": 500
                    },
                    {
                        "name": "time_limit",
                        "data_type_ref": {
                            "codebook_reference": "",
                            "version": ""
                        },
                        "value": 60000
                    }
                ]
            },
            "delay_time": 1000
        }
    ]
}"""

event_result = {
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


class Execute_test(unittest.TestCase):    
    maxDiff = None
    
    def setUp(self):
        """ setUP
        """
        # start the server process
        e_profile = "tests/engine_profile/engine_profile_2_2"
        c_info = "tests/client_info/client_info3"
        self.ps = [Process(target=HRI_Engine_sample.test_engine, args=(8016,e_profile, c_info, None, None,)),
            Process(target=HRI_Engine_sample.test_engine, args=(8017,e_profile, c_info, "urn:x-rois:def:HRIEngine:Kyutech::sub01", None,)),
            Process(target=HRI_Engine_sample.test_engine, args=(8018,e_profile, c_info, "urn:x-rois:def:HRIEngine:Kyutech::sub02", None,)),
            Process(target=HRI_Engine_sample.test_engine, args=(8019,e_profile, c_info, "urn:x-rois:def:HRIEngine:Kyutech::sub03", None,)),
            
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
        
        for x in reversed(self.ps):
            x.start()
            time.sleep(0.5)

        time.sleep(5.0)
        

    def test_IF(self):
        """ test_IF
        """
        #execute1
        c_ri = command_message.RoIS_Identifier("","")
        c_p_ss1 = command_message.Parameter("speech_text", c_ri, "aaa")
        c_p_ss2 = command_message.Parameter("SSML_text", c_ri, "ssml")
        c_p_ss3 = command_message.Parameter("volume", c_ri, 50)
        c_p_ss4 = command_message.Parameter("languages", c_ri, "japanese")
        c_p_ss5 = command_message.Parameter("character", c_ri, "m1")
        c_al1 = command_message.ArgumentList([c_p_ss1,c_p_ss2,c_p_ss3,c_p_ss4,c_p_ss5])
        c_cm1 = command_message.CommandMessage('urn:x-rois:def:HRIComponent:Kyutech:sub01:SpeechSynthesis',"set_parameter","",c_al1)
        c_cm1.delay_time = 0

        c_p = command_message.Parameter("", c_ri, "")
        c_al2 = command_message.ArgumentList([c_p])
        c_cm2 = command_message.CommandMessage('urn:x-rois:def:HRIComponent:Kyutech:sub01:SpeechSynthesis',"get_parameter","",c_al2)
        c_cm2.delay_time = 0

        c_p_fl1 = command_message.Parameter("detection_threshold", c_ri, 3)
        c_p_fl2 = command_message.Parameter("minimum_interval", c_ri, 2)
        c_al3_1_1 = command_message.ArgumentList([c_p_fl1,c_p_fl2])
        c_cm3_1_1 = command_message.CommandMessage('urn:x-rois:def:HRIComponent:Kyutech:sub02:FaceLocalization',"set_parameter","",c_al3_1_1)
        c_cm3_1_1.delay_time = 3000
    
        c_p_n1 = command_message.Parameter("target_position", c_ri, [100.0,200.0])
        c_p_n2 = command_message.Parameter("time_limit", c_ri, 60000)
        c_p_n3 = command_message.Parameter("routing_policy", c_ri, "time priority")
        c_al3_1_2 = command_message.ArgumentList([c_p_n1,c_p_n2,c_p_n3])
        c_cm3_1_2 = command_message.CommandMessage('urn:x-rois:def:HRIComponent:Kyutech:sub02:Navigation',"set_parameter","",c_al3_1_2)
        c_cm3_1_2.delay_time = 4000

        c_p_m1 = command_message.Parameter("line", c_ri, [1000,360])
        c_p_m2 = command_message.Parameter("curve", c_ri, [1000,90])
        c_p_m3 = command_message.Parameter("time", c_ri, 1000)
        c_al3_2 = command_message.ArgumentList([c_p_m1,c_p_m2,c_p_m3])
        c_cm3_2 = command_message.CommandMessage('urn:x-rois:def:HRIComponent:Kyutech:sub03:Move',"set_parameter","",c_al3_2)
        c_cm3_2.delay_time = 5000

        c_b1 = command_message.Branch([c_cm3_1_1,c_cm3_1_2])
        c_b2 = command_message.Branch([c_cm3_2])
        c_cc = command_message.ConcurrentCommands([c_b1,c_b2,c_b2])
        c_cc.delay_time = 0

        c_p_f1 = command_message.Parameter("target_object_ref", c_ri, "human1")
        c_p_f2 = command_message.Parameter("distance", c_ri, 500)
        c_p_f3 = command_message.Parameter("time_limit", c_ri, 60000)
        c_al4 = command_message.ArgumentList([c_p_f1,c_p_f2,c_p_f3])
        c_cm4 = command_message.CommandMessage('urn:x-rois:def:HRIComponent:Kyutech:sub01:Follow',"set_parameter","",c_al4)
        c_cm4.delay_time = 1000    
        
        c_cus1 = command_message.CommandUnitSequence([c_cm1,c_cm2,c_cc,c_cm4])



        i = HRI_Engine_client_sample.IF("http://127.0.0.1:8016")
        res = [
            i.connect(),
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

            i.execute(c_cus1),
            
            i.get_command_result("main-exe-1","")
        ]
            
        # print(res)

        s_e = set()
        completed_command_id = set()
        for x in range(10):
            e = i.get_event()
            s_e.add((e[0][:3],e[1]))
            if e[1] == "completed":
                completed_command_id.add(e[0][0])
            else:
                pass
        
        # print("completed_command_id:{}".format(completed_command_id))
        
        command_unit_lists = [command_unit_list1]
        command_ids = set()
        for y in command_unit_lists:
            d = json.loads(y)
            for c in d["command_unit_list"]:
                c_k = list(c.keys())
                if c_k[0] != "branch_list":
                    if c["command_type"] == "set_parameter":
                        command_ids.add(c["command_id"])
                else:
                    for b in c["branch_list"]:
                        for cl in b["command_list"]:
                            if cl["command_type"] == "set_parameter":
                                command_ids.add(cl["command_id"])

        
        # print("set_parameter_command_ids:{}".format(command_ids))

    
        res.extend([
            i.disconnect()
        ])

        self.assertEqual(s_e,event_result)
        # self.assertEqual(completed_command_id,command_ids)
        return self.assertEqual(res,
                                [
                                RoIS_HRI.ReturnCode_t.OK,
                            
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

                                (RoIS_HRI.ReturnCode_t.ERROR,command_unit_list1), # execute1

                                (RoIS_HRI.ReturnCode_t.OK,["Execute(main-exe-1):Can't access the set_parameter in the same component from different branches"]), # get_command_result
                                
                                RoIS_HRI.ReturnCode_t.OK # disconnect
                                ])


    def tearDown(self):
        """ tearDown
        """
        # terminate the server process
        for x in self.ps:
            if x.is_alive():
                x.terminate()

        time.sleep(3)


if __name__ == '__main__':
    unittest.main()