"""Library client test module"""

from unittest import TestCase
from matatika.library import MatatikaClient


class TestLibraryClient(TestCase):
    """Test class for library client"""

    def test_value_error_no_access_token_or_client_credentials(self):
        """
        Test a `ValueError` is thrown when a client is instantiated with no `auth_token` or
        `client_id`and`client_secret`
        """

        with self.assertRaises(ValueError) as err:
            MatatikaClient()
            self.assertEqual(
                'An access token or client credentials must be provided', str(err))
