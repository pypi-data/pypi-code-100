from typing import Dict

import requests
import httpretty

from tests.instrumentation.base_http_instrumentor_test import BaseHttpInstrumentorTest

TEST_URL = 'http://test.com'
MOCKED_RESPONSE_BODY = 'A Mocked Response'


class TestHeliosphereRequestsInstrumentor(BaseHttpInstrumentorTest):

    @httpretty.activate
    def test_instrument(self):
        headers = {self.RESPONSE_TEST_HEADER_KEY: self.RESPONSE_TEST_HEADER_VALUE}
        httpretty.register_uri(httpretty.POST, TEST_URL, body=MOCKED_RESPONSE_BODY, **headers)

        request_body = {'param1': 1, 'param2': 2}
        requests.post(TEST_URL, data=request_body, headers={self.REQUEST_TEST_HEADER_KEY: self.REQUEST_TEST_HEADER_VALUE})

        self.tracer_provider.force_flush()

        requests_span = None
        for span in self.span_exporter.get_finished_spans():
            name = span.attributes['otel.library.name']
            if name == 'opentelemetry.instrumentation.requests':
                requests_span = span

        self.assertIsNotNone(requests_span)

        self.assert_request_headers(requests_span)
        self.assert_request_body(requests_span, self.expected_request_body(request_body))

        self.assert_response_headers(requests_span)
        self.assert_response_body(requests_span, MOCKED_RESPONSE_BODY)

    @staticmethod
    def expected_request_body(param_dict: Dict) -> str:
        body = ''
        for key, value in param_dict.items():
            if body != '':
                body += '&'
            body += f'{key}={value}'
        return body
