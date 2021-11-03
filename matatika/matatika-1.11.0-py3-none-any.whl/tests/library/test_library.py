"""Base library test module"""

from unittest import TestCase
from matatika.library import MatatikaClient


class TestLibrary(TestCase):
    """Test class for library"""

    def setUp(self):

        super().setUp()

        self.client = MatatikaClient(auth_token='auth-token',
                                     client_id='client-id',
                                     client_secret='client-secret',
                                     endpoint_url='endpoint-url',
                                     workspace_id='workspace-id')
