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
from phrase_api.api.documents_api import DocumentsApi  # noqa: E501
from phrase_api.rest import ApiException


class TestDocumentsApi(unittest.TestCase):
    """DocumentsApi unit test stubs"""

    def setUp(self):
        self.api = phrase_api.api.documents_api.DocumentsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_document_delete(self):
        """Test case for document_delete

        Delete document  # noqa: E501
        """
        pass

    def test_documents_list(self):
        """Test case for documents_list

        List documents  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
