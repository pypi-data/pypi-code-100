import urllib3
import httpretty

from tests.instrumentation.base_http_instrumentor_test import BaseHttpInstrumentorTest


TEST_URL = 'http://test.com'
MOCKED_RESPONSE_BODY = 'A Mocked Response'


class TestHeliosphereUrllib3Instrumentor(BaseHttpInstrumentorTest):

    @httpretty.activate
    def test_instrument(self):
        headers = {self.RESPONSE_TEST_HEADER_KEY: self.RESPONSE_TEST_HEADER_VALUE}
        httpretty.register_uri(httpretty.POST, TEST_URL, body=MOCKED_RESPONSE_BODY, **headers)

        request_body = {'param1': 'hello', 'param2': 'world'}
        http = urllib3.PoolManager()
        http.request("POST", TEST_URL, headers={self.REQUEST_TEST_HEADER_KEY: self.REQUEST_TEST_HEADER_VALUE},
                     body=str(request_body))

        self.tracer_provider.force_flush()

        urllib3_span = None
        for span in self.span_exporter.get_finished_spans():
            name = span.attributes['otel.library.name']
            if name == 'opentelemetry.instrumentation.urllib3':
                urllib3_span = span

        self.assertIsNotNone(urllib3_span)

        self.assert_response_headers(urllib3_span)
        self.assert_response_body(urllib3_span, MOCKED_RESPONSE_BODY)

        # Todo: add these assertions after updating the request_hook function in Urllib3 instrumentor
        # self.assert_request_headers(urllib3_span)
        # self.assert_request_body(urllib3_span, str(request_body))
