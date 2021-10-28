# coding: utf-8

"""
    Phrase API Reference

    The version of the OpenAPI document: 2.0.0
    Contact: support@phrase.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import phrase_api
from phrase_api.models.locale_preview1 import LocalePreview1  # noqa: E501
from phrase_api.rest import ApiException

class TestLocalePreview1(unittest.TestCase):
    """LocalePreview1 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test LocalePreview1
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = phrase_api.models.locale_preview1.LocalePreview1()  # noqa: E501
        if include_optional :
            return LocalePreview1(
                id = '0', 
                name = '0', 
                code = '0', 
                project = {"id":"abcd1234cdef1234abcd1234cdef1234","name":"My Android Project","main_format":"xml","created_at":"2015-01-28T09:52:53Z","updated_at":"2015-01-28T09:52:53Z"}
            )
        else :
            return LocalePreview1(
        )

    def testLocalePreview1(self):
        """Test LocalePreview1"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
