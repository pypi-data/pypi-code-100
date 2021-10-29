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
import json
import requests

import webob.dec

import iso8601

from keystonemiddleware._common import config
from keystonemiddleware.auth_token import _cache
from keystonemiddleware.auth_token import _exceptions as ksm_exceptions
import oslo_cache
from oslo_config import cfg
from oslo_log import log as logging
from oslo_serialization import jsonutils

_CACHE_INVALID_INDICATOR = 'invalid'
VALIDATETOKEN_MIDDLEWARE_GROUP = 'validatetoken'

_VALIDATETOKEN_OPTS = [
    cfg.StrOpt('www_authenticate_uri',
               deprecated_name='auth_uri',
               help='Complete "public" Identity API endpoint. This endpoint'
               ' should not be an "admin" endpoint, as it should be accessible'
               ' by all end users. Unauthenticated clients are redirected to'
               ' this endpoint to authenticate. Although this endpoint should'
               ' ideally be unversioned, client support in the wild varies.'
               ' If you\'re using a versioned v2 endpoint here, then this'
               ' should *not* be the same endpoint the service user utilizes'
               ' for validating tokens, because normal end users may not be'
               ' able to reach that endpoint.'),
    cfg.BoolOpt('delay_auth_decision',
                default=False,
                help='Do not handle authorization requests within the'
                ' middleware, but delegate the authorization decision to'
                ' downstream WSGI components.'),
    cfg.IntOpt('http_connect_timeout',
               help='Request timeout value for communicating with Identity'
               ' API server.'),
    cfg.IntOpt('http_request_max_retries',
               default=3,
               help='How many times are we trying to reconnect when'
               ' communicating with Identity API Server.'),
    cfg.StrOpt('cache',
               help='Request environment key where the Swift cache object is'
               ' stored. When auth_token middleware is deployed with a Swift'
               ' cache, use this option to have the middleware share a caching'
               ' backend with swift. Otherwise, use the ``memcached_servers``'
               ' option instead.'),
    cfg.StrOpt('region_name',
               help='The region in which the identity server can be found.'),
    cfg.ListOpt('memcached_servers',
                deprecated_name='memcache_servers',
                help='Optionally specify a list of memcached server(s) to'
                ' use for caching. If left undefined, tokens will instead be'
                ' cached in-process.'),
    cfg.IntOpt('token_cache_time',
               default=300,
               help='In order to prevent excessive effort spent validating'
               ' tokens, the middleware caches previously-seen tokens for a'
               ' configurable duration (in seconds). Set to -1 to disable'
               ' caching completely.'),
    cfg.StrOpt('memcache_security_strategy',
               default='None',
               choices=('None', 'MAC', 'ENCRYPT'),
               ignore_case=True,
               help='(Optional) If defined, indicate whether token data'
               ' should be authenticated or authenticated and encrypted.'
               ' If MAC, token data is authenticated (with HMAC) in the cache.'
               ' If ENCRYPT, token data is encrypted and authenticated in the'
               ' cache. If the value is not one of these options or empty,'
               ' auth_token will raise an exception on initialization.'),
    cfg.StrOpt('memcache_secret_key',
               secret=True,
               help='(Optional, mandatory if memcache_security_strategy is'
               ' defined) This string is used for key derivation.'),
    cfg.IntOpt('memcache_pool_dead_retry',
               default=5 * 60,
               help='(Optional) Number of seconds memcached server is'
               ' considered dead before it is tried again.'),
    cfg.IntOpt('memcache_pool_maxsize',
               default=10,
               help='(Optional) Maximum total number of open connections to'
               ' every memcached server.'),
    cfg.IntOpt('memcache_pool_socket_timeout',
               default=3,
               help='(Optional) Socket timeout in seconds for communicating '
                    'with a memcached server.'),
    cfg.IntOpt('memcache_pool_unused_timeout',
               default=60,
               help='(Optional) Number of seconds a connection to memcached'
               ' is held unused in the pool before it is closed.'),
    cfg.IntOpt('memcache_pool_conn_get_timeout',
               default=10,
               help='(Optional) Number of seconds that an operation will wait '
                    'to get a memcached client connection from the pool.'),
    cfg.BoolOpt('memcache_use_advanced_pool',
                default=True,
                help='(Optional) Use the advanced (eventlet safe) memcached '
                     'client pool.'),
]
CONF = cfg.CONF
CONF.register_opts(_VALIDATETOKEN_OPTS, group=VALIDATETOKEN_MIDDLEWARE_GROUP)

oslo_cache.configure(cfg.CONF)


class ValidateToken:
    """Validate token middleware

    Fetches the token with the token itself to get it information
    """

    def __init__(self, app, conf):
        self.app = app
        self.conf = conf
        self._conf = config.Config(
            'validatetoken', VALIDATETOKEN_MIDDLEWARE_GROUP, _list_opts(), conf
        )
        self.log = logging.getLogger(conf.get('log_name', __name__))
        self.log.info('Starting validatetoken middleware')

        self._www_authenticate_uri = conf.get('www_authenticate_uri')
        auth_uri = conf.get('auth_uri')
        if not self._www_authenticate_uri and auth_uri:
            self._www_authenticate_uri = auth_uri
        if not self._www_authenticate_uri:
            self.log.fatal(
                'Configuring www_authenticate_uri to point to the public '
                'identity endpoint is required; clients may not be able to '
                'authenticate against an admin endpoint')
            raise RuntimeError

        self._delay_auth_decision = self._conf.get('delay_auth_decision')

        self._token_cache = self._token_cache_factory()

    def _deny_request(self, response=None, message=None, status_code=401):
        """Return error response"""
        if response:
            try:
                body = jsonutils.dumps(response)
            except Exception:
                body = response.text
        elif message:
            body = jsonutils.dumps({'error': {
                'code': status_code,
                'title': 'Unauthorized',
                'message': message,
            }})
        resp = webob.Response()
        resp.status = status_code
        resp.headers['Content-Type'] = 'application/json'
        resp.body = body.encode()
        return resp

    def __call__(self, environ, start_response):
        self.log.debug('Entering Validating token auth %s' % environ)
        self._token_cache.initialize(environ)
        token = environ.get('HTTP_X_AUTH_TOKEN')
        if token:
            try:
                data = self.fetch_token(token)
                token_info = data.get('token')
                token_expires = token_info.get('expires_at')
                current_time = datetime.datetime.now(datetime.timezone.utc)
                if current_time >= iso8601.parse_date(token_expires):
                    return self._deny_request(
                        message='Token expired')(environ, start_response)
                environ['HTTP_X_IDENTITY_STATUS'] = 'Confirmed'
                environ['keystone.token_info'] = data
                domain = token_info.get('domain')
                if domain:
                    environ['HTTP_X_DOMAIN_ID'] = domain.get('id')
                    environ['HTTP_X_DOMAIN_NAME'] = domain.get('name')
                project = token_info.get('project')
                if project:
                    environ['HTTP_X_PROJECT_ID'] = project.get('id')
                    environ['HTTP_X_PROJECT_NAME'] = project.get('name')
                    pd = project.get('domain')
                    if pd:
                        environ['HTTP_X_PROJECT_DOMAIN_ID'] = pd.get('id')
                        environ['HTTP_X_PROJECT_DOMAIN_NAME'] = pd.get('name')
                user = token_info.get('user')
                if user:
                    environ['HTTP_X_USER_ID'] = user.get('id')
                    environ['HTTP_X_USER_NAME'] = user.get('name')
                    ud = user.get('domain')
                    if ud:
                        environ['HTTP_X_USER_DOMAIN_ID'] = ud.get('id')
                        environ['HTTP_X_USER_DOMAIN_NAME'] = ud.get('name')
                roles = token_info.get('roles')
                if roles:
                    environ['HTTP_X_ROLES'] = ','.join(
                        [f['name'] for f in roles])

            except KeyError:
                return self._deny_request(
                    message='Can not process token data')(
                        environ, start_response)
            except ksm_exceptions.InvalidToken:
                self.log.debug('Token validation failure.', exc_info=True)
                return self._deny_request(
                    message='Invalid token')(
                        environ, start_response)
            except ksm_exceptions.ServiceError:
                return self._deny_request(
                    message='Keystone is temporarily not available',
                    status_code=503
                )(environ, start_response)

        return self.app(environ, start_response)

    def fetch_token(self, token):
        """Retrieve token either from cache or from Keystone"""
        data = None
        try:
            cached = self._token_cache.get(token)
            if cached:
                self.log.debug('Token found in cache')
                if cached == _CACHE_INVALID_INDICATOR:
                    self.log.debug('Cached token is marked unauthorized')
                    raise ksm_exceptions.InvalidToken()

                data = cached
            else:
                data = self._check_token(token)
                self._token_cache.set(token, data)

            token_info = data.get('token')
            token_expires = token_info.get('expires_at')
            current_time = datetime.datetime.now(datetime.timezone.utc)
            if current_time >= iso8601.parse_date(token_expires):
                self.log.debug('Token expired.')
                raise ksm_exceptions.InvalidToken('Token Expired.')

        except (
            ksm_exceptions.ServiceError,
            requests.RequestException,
            json.decoder.JSONDecodeError
        ) as e:
            self.log.critical('Unable to validate token: %s', e)
            if self._delay_auth_decision:
                self.log.debug('Keystone unavailable; marking token as '
                               'invalid and deferring auth decision.')
                raise ksm_exceptions.InvalidToken(
                    'Keystone unavailable: %s' % e)
            raise ksm_exceptions.ServiceError(
                'The Keystone service is temporarily unavailable.'
            )
        except ksm_exceptions.InvalidToken:
            self.log.debug('Token validation failure.')
            self._token_cache.set(token, _CACHE_INVALID_INDICATOR)
            self.log.warning('Authorization failed for token')
            raise

        return data

    def _check_token(self, token):
        self.log.debug('Verifying token')
        retries = self._conf.get('http_request_max_retries')
        response = None
        while retries >= 0:
            try:
                response = requests.request(
                    'GET',
                    '%s/v3/auth/tokens' % self._www_authenticate_uri,
                    headers={
                        'X-Auth-Token': token,
                        'X-Subject-Token': token
                        },
                    timeout=self._conf.get('http_connect_timeout')
                )
                if response.status_code < 500:
                    # Something "reasonable". Do not retry
                    break
            except requests.RequestException:
                if retries <= 0:
                    raise
            retries -= 1

        if response.status_code >= 500:
            raise ksm_exceptions.ServiceError(
                'Keystone returned: %s' % response.status_code)
        if response.status_code != 200:
            raise ksm_exceptions.InvalidToken(
                'Keystone rejected token: %s' % response.text)

        return response.json()

    def _create_oslo_cache(self):
        # having this as a function makes test mocking easier
        region = oslo_cache.create_region()
        oslo_cache.configure_cache_region(self._conf.oslo_conf_obj, region)
        return region

    def _token_cache_factory(self):

        security_strategy = self._conf.get('memcache_security_strategy')

        cache_kwargs = dict(
            cache_time=int(self._conf.get('token_cache_time')),
            env_cache_name=self._conf.get('cache'),
            memcached_servers=self._conf.get('memcached_servers'),
            use_advanced_pool=self._conf.get('memcache_use_advanced_pool'),
            dead_retry=self._conf.get('memcache_pool_dead_retry'),
            maxsize=self._conf.get('memcache_pool_maxsize'),
            unused_timeout=self._conf.get('memcache_pool_unused_timeout'),
            conn_get_timeout=self._conf.get('memcache_pool_conn_get_timeout'),
            socket_timeout=self._conf.get('memcache_pool_socket_timeout'),
        )

        if security_strategy.lower() != 'none':
            secret_key = self._conf.get('memcache_secret_key')
            return _cache.SecureTokenCache(
                self.log, security_strategy, secret_key, **cache_kwargs)
        else:
            return _cache.TokenCache(self.log, **cache_kwargs)


def _list_opts():
    """Return a list of oslo_config options available in validatetoken middleware.

    The returned list includes all oslo_config options which may be registered
    at runtime by the project.
    Each element of the list is a tuple. The first element is the name of the
    group under which the list of elements in the second element will be
    registered. A group name of None corresponds to the [DEFAULT] group in
    config files.
    :returns: a list of (group_name, opts) tuples
    """
    return [
        (VALIDATETOKEN_MIDDLEWARE_GROUP, copy.deepcopy(_VALIDATETOKEN_OPTS))
    ]


def filter_factory(global_conf, **local_conf):
    """Standard filter factory to use the middleware with paste.deploy"""

    conf = global_conf.copy()
    conf.update(local_conf)

    def auth_filter(app):
        return ValidateToken(app, conf)

    return auth_filter
