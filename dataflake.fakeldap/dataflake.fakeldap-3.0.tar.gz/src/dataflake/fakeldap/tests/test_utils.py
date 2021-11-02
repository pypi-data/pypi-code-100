##############################################################################
#
# Copyright (c) 2012-2021 Jens Vagelpohl and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import unittest


class HashPwdTests(unittest.TestCase):

    def test_hash_pwd(self):
        from ..utils import hash_pwd
        pwd = hash_pwd('secret')
        self.assertTrue(isinstance(pwd, bytes))
        self.assertTrue(pwd.startswith(b'{SHA}'))

    def test_hash_unicode_pwd(self):
        from ..utils import hash_pwd
        pwd = hash_pwd('bj\xf8rn')
        self.assertTrue(isinstance(pwd, bytes))
        self.assertTrue(pwd.startswith(b'{SHA}'))


class ConstraintUtilTests(unittest.TestCase):

    def test_check_types(self):
        from ..utils import check_types

        @check_types(('test', str), ('test2', bytes))
        def _test_me(test, test2):
            return True

        self.assertTrue(_test_me('stringvalue', b'bytesvalue'))

        with self.assertRaises(TypeError) as context:
            _test_me(b'bytesvalue', 'stringvalue')
        self.assertEqual(str(context.exception),
                         'Parameter "test" must be str, '
                         "found b'bytesvalue' (bytes)")
