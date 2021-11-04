from typing import Optional, Dict, Set

import bottle
import elasticapm
from bottle import request, response
from elasticapm import Client
import elasticapm.instrumentation.control

from bottle_elastic_apm.utils import (
    get_data_from_response,
    get_data_from_request,
)

TRANSACTION_TYPE = "request"


def make_apm_client(config: Optional[Dict] = None, **defaults) -> Client:
    defaults["framework_name"] = bottle.__name__
    defaults["framework_version"] = bottle.__version__
    return Client(config, **defaults)


class ElasticAPM:
    name = "elasticapm"
    api = 2

    def __init__(self, client: Optional[Client] = None, avoided_errors: Optional[Set] = None, **kwargs):
        if not avoided_errors:
            avoided_errors = set()
        self.avoided_errors = avoided_errors
        if client:
            self.client = client
        else:
            self.client = make_apm_client(**kwargs)

        if self.client.config.instrument and self.client.config.enabled:
            elasticapm.instrumentation.control.instrument()

    def setup(self, _app):
        pass

    def apply(self, callback, _context):
        def wrapper(*args, **kwargs):
            self.client.begin_transaction(
                TRANSACTION_TYPE,
                trace_parent=elasticapm.trace_parent_from_headers(request.headers),
            )
            transaction_result = "HTTP 2xx"
            try:
                res = callback(*args, **kwargs)
                transaction_result = self.set_response_information(response)
                return res
            except bottle.HTTPError as error:
                transaction_result = self.set_response_information(error)
                handled = True if transaction_result == "HTTP 4xx" else False
                if error.args not in self.avoided_errors:
                    self.client.capture_exception(handled=handled)
                raise error
            except Exception as error:
                transaction_result = "HTTP 5xx"
                self.client.capture_exception(handled=False)
                raise error
            finally:
                transaction_name = self.set_request_information()
                self.client.end_transaction(transaction_name, transaction_result)

        return wrapper

    def set_request_information(self):
        submodule = request.script_name or ""
        transaction_name = f"{request.method} {submodule[:-1]}{request.route.rule}"
        elasticapm.set_context(
            lambda: get_data_from_request(
                request,
                capture_body=self.client.config.capture_body in ("transactions", "all"),
                capture_headers=self.client.config.capture_headers,
            ),
            "request",
        )
        return transaction_name

    @staticmethod
    def set_response_information(local_response: bottle.BaseResponse):
        transaction_result = f"HTTP {str(local_response.status_code)[0]}xx"
        elasticapm.set_context(
            lambda: get_data_from_response(local_response), "response"
        )
        return transaction_result
