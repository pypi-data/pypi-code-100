import flask

from heliosphere.instrumentation import HeliosphereFlaskInstrumentor
from tests.instrumentation.base_http_instrumentor_test import BaseHttpInstrumentorTest


class TestHeliosphereFlaskInstrumentor(BaseHttpInstrumentorTest):

    ROUTE_PATTERN = '/test/<test_id>'

    def _get_client(self):
        app = flask.Flask(__name__)

        @app.route(self.ROUTE_PATTERN, methods=["GET", "POST"])
        def endpoint(test_id: int):
            response = flask.Response(f'Test ID: {test_id}')
            response.headers[self.RESPONSE_TEST_HEADER_KEY] = self.RESPONSE_TEST_HEADER_VALUE
            return response

        return app.test_client()

    def test_instrument(self):
        test_id = 7

        headers = {self.REQUEST_TEST_HEADER_KEY: self.REQUEST_TEST_HEADER_VALUE}
        body = "This is the request body"
        client = self._get_client()
        response = client.post(f'/test/{test_id}', data=body, headers=headers)

        # make sure we remove the extra header added in the instrumentation hooks
        self.assertFalse(HeliosphereFlaskInstrumentor.RESPONSE_BODY_HEADER_NAME in response.headers)

        self.tracer_provider.force_flush()

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(len(spans), 1)

        flask_span = spans[0]
        self.assertEqual(flask_span.attributes.get('otel.library.name'), 'opentelemetry.instrumentation.flask')

        route = flask_span.attributes.get('http.route', None)
        self.assertEqual(route, self.ROUTE_PATTERN)

        self.assert_request_headers(flask_span)
        self.assert_request_body(flask_span, body)

        self.assert_response_headers(flask_span)
        self.assert_response_body(flask_span, f'Test ID: {test_id}')
