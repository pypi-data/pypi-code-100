import contextlib
import os
import tempfile
import unittest
from argparse import Namespace
from io import StringIO
import responses
from requests import Response
from a28 import api, utils
from a28.api import API
from a28.config import ConfigFile


class TestApiMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.test_dir = tempfile.TemporaryDirectory()
        utils.CONFIG_PATH = self.test_dir.name
        utils.CONFIG = os.path.join(utils.CONFIG_PATH, 'config.json')

        self.responses = responses.RequestsMock()
        self.responses.start()

        self.temp_stdout = StringIO()

        self.addCleanup(self.responses.stop)
        self.addCleanup(self.responses.reset)

    def tearDown(self) -> None:
        self.test_dir.cleanup()

    def test_initialize_populate_globals_from_config(self):
        self.responses.add(
            responses.GET,
            'https://assets.a28.io/plugin/endpoints.json',
            json={
                "international": {
                    "api": {
                        "endpoint": "https://api.example.com/v1/"
                    }
                }
            },
            status=200
        )

        api_client = API('international')

        self.assertEqual('https://api.example.com/v1/', api_client.api_endpoint)
        self.assertEqual('international', api_client.region)

    def test_initialize_throws_if_config_is_invalid(self):
        self.responses.add(
            responses.GET,
            'https://assets.a28.io/plugin/endpoints.json',
            json={
                "boo": {
                    "api": {
                        "endpoint": "https://api.example.com/v1/"
                    }
                }
            },
            status=200
        )

        with self.assertRaises(SystemExit) as err:
            with contextlib.redirect_stdout(self.temp_stdout):
                API('international')

        self.assertEqual(err.exception.code, 1)
        self.assertEqual("invalid endpoint", self.temp_stdout.getvalue().strip())

    def test_check_token_with_valid_response(self):
        self.responses.add(
            responses.GET,
            'https://assets.a28.io/plugin/endpoints.json',
            json={
                "international": {
                    "api": {
                        "endpoint": "https://api.example.com/v1/"
                    }
                }
            },
            status=200
        )
        api_client = API('international')

        resp = Response()

        resp._content = b'{"statusCode":200,"status":"SUCCESS","token":"supersecrettoken11"}'
        resp.status_code = 200

        self.assertEqual({}, ConfigFile.load())

        api_client._check_token(resp)

        self.assertEqual({'international': {'token': 'supersecrettoken11'}}, ConfigFile.load())

    def test_check_token_with_non_json_response(self):
        self.responses.add(
            responses.GET,
            'https://assets.a28.io/plugin/endpoints.json',
            json={
                "international": {
                    "api": {
                        "endpoint": "https://api.example.com/v1/"
                    }
                }
            },
            status=200
        )
        api_client = API('international')
        resp = Response()

        resp._content = b'what'
        resp.status_code = 200

        self.assertEqual({}, ConfigFile.load())

        api_client._check_token(resp)

        self.assertEqual({}, ConfigFile.load())

    def test_check_token_with_valid_response_but_no_token(self):
        self.responses.add(
            responses.GET,
            'https://assets.a28.io/plugin/endpoints.json',
            json={
                "international": {
                    "api": {
                        "endpoint": "https://api.example.com/v1/"
                    }
                }
            },
            status=200
        )
        api_client = API('international')
        resp = Response()

        resp._content = b'{"statusCode":200,"status":"SUCCESS"}'
        resp.status_code = 200

        self.assertEqual({}, ConfigFile.load())

        api_client._check_token(resp)

        self.assertEqual({}, ConfigFile.load())

    def test_endpoint_with_valid_response(self):
        self.responses.add(
            responses.GET,
            'https://assets.a28.io/plugin/endpoints.json',
            json={
                "uk": {
                    "api": {
                        "endpoint": "https://api.example.com/v1/"
                    }
                },
                "international": {
                    "api": {
                        "endpoint": "https://api.example.com/v1/"
                    }
                },
                "france": {
                    "api": {
                        "endpoint": "https://api.example.com/v1/"
                    }
                }
            },
            status=200
        )

        with contextlib.redirect_stdout(self.temp_stdout):
            api.endpoints(Namespace())

        self.assertEqual("uk\ninternational\nfrance\ndev", self.temp_stdout.getvalue().strip())

    def test_status_with_correct_response(self):
        self.responses.add(
            responses.GET,
            'https://assets.a28.io/plugin/endpoints.json',
            json={
                "international": {
                    "api": {
                        "endpoint": "https://api.example.com/v1"
                    }
                }
            },
            status=200
        )

        self.responses.add(
            responses.GET,
            'https://api.example.com/v1/status',
            json={"status": "SUCCESS", "statusCode": 200, "message": "im a message"},
            status=200
        )

        with contextlib.redirect_stdout(self.temp_stdout):
            api.status(Namespace(endpoint="international"))

        self.assertEqual("im a message", self.temp_stdout.getvalue().strip())

    def test_status_with_incorrect_response(self):
        self.responses.add(
            responses.GET,
            'https://assets.a28.io/plugin/endpoints.json',
            json={
                "international": {
                    "api": {
                        "endpoint": "https://api.example.com/v1"
                    }
                }
            },
            status=200
        )

        self.responses.add(
            responses.GET,
            'https://api.example.com/v1/status',
            json={"status": "SUCCESS", "statusCode": 200},
            status=200
        )

        with contextlib.redirect_stdout(self.temp_stdout):
            api.status(Namespace(endpoint="international"))

        self.assertEqual("unable to connect to endpoint", self.temp_stdout.getvalue().strip())
