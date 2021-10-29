# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import copy
import datetime
import logging

from unittest import mock

import fixtures
import requests
from requests_mock.contrib import fixture as rm_fixture
import webob

from keystonemiddleware.auth_token import _cache
from keystonemiddleware.tests.unit.auth_token import base
from keystonemiddleware.tests.unit.auth_token.test_auth_token_middleware \
        import (TimeFixture)
import oslo_cache
from oslo_utils import timeutils

from validatetoken.middleware import validatetoken

BASE_HOST = 'https://keystone.example.com'
BASE_URI = '%s/testadmin' % BASE_HOST

EXPECTED_V3_DEFAULT_ENV_ADDITIONS = {
    'HTTP_X_PROJECT_DOMAIN_ID': 'domain_id1',
    'HTTP_X_PROJECT_DOMAIN_NAME': 'domain_name1',
    'HTTP_X_USER_DOMAIN_ID': 'domain_id1',
    'HTTP_X_USER_DOMAIN_NAME': 'domain_name1',
    'HTTP_X_IS_ADMIN_PROJECT': 'True'
}

GOOD_RESPONSE = {
    "token": {
        "expires_at": "2021-01-02T00:00:00.00000Z",
        "methods": ["password"],
        "catalog": "<removed>",
        "roles": [
            {"id": "0", "name": "not_admin"},
            {"id": "1", "name": "nova"},
        ],
        "project": {
            "domain": {
                "id": "fake_domain_id",
                "name": "fake_domain_name"
            },
            "id": "fake_project_id",
            "name": "fake_project_name"
        },
        "issued_at": "2021-01-01T00:00:00.000000Z",
        "user": {
            "domain": {
                "id": "fake_user_domain_id",
                "name": "fake_user_domain_name"
            },
            "id": "fake_user_id",
            "name": "fake_user_name",
            "password_expires_at": ""
        }
    }
}


class FakeResponse(object):
    reason = "Test Reason"
    headers = {'x-subject-token': 'fake_token'}

    def __init__(self, json, status_code=400):
        self._json = json
        self.text = json
        self.status_code = status_code

    def json(self):
        return self._json


class FakeApp(object):
    """This represents a WSGI app protected by the auth_token middleware."""

    SUCCESS = b'SUCCESS'
    FORBIDDEN = b'FORBIDDEN'
    expected_env = {}

    def __init__(self, expected_env=None, need_service_token=False):
        self.expected_env = dict()

        if expected_env:
            self.expected_env.update(expected_env)

        self.need_service_token = need_service_token

    @webob.dec.wsgify
    def __call__(self, req):
        for k, v in self.expected_env.items():
            assert req.environ[k] == v, '%s != %s' % (req.environ[k], v)

        resp = webob.Response()
        resp.body = FakeApp.SUCCESS

        return resp


class FakeOsloCache(_cache._FakeClient):
    """A fake oslo_cache object.

    The memcache and oslo_cache interfaces are almost the same except we need
    to return NO_VALUE when not found.
    """

    def get(self, key):
        return super(FakeOsloCache, self).get(key) or oslo_cache.NO_VALUE


class ValidateTokenMiddlewareTestBase(base.BaseAuthTokenTestCase):
    TEST_AUTH_URL = 'https://keystone.example.com'
    TEST_URL = '%s/v3/auth/tokens' % (TEST_AUTH_URL,)

    def setUp(self, expected_env=None, auth_version=None, fake_app=None):
        super(ValidateTokenMiddlewareTestBase, self).setUp()

        self.logger = self.useFixture(fixtures.FakeLogger(level=logging.DEBUG))

        # the default oslo_cache is null cache, always use an in-mem cache
        self.useFixture(fixtures.MockPatchObject(validatetoken.ValidateToken,
                                                 '_create_oslo_cache',
                                                 return_value=FakeOsloCache()))

        self.expected_env = expected_env or dict()
        self.fake_app = fake_app or FakeApp
        self.middleware = None

        self.conf = {
            'www_authenticate_uri': self.TEST_AUTH_URL,
        }

        self.requests_mock = self.useFixture(rm_fixture.Fixture())

        self.token_dict = {
            'uuid_token_default': '5603457654b346fdbb93437bfe76f2f1'
        }

    def start_fake_response(self, status, headers):
        self.response_status = int(status.split(' ', 1)[0])
        self.response_headers = dict(headers)

    def call_middleware(self, **kwargs):
        return self.call(self.middleware, **kwargs)

    def set_middleware(self, expected_env=None, conf=None):
        """Configure the class ready to call the auth_token middleware.

        Set up the various fake items needed to run the middleware.
        Individual tests that need to further refine these can call this
        function to override the class defaults.
        """
        if conf:
            self.conf.update(conf)

        if expected_env:
            self.expected_env.update(expected_env)

        self.middleware = validatetoken.ValidateToken(
            self.fake_app(self.expected_env), self.conf)


class ValidateTokenMiddlewareTestGood(ValidateTokenMiddlewareTestBase):

    def setUp(self):
        super(ValidateTokenMiddlewareTestGood, self).setUp()
        self.middleware = validatetoken.ValidateToken(FakeApp(), self.conf)

        response = copy.deepcopy(GOOD_RESPONSE)
        expires_at = datetime.datetime.now() + datetime.timedelta(hours=1)
        response['token']['expires_at'] = expires_at.isoformat()

        self.requests_mock.get(self.TEST_URL,
                               status_code=200,
                               headers={
                                   'Content-Type': 'application/json'
                               },
                               json=response)

    # Ignore the request and pass to the next middleware in the
    # pipeline if no path has been specified.
    def test_no_path_request(self):
        req = webob.Request.blank('/')
        self.middleware(req.environ, self.start_fake_response)
        self.assertEqual(self.response_status, 200)

    # Ignore the request and pass to the next middleware in the
    # pipeline if no Authorization header has been specified
    def test_without_authorization(self):
        req = webob.Request.blank('/dummy')
        self.middleware(req.environ, self.start_fake_response)
        self.assertEqual(self.response_status, 200)

    @mock.patch.object(requests, 'request')
    def test_token_request(self, mr):
        req = webob.Request.blank('/dummy')
        req.headers['X-Auth-Token'] = 'token'

        mr.return_value = FakeResponse(GOOD_RESPONSE, 200)

        req.get_response(self.middleware)
        mr.assert_called_with(
            'GET',
            'https://keystone.example.com/v3/auth/tokens',
            headers={
                'X-Auth-Token': 'token',
                'X-Subject-Token': 'token'},
            timeout=None
        )

    def test_authenticated(self):
        req = webob.Request.blank('/dummy')
        req.headers['X-Auth-Token'] = 'token'

        resp = req.get_response(self.middleware)
        self.assertEqual(resp.status_int, 200)

        token = GOOD_RESPONSE['token']
        env = req.environ
        self.assertEqual(
            'Confirmed',
            env['HTTP_X_IDENTITY_STATUS']
        )
        self.assertEqual(
            token['user']['id'],
            env['HTTP_X_USER_ID']
        )
        self.assertEqual(
            token['user']['name'],
            env['HTTP_X_USER_NAME']
        )

        self.assertEqual(
            token['user']['domain']['id'],
            env['HTTP_X_USER_DOMAIN_ID']
        )
        self.assertEqual(
            token['user']['domain']['name'],
            env['HTTP_X_USER_DOMAIN_NAME']
        )
        self.assertEqual(
            token['project']['id'],
            env['HTTP_X_PROJECT_ID']
        )
        self.assertEqual(
            token['project']['name'],
            env['HTTP_X_PROJECT_NAME']
        )

        self.assertEqual(
            token['project']['domain']['id'],
            env['HTTP_X_PROJECT_DOMAIN_ID']
        )
        self.assertEqual(
            token['project']['domain']['name'],
            env['HTTP_X_PROJECT_DOMAIN_NAME']
        )
        self.assertEqual(
            ','.join([f['name'] for f in token['roles']]),
            env['HTTP_X_ROLES']
        )


class ValidateTokenMiddlewareTestBad(ValidateTokenMiddlewareTestBase):

    def setUp(self):
        super(ValidateTokenMiddlewareTestBad, self).setUp()
        self.middleware = validatetoken.ValidateToken(FakeApp(), self.conf)

        self.requests_mock.get(self.TEST_URL,
                               status_code=200,
                               json=GOOD_RESPONSE)

    def test_token_expired(self):
        req = webob.Request.blank('/dummy')
        req.headers['X-Auth-Token'] = 'token'

        resp = req.get_response(self.middleware)
        self.assertEqual(resp.status_int, 401)

    def test_token_invalid(self):
        self.requests_mock.get(
            self.TEST_URL, status_code=401,
            headers={'Content-Type': 'application/json'},
            json={'error': 'token invalid'})

        req = webob.Request.blank('/dummy')
        req.headers['X-Auth-Token'] = 'token'

        resp = req.get_response(self.middleware)
        self.assertEqual(resp.status_int, 401)


class Caching(ValidateTokenMiddlewareTestBase):
    def setUp(self):
        super().setUp()
        self.middleware = validatetoken.ValidateToken(FakeApp(), self.conf)

    def _get_cached_token(self, token):
        return self.middleware._token_cache.get(token)

    def test_memcache_set_invalid_uuid(self):
        self.requests_mock.get(self.TEST_URL, status_code=404)

        token = 'invalid-token'
        self.call_middleware(headers={'X-Auth-Token': token},
                             expected_status=401)
        self.assertEqual(validatetoken._CACHE_INVALID_INDICATOR,
                         self._get_cached_token(token))

    def test_memcache_hit_invalid_token(self):
        token = 'invalid-token'
        self.requests_mock.get(self.TEST_URL, status_code=404)

        # Call once to cache token's invalid state; verify it cached as such
        self.call_middleware(headers={'X-Auth-Token': token},
                             expected_status=401)
        self.assertEqual(validatetoken._CACHE_INVALID_INDICATOR,
                         self._get_cached_token(token))

        # Call again for a cache hit; verify it detected as cached and invalid
        self.call_middleware(headers={'X-Auth-Token': token},
                             expected_status=401)
        self.assertIn('Cached token is marked unauthorized',
                      self.logger.output)

    def test_memcache_set_expired(self, extra_conf={}, extra_environ={}):
        response = copy.deepcopy(GOOD_RESPONSE)
        expires_at = datetime.datetime.now() + datetime.timedelta(hours=1)
        response['token']['expires_at'] = expires_at.isoformat()

        self.requests_mock.get(self.TEST_URL,
                               status_code=200,
                               headers={
                                   'Content-Type': 'application/json'
                               },
                               json=response)

        token_cache_time = 10
        conf = {
            'token_cache_time': '%s' % token_cache_time,
        }
        conf.update(extra_conf)
        self.set_middleware(conf=conf)

        token = self.token_dict['uuid_token_default']
        self.call_middleware(headers={'X-Auth-Token': token})

        req = webob.Request.blank('/')
        req.headers['X-Auth-Token'] = token
        req.environ.update(extra_environ)

        now = datetime.datetime.utcnow()
        self.useFixture(TimeFixture(now))
        req.get_response(self.middleware)
        self.assertIsNotNone(self._get_cached_token(token))

        timeutils.advance_time_seconds(token_cache_time)
        self.assertIsNone(self._get_cached_token(token))

    def test_http_error_not_cached_token(self):
        """Test to don't cache token as invalid on network errors.

        We use UUID tokens since they are the easiest one to reach
        get_http_connection.
        """
        self.requests_mock.get(self.TEST_URL, status_code=503)
        self.set_middleware(conf={'http_request_max_retries': '0'})
        self.call_middleware(headers={'X-Auth-Token': 'invalid-token'},
                             expected_status=503)
        self.assertIsNone(self._get_cached_token('invalid-token'))


class CachePoolTest(ValidateTokenMiddlewareTestBase):
    def test_use_cache_from_env(self):
        # If `swift.cache` is set in the environment and `cache` is set in the
        # config then the env cache is used.
        env = {'swift.cache': 'CACHE_TEST'}
        conf = {
            'cache': 'swift.cache'
        }
        self.set_middleware(conf=conf)
        self.middleware._token_cache.initialize(env)
        with self.middleware._token_cache._cache_pool.reserve() as cache:
            self.assertEqual(cache, 'CACHE_TEST')

    def test_not_use_cache_from_env(self):
        # If `swift.cache` is set in the environment but `cache` isn't set
        # initialize the config then the env cache isn't used.
        self.set_middleware()
        env = {'swift.cache': 'CACHE_TEST'}
        self.middleware._token_cache.initialize(env)
        with self.middleware._token_cache._cache_pool.reserve() as cache:
            self.assertNotEqual(cache, 'CACHE_TEST')

    def test_multiple_context_managers_share_single_client(self):
        self.set_middleware()
        token_cache = self.middleware._token_cache
        env = {}
        token_cache.initialize(env)

        caches = []

        with token_cache._cache_pool.reserve() as cache:
            caches.append(cache)

        with token_cache._cache_pool.reserve() as cache:
            caches.append(cache)

        self.assertIs(caches[0], caches[1])
        self.assertEqual(set(caches), set(token_cache._cache_pool))

    def test_nested_context_managers_create_multiple_clients(self):
        self.set_middleware()
        env = {}
        self.middleware._token_cache.initialize(env)
        token_cache = self.middleware._token_cache

        with token_cache._cache_pool.reserve() as outer_cache:
            with token_cache._cache_pool.reserve() as inner_cache:
                self.assertNotEqual(outer_cache, inner_cache)

        self.assertEqual(
            set([inner_cache, outer_cache]),
            set(token_cache._cache_pool))
