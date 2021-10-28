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
from phrase_api.models.notification_group_detail import NotificationGroupDetail  # noqa: E501
from phrase_api.rest import ApiException

class TestNotificationGroupDetail(unittest.TestCase):
    """NotificationGroupDetail unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test NotificationGroupDetail
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = phrase_api.models.notification_group_detail.NotificationGroupDetail()  # noqa: E501
        if include_optional :
            return NotificationGroupDetail(
                id = '0', 
                event_name = '0', 
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                notifications_count = 56, 
                latest_notification = None
            )
        else :
            return NotificationGroupDetail(
        )

    def testNotificationGroupDetail(self):
        """Test NotificationGroupDetail"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
