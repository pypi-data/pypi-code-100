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
from phrase_api.models.team_detail import TeamDetail  # noqa: E501
from phrase_api.rest import ApiException

class TestTeamDetail(unittest.TestCase):
    """TeamDetail unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TeamDetail
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = phrase_api.models.team_detail.TeamDetail()  # noqa: E501
        if include_optional :
            return TeamDetail(
                id = '0', 
                name = '0', 
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                projects = [
                    {"id":"abcd1234cdef1234abcd1234cdef1234","name":"My Android Project","slug":"android_project","main_format":"xml","project_image_url":"http://assets.example.com/project.png","account":"account","space":"space","created_at":"2015-01-28T09:52:53Z","updated_at":"2015-01-28T09:52:53Z"}
                    ], 
                spaces = [
                    {"id":"2e7574e8f2372906a03110c2a7cfe671","name":"My first space","created_at":"2020-02-25T12:17:25Z","updated_at":"2020-03-13T14:46:57Z","projects_count":2,"projects":[{"id":"abcd1234cdef1234abcd1234cdef1234","name":"My Android Project","main_format":"xml","project_image_url":"http://assets.example.com/project.png","account":"account","created_at":"2015-01-28T09:52:53Z","updated_at":"2015-01-28T09:52:53Z"},{"id":"abcd11231fadef1234adacd1234cdef1234","name":"My IOS Project","main_format":"yml","project_image_url":"http://assets.example.com/project2.png","account":"account","created_at":"2015-01-28T09:52:53Z","updated_at":"2015-01-28T09:52:53Z"}]}
                    ], 
                users = [
                    {"id":"abcd1234cdef1234abcd1234cdef1234","username":"joe.doe","name":"Joe Doe","position":"Lead Developer","created_at":"2015-01-28T09:52:53Z","updated_at":"2015-01-28T09:52:53Z"}
                    ]
            )
        else :
            return TeamDetail(
        )

    def testTeamDetail(self):
        """Test TeamDetail"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
