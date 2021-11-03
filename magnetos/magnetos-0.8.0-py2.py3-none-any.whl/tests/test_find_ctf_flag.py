# -*- coding: utf-8 -*-
# created by restran on 2019/08/01
from __future__ import unicode_literals, absolute_import
import unittest
import json
from magnetos.utils.find_ctf_flag import clean_find_ctf_flag_result


class FindCTFFlagTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_clean_find_ctf_flag_result(self):
        result = ['flag123', 'flag{123}', 'abcd']
        result_list = clean_find_ctf_flag_result(result)
        expected = ['flag{123}', 'flag123', 'abcd']
        self.assertEqual(json.dumps(expected), json.dumps(result_list))


if __name__ == '__main__':
    unittest.main()
