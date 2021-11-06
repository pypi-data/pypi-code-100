# test_execute.py
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
from datetime import datetime
import atexit

from pyrois import RoIS_HRI, RoIS_Common, RoIS_Service
from pyrois_common import HRI_Engine_sample, HRI_Engine_client_sample, command_message
from . import utils

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
        }
    ]
}"""

right_event_result = {
    (('main-2', RoIS_Service.Completed_Status.OK), 'completed'), # completed
    (('main-exe-1-1', RoIS_Service.Completed_Status.OK), 'completed') # completed
    # (('main-1', 'person_localized', '1'), 'notify_event'),
    # (('main-2', 'person_localized', '1'), 'notify_event'),
    # (('main-3', 'person_detected', '2'), 'notify_event'),
    # (('main-4', 'person_detected', '2'), 'notify_event')
}

right_command_result = [
    RoIS_HRI.ReturnCode_t.OK,
    # (RoIS_HRI.ReturnCode_t.OK, eng_profile),
    # (RoIS_HRI.ReturnCode_t.OK,["urn:x-rois:def:HRIComponent:Kyutech:main:PersonDetection",
    # "urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization",
    # "urn:x-rois:def:HRIComponent:Kyutech:main:SystemInformation"
    # ]),
    # (RoIS_HRI.ReturnCode_t.OK,["urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization",]),
    RoIS_HRI.ReturnCode_t.OK, # bind:PersonLocalization
    # (RoIS_HRI.ReturnCode_t.OK,[1000
    # ,20]), # get_parameter:PersonLocalization
    (RoIS_HRI.ReturnCode_t.OK,"main-2"), # set_parameter:PersonLocalization
    (RoIS_HRI.ReturnCode_t.OK,commnd_unit_list), # execute
    # (RoIS_HRI.ReturnCode_t.OK,"1"), # subscribe:PersonLocalizationn
    (RoIS_HRI.ReturnCode_t.OK,["Set_parameter(urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization)"]), # get_command_result
    RoIS_HRI.ReturnCode_t.OK # disconnect
    ]
# dt = datetime.now()
# dt_format = dt.strftime("%Y%m%d-%H%M")
# logger1 = logging.getLogger('[main]_Engine: HRI_Engine_sample.py')
# logger1.setLevel(logging.DEBUG)
# logger2 = logging.getLogger('Service_Application: HRI_Engine_client_sample.py')
# logger2.setLevel(logging.DEBUG)

# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# f = logging.FileHandler('unittest_execute_{}.log'.format(dt_format))
# f.setLevel(logging.DEBUG)
# f.setFormatter(formatter)
# logger1.addHandler(f)
# logger2.addHandler(f)

# c = logging.StreamHandler()
# c.setLevel(logging.ERROR)
# c.setFormatter(formatter)
# logger1.addHandler(c)
# logger2.addHandler(c)

def test_sa(q):
    c_ri = command_message.RoIS_Identifier("","")
    c_p1 = command_message.Parameter("detection_threshold", c_ri, 555)
    c_p2 = command_message.Parameter("minimum_interval", c_ri, 222)
    c_al = command_message.ArgumentList([c_p1,c_p2])
    # c_cb = command_message.CommandBase(5) # 反映されない気がする ソースいじる必要がある？
    c_cm = command_message.CommandMessage('urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization',"set_parameter","",c_al) # command_id引数いらない
    c_cm.delay_time = 5
    c_cus = command_message.CommandUnitSequence([c_cm])

    i = HRI_Engine_client_sample.IF("http://127.0.0.1:8016")
    res = [
        i.connect(),
        # i.get_profile(""),
        # i.search(""),
        # i.bind('urn:x-rois:def:HRIComponent:Kyutech:main:PersonDetection'),
        i.bind('urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization'),
        # i.bind('urn:x-rois:def:HRIComponent:Kyutech:main:SystemInformation'),
        # i.get_parameter('urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization'),
        i.set_parameter('urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization',[100,10]),
        i.execute(c_cus),
        # i.subscribe("person_localized",""),
        # i.subscribe("person_detected",""),
        i.get_command_result("main-2","")
    ]
        
    # print(res)

    s_e = set()
    for x in range(2):
        e = i.get_event()
        s_e.add((e[0][:3],e[1]))
    
    res.extend([
        i.disconnect()
    ])

    r = 0
    if s_e != right_event_result:
        print(s_e)
        r=1
    if res != right_command_result:
        print(res)
        r=2
    q.put(r)
    # print('sa finished')
    return r

def kill_ps(ps):
    # terminate the server process
    for x in ps:
        x.kill()
        time.sleep(0.5)

class Execute_test(unittest.TestCase):    
    maxDiff = None
    
    def setUp(self):
        """ setUP
        """
        # start the server process
        self.q = Queue()
        self.ps = [Process(target=test_sa, args=(self.q,)),
            Process(target=HRI_Engine_sample.test_engine, args=(8016,"tests/engine_profile/engine_profile_3_1", "client_info1", "urn:x-rois:def:HRIEngine:Kyutech::main", None,)), # loggerを代入するとエラー self.fhを持っていないから？
                        # File "C:\Users\higashi\Documents\pyRoIS_higashi\HRI_Engine_sample.py", line 780, in init_logger
                        # self.logger_client.addHandler(self.fh)
                        # AttributeError: 'IF' object has no attribute 'fh'
            # Process(target=Person_Detection.example_pd, args=(8002,)),
            Process(target=Person_Localization.example_pl, args=(8003,))
            # Process(target=System_Information.example_si, args=(8001,))
            ]
        
        for x in reversed(self.ps[1:]):
            x.start()
            time.sleep(0.5)

        time.sleep(5.0)
        

    def test_execute(self):
        """ test_execute
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