# coding: utf-8

"""
    College Football Data API

    This is an API for accessing all sorts of college football data.  It currently has a wide array of data ranging from play by play to player statistics to game scores and more.  # noqa: E501

    OpenAPI spec version: 2.4.1
    Contact: admin@collegefootballdata.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import cfbd
from cfbd.models.player_game_categories import PlayerGameCategories  # noqa: E501
from cfbd.rest import ApiException


class TestPlayerGameCategories(unittest.TestCase):
    """PlayerGameCategories unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPlayerGameCategories(self):
        """Test PlayerGameCategories"""
        # FIXME: construct object with mandatory attributes with example values
        # model = cfbd.models.player_game_categories.PlayerGameCategories()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
