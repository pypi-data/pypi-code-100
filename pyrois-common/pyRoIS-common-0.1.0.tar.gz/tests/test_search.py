# HRI_Engine_testNEW.py
#
# Copyright 2017 Eiichi Inohira
# Addition 2018 Ryota Higashi 
# This software may be modified and distributed under the terms
# of the MIT license
#
# For python 3
# For HRI Engine

"""HRI_Engine_example
"""

from __future__ import print_function

import os
import sys
import xml.etree.ElementTree as ET
import glob
import unittest

from pyrois import RoIS_HRI


class TestProfile(unittest.TestCase):
    def test_search(self):
        a = self.search('component_profile_FL')
        return self.assertNotEqual(a[1],["None"])
    def search(self, condition):
        status = RoIS_HRI.ReturnCode_t.OK.value #xmlで接続したい記述．それを探してIDを返す
        component_ref_list = ["None"]
            # List< RoIS_Identifier>
            # とりあえず，conditionに記載したコンポーネント名をxmlファイルの中から探す
        file_list = glob.glob('tests/component_profile/*.xml')
        # print(os.getcwd())
        filename = os.path.join('tests','component_profile',condition + '.xml')
        # print(filename)
        if filename in file_list:
            with open(filename,'r') as f:
                self.component_profile = f.read()
            tree = ET.parse(filename)
            root = tree.getroot()
            text = root.attrib
            component_ref_list = list(text.values())
            # print(component_ref_list)
            
        return (status, component_ref_list)

if __name__ == "__main__":
    unittest.main()
