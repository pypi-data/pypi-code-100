"""Catalog test module"""

from unittest.case import TestCase
from unittest.mock import Mock, patch
from requests.models import Response
from requests.sessions import Request
from matatika.catalog import Catalog
from matatika.library import MatatikaClient


class TestCatalog(TestCase):
    """Test class for catalog operations"""

    def setUp(self):
        client = MatatikaClient(auth_token='auth-token',
                                client_id='client-id',
                                client_secret='client-secret',
                                endpoint_url='endpoint-url',
                                workspace_id='workspace-id')

        self.catalog = Catalog(client)

    @patch('matatika.catalog.get_access_token')
    def test_new_access_token(self, mock_get_access_token: Mock):
        """Test new access token given `client_id`, `client_secret` and no `auth_token`"""

        mock_get_access_token.return_value = 'mock-access-token'

        client = MatatikaClient(client_id='client-id',
                                client_secret='client-secret')
        self.assertIsNone(client.auth_token)

        Catalog(client)
        self.assertEqual(mock_get_access_token.return_value, client.auth_token)

    @patch('matatika.catalog.get_access_token')
    @patch('matatika.catalog.requests.Session.send')
    def test_refresh_access_token_on_401(self, mock_get_profile: Mock, mock_get_access_token: Mock):
        """Test refresh access token logic when `401 Unauthorized` is returned"""

        mock_get_access_token.return_value = 'mock-access-token'

        bad_auth_request = Request()
        bad_auth_request.method = 'GET'
        bad_auth_request.url = 'http://test'

        bad_auth_response = Response()
        bad_auth_response.request = self.catalog.session.prepare_request(
            bad_auth_request)
        bad_auth_response.status_code = 401

        new_auth_response = Response()
        new_auth_response.status_code = 200
        new_auth_response.headers['Authorization'] = f'Bearer {mock_get_access_token.return_value}'
        mock_get_profile.return_value = new_auth_response

        # pylint: disable=protected-access
        self.catalog._refresh_access_token(bad_auth_response)

        self.assertEqual(new_auth_response.headers['Authorization'],
                         self.catalog.session.headers['Authorization'])
        self.assertListEqual([], bad_auth_response.request.hooks['response'])
        self.assertEqual(mock_get_access_token.return_value,
                         self.catalog.client.auth_token)

    @patch('matatika.catalog.get_access_token')
    def test_no_refresh_access_token_on_non_401(self, mock_get_access_token: Mock):
        """Test refresh access token logic when any non-401 status is returned"""

        ok_auth_response = Response()
        ok_auth_response.status_code = 200

        # pylint: disable=protected-access
        self.catalog._refresh_access_token(ok_auth_response)
        mock_get_access_token.assert_not_called()

    @patch('matatika.catalog.get_access_token')
    def test_no_refresh_access_token_when_no_client_id_or_secret(self, mock_get_access_token: Mock):
        """Test refresh access token logic when any non-401 status is returned"""

        ok_auth_response = Response()
        ok_auth_response.status_code = 200

        self.catalog.client_id = None
        self.catalog.client_secret = None

        # pylint: disable=protected-access
        self.catalog._refresh_access_token(ok_auth_response)
        mock_get_access_token.assert_not_called()
