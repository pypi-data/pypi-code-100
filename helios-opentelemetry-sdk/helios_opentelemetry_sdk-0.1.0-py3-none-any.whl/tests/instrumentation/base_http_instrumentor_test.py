import json

from opentelemetry.sdk.trace import ReadableSpan

from heliosphere.instrumentation.base_http_instrumentor import HeliosphereBaseHttpInstrumentor
from tests.instrumentation.base import BaseInstrumentorTest


class BaseHttpInstrumentorTest(BaseInstrumentorTest):

    REQUEST_TEST_HEADER_KEY = 'Request-Test-Header'
    REQUEST_TEST_HEADER_VALUE = 'request_test_header'
    RESPONSE_TEST_HEADER_KEY = 'response-test-header'
    RESPONSE_TEST_HEADER_VALUE = 'response_test_header'

    def assert_headers(self, span: ReadableSpan, attribute_name: str, header_name: str, header_value: str):
        headers = span.attributes.get(attribute_name, None)
        self.assertIsNotNone(headers)

        headers = json.loads(headers)
        test_header = headers.get(header_name)

        if test_header is None:
            test_header = headers.get(header_name.lower())

        if test_header is None:
            test_header = headers.get(header_name.upper().replace("-", "_"))

        self.assertEqual(test_header, header_value)

    def assert_request_headers(self, span: ReadableSpan):
        self.assert_headers(span, HeliosphereBaseHttpInstrumentor.HTTP_REQUEST_HEADERS_ATTRIBUTE_NAME,
                            self.REQUEST_TEST_HEADER_KEY, self.REQUEST_TEST_HEADER_VALUE)

    def assert_response_headers(self, span: ReadableSpan):
        self.assert_headers(span, HeliosphereBaseHttpInstrumentor.HTTP_RESPONSE_HEADERS_ATTRIBUTE_NAME,
                            self.RESPONSE_TEST_HEADER_KEY, self.RESPONSE_TEST_HEADER_VALUE)

    def assert_body(self, span: ReadableSpan, attribute_name: str, expected_body: str):
        body = span.attributes.get(attribute_name, None)
        self.assertEqual(body, expected_body)

    def assert_request_body(self, span: ReadableSpan, expected_body: str):
        self.assert_body(span, HeliosphereBaseHttpInstrumentor.HTTP_REQUEST_BODY_ATTRIBUTE_NAME, expected_body)

    def assert_response_body(self, span: ReadableSpan, expected_body: str):
        self.assert_body(span, HeliosphereBaseHttpInstrumentor.HTTP_RESPONSE_BODY_ATTRIBUTE_NAME, expected_body)
