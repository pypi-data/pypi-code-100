# coding: utf-8

"""
    Phrase API Reference

    The version of the OpenAPI document: 2.0.0
    Contact: support@phrase.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import phrase_api
from phrase_api.api.locales_api import LocalesApi  # noqa: E501
from phrase_api.rest import ApiException


class TestLocalesApi(unittest.TestCase):
    """LocalesApi unit test stubs"""

    def setUp(self):
        self.api = phrase_api.api.locales_api.LocalesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_account_locales(self):
        """Test case for account_locales

        List locales used in account  # noqa: E501
        """
        pass

    def test_locale_create(self):
        """Test case for locale_create

        Create a locale  # noqa: E501
        """
        pass

    def test_locale_delete(self):
        """Test case for locale_delete

        Delete a locale  # noqa: E501
        """
        pass

    def test_locale_download(self):
        """Test case for locale_download

        Download a locale  # noqa: E501
        """
        pass

    def test_locale_show(self):
        """Test case for locale_show

        Get a single locale  # noqa: E501
        """
        pass

    def test_locale_update(self):
        """Test case for locale_update

        Update a locale  # noqa: E501
        """
        pass

    def test_locales_list(self):
        """Test case for locales_list

        List locales  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
