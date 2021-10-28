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
from phrase_api.models.locale_details import LocaleDetails  # noqa: E501
from phrase_api.rest import ApiException

class TestLocaleDetails(unittest.TestCase):
    """LocaleDetails unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test LocaleDetails
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = phrase_api.models.locale_details.LocaleDetails()  # noqa: E501
        if include_optional :
            return LocaleDetails(
                id = '0', 
                name = '0', 
                code = '0', 
                default = True, 
                main = True, 
                rtl = True, 
                plural_forms = [
                    '0'
                    ], 
                source_locale = {"id":"abcd1234cdef1234abcd1234cdef1234","name":"English","code":"en-GB"}, 
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                statistics = phrase_api.models.locale_statistics.locale_statistics(
                    keys_total_count = 56, 
                    keys_untranslated_count = 56, 
                    words_total_count = 56, 
                    translations_completed_count = 56, 
                    translations_unverified_count = 56, 
                    unverified_words_count = 56, 
                    missing_words_count = 56, )
            )
        else :
            return LocaleDetails(
        )

    def testLocaleDetails(self):
        """Test LocaleDetails"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
