import flask
import random
import werkzeug

import random
from lariat.patch.statsd_config import DEFAULT_STATSD_CLIENT as Instrumentation

import sys
import logging
from urllib import parse

log = logging.getLogger(__name__)


def patch():
    try:
        _wsgi_app = flask.app.Flask.wsgi_app
        _finalize_request = flask.app.Flask.finalize_request

        def wsgi_app_patched(self, environ, start_response):
            request = werkzeug.Request(environ)
            reqid = Instrumentation.context.start()
            Instrumentation.event(
                reqid,
                "flask.request",
                meta={
                    "method": request.method,
                    "base_url": request.base_url,
                    "query_params": {
                        k.decode('utf-8'): [v.decode('utf-8') for v in vs]\
                                for k, vs in parse.parse_qs(request.query_string).items()},
                },
            )

            ctx = self.request_context(environ)
            error = None
            try:
                try:
                    ctx.push()
                    from flask import g; g._lariat_request_id = reqid
                    response = self.full_dispatch_request()
                except Exception as e:
                    error = e
                    response = self.handle_exception(e)
                except:  # noqa: B001
                    error = sys.exc_info()[1]
                    raise
                return response(environ, start_response)
            finally:
                if self.should_ignore_error(error):
                    error = None
                ctx.auto_pop(error)

        flask.app.Flask.wsgi_app = wsgi_app_patched

        def finalize_request_patched(self, rv, from_error_handler=False):
            from flask import g; reqid = g._lariat_request_id
            response = _finalize_request(self, rv, from_error_handler)

            Instrumentation.event(
                reqid,
                "flask.response",
                meta={
                    "json": response.json,  # this just returns None if the app's response is not json
                    "status_code": response.status_code,
                },
            )
            return response

        flask.app.Flask.finalize_request = finalize_request_patched

    except Exception:
        log.info("could not patch flask app")
