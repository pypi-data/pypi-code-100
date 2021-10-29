# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Run the echo service.

The echo service can be run on port 8000 by executing the following::

 $ python -m validatetoken.echo

When the ``validatetoken`` module authenticates a request, the echo service
will respond with all the environment variables presented to it by this
module.
"""
import logging

from wsgiref import simple_server

from oslo_serialization import jsonutils

from validatetoken.middleware import validatetoken

logging.basicConfig(level=logging.DEBUG)


def echo_app(environ, start_response):
    """A WSGI application that echoes the CGI environment back to the user."""
    start_response('200 OK', [('Content-Type', 'application/json')])
    environment = dict((k, v) for k, v in environ.items()
                       if k.startswith('HTTP_X_'))
    yield jsonutils.dumps(environment)


class EchoService(object):
    """Runs an instance of the echo app on init."""

    def __init__(self):
        # hardcode any non-default configuration here
        conf = {
            'www_authenticate_uri': 'https://iam.eu-de.otc.t-systems.com',
            'cache': 'some_key',
            'memcached_servers': ['localhost:11211']
        }
        app = validatetoken.ValidateToken(echo_app, conf)
        server = simple_server.make_server('', 8000, app)
        print('Serving on port 8000 (Ctrl+C to end)...')
        server.serve_forever()
