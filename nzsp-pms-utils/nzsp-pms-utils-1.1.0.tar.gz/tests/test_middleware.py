"""
Middleware functions test
"""
import unittest
import unittest.mock as mock
import xmlrunner
from nzsp_pms_utils.middleware import verify_authorization

class TestMiddleware(unittest.TestCase):
    """
    Test
    """

    @mock.patch('nzsp_pms_utils.middleware.flask')
    def test_verify_authorization_raises_key_error(self, mock_flask):
        """Raises KeyError when no service_name set globally test"""
        mock_flask.g.get.return_value = None
        with self.assertRaises(KeyError):
            verify_authorization()

    @mock.patch('nzsp_pms_utils.middleware.flask')
    @mock.patch('nzsp_pms_utils.middleware.requests')
    def test_verify_authorization_status_200(self, mock_requests, mock_flask):
        """Assign user identifier globally in status 200 test"""
        mock_flask.g.get.return_value = {
            "service_name": "Test"
        }
        user_identifier = "Test"
        mock_requests.get.return_value.status_code = 200
        mock_requests.get.return_value.json.return_value = {
            "user_identifier": user_identifier
        }
        verify_authorization()
        self.assertEqual(mock_flask.g.user_identifier, user_identifier)

    @mock.patch('nzsp_pms_utils.middleware.flask')
    @mock.patch('nzsp_pms_utils.middleware.requests')
    def test_verify_authorization_status_500(self, mock_requests, mock_flask):
        """Response jsonify status in status different that 200 test"""
        mock_flask.g.get.return_value = {
            "service_name": "Test"
        }
        status_code = 500
        mock_requests.get.return_value.status_code = 500
        verify_authorization()
        mock_flask.Response.assert_called_with(status = status_code)

if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False
    )
