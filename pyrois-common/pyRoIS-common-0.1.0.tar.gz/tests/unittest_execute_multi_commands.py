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
        > A.4 HRI Engine Profile (p.102 (PDF:p.115)) reference
<-->

<rois:HRIEngineProfile gml:id="engine_profile"
    xmlns:rois="http://www.omg.org/spec/RoIS/20151201"
    xmlns:gml="http://www.opengis.net/gml/3.2">
    <gml:identifier>urn:x-rois:def:HRIEngine:Kyutech::main</gml:identifier>
    <gml:name>main</gml:name>
    <rois:HRIComponent>urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization</rois:HRIComponent>
</rois:HRIEngineProfile>"""

commnd_unit_list ="""{
    "command_unit_list": [
        {
            "component_ref": "urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization",
            "command_type": "set_parameter",
            "command_id": "main-exe-1-1",
            "arguments": {
                "parameters": [
                    {
                        "name": "detection_threshold",
                        "data_type_ref": {
                            "codebook_reference": "",
                            "version": ""
                        },
                        "value": 555
                    },
                    {
                        "name": "minimum_interval",
                        "data_type_ref": {
                            "codebook_reference": "",
                            "version": ""
                        },
                        "value": 222
                    }
                ]
            },
            "delay_time": 5
        },
        {
            "component_ref": "urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization",
            "command_type": "get_parameter",
            "command_id": "main-exe-1-2",
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
            "delay_time": 3
        },
        {
            "component_ref": "urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization",
            "command_type": "set_parameter",
            "command_id": "main-exe-1-3",
            "arguments": {
                "parameters": [
                    {
                        "name": "detection_threshold",
                        "data_type_ref": {
                            "codebook_reference": "",
                            "version": ""
                        },
                        "value": 300
                    },
                    {
                        "name": "minimum_interval",
                        "data_type_ref": {
                            "codebook_reference": "",
                            "version": ""
                        },
                        "value": 100
                    }
                ]
            },
            "delay_time": 10
        },
        {
            "component_ref": "urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization",
            "command_type": "get_parameter",
            "command_id": "main-exe-1-4",
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
            "delay_time": 2
        }
    ]
}"""

# command_unit_list_dict = {'command_unit_list': [{'component_ref': 'urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization', 'command_type': 'set_parameter', 'command_id': 'main-4', 'arguments': {'parameters': [{'name': 'detection_threshold', 'data_type_ref': {'codebook_reference': '', 'version': ''}, 'value': 555}, {'name': 'minimum_interval', 'data_type_ref': {'codebook_reference': '', 'version': ''}, 'value': 222}]}, 'delay_time': 5}, {'component_ref': 'urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization', 'command_type': 'get_parameter', 'command_id': 'main-5', 'arguments': {'parameters': [{'name': '', 'data_type_ref': {'codebook_reference': '', 'version': ''}, 'value': ''}]}, 'delay_time': 3}, {'component_ref': 'urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization', 'command_type': 'set_parameter', 'command_id': 'main-6', 'arguments': {'parameters': [{'name': 'detection_threshold', 'data_type_ref': {'codebook_reference': '', 'version': ''}, 'value': 300}, {'name': 'minimum_interval', 'data_type_ref': {'codebook_reference': '', 'version': ''}, 'value': 100}]}, 'delay_time': 10}, {'component_ref': 'urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization', 'command_type': 'get_parameter', 'command_id': 'main-7', 'arguments': {'parameters': [{'name': '', 'data_type_ref': {'codebook_reference': '', 'version': ''}, 'value': ''}]}, 'delay_time': 2}]}
getparameter_dict = "Get_parameter(urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization):Parameters_(555, 222)"

event_result = {
    (('main-exe-1-1', RoIS_Service.Completed_Status.OK), 'completed'), # completed set_parameter
    (('main-exe-1-3', RoIS_Service.Completed_Status.OK), 'completed'), # completed set_parameter
    # (('main-1', 'person_localized', '1'), 'notify_event'),
    # (('main-2', 'person_localized', '1'), 'notify_event'),
    # (('main-3', 'person_detected', '2'), 'notify_event'),
    # (('main-4', 'person_detected', '2'), 'notify_event')
}


class Execute_test(unittest.TestCase):    
    maxDiff = None
    
    def setUp(self):
        """ setUP
        """
        # start the server process
        e_profile = "tests/engine_profile/engine_profile_3_1"
        c_info = "tests/client_info/client_info1"
        self.ps = [Process(target=HRI_Engine_sample.test_engine, args=(8016,e_profile, c_info, "urn:x-rois:def:HRIEngine:Kyutech::main", None,)),
            # Process(target=Person_Detection.example_pd, args=(8002,)),
            Process(target=Person_Localization.example_pl, args=(8003,))
            # Process(target=System_Information.example_si, args=(8001,))
            ]
        
        for x in reversed(self.ps):
            x.start()
            time.sleep(0.5)

        time.sleep(5.0)
        

    def test_IF(self):
        """ test_IF
        """
        c_ri = command_message.RoIS_Identifier("","")
        c_p1 = command_message.Parameter("detection_threshold", c_ri, 555)
        c_p2 = command_message.Parameter("minimum_interval", c_ri, 222)
        c_al1 = command_message.ArgumentList([c_p1,c_p2])
        c_cm1 = command_message.CommandMessage('urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization',"set_parameter","",c_al1)
        c_cm1.delay_time = 5
        
        c_p3 = command_message.Parameter("detection_threshold", c_ri, 300)
        c_p4 = command_message.Parameter("minimum_interval", c_ri, 100)
        c_al2 = command_message.ArgumentList([c_p3,c_p4])
        c_cm2 = command_message.CommandMessage('urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization',"set_parameter","",c_al2)
        c_cm2.delay_time = 10
    
        c_p5 = command_message.Parameter("", c_ri, "")
        c_al3 = command_message.ArgumentList([c_p5])
        c_cm3 = command_message.CommandMessage('urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization',"get_parameter","",c_al3)
        c_cm3.delay_time = 3

        c_p6 = command_message.Parameter("", c_ri, "")
        c_al4 = command_message.ArgumentList([c_p6])
        c_cm4 = command_message.CommandMessage('urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization',"get_parameter","",c_al4)
        c_cm4.delay_time = 2
        
        c_cus = command_message.CommandUnitSequence([c_cm1,c_cm3,c_cm2,c_cm4])


        i = HRI_Engine_client_sample.IF("http://127.0.0.1:8016")
        res = [
            i.connect(),
            i.bind('urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization'),
            i.get_parameter('urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization'),
            i.execute(c_cus),
            i.get_command_result("main-3","")
        ]
            
        # print(res)

        s_e = set()
        for x in range(2):
            e = i.get_event()
            # print(e)
            s_e.add((e[0][:3],e[1]))
        
        res.extend([
            i.disconnect()
        ])

        # print(s_e,event_result)
        self.assertEqual(s_e,event_result)
        return self.assertEqual(res,
                                [
                                RoIS_HRI.ReturnCode_t.OK,
                            
                                RoIS_HRI.ReturnCode_t.OK, # bind:PersonLocalization

                                (RoIS_HRI.ReturnCode_t.OK,[1000,20]), # get_parameter:PersonLocalization
                                (RoIS_HRI.ReturnCode_t.OK,commnd_unit_list), # execute

                                (RoIS_HRI.ReturnCode_t.OK,[getparameter_dict]), # get_command_result
                                
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