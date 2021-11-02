from fastapi import FastAPI, Response
from fastapi.testclient import TestClient

from tests.instrumentation.base_http_instrumentor_test import BaseHttpInstrumentorTest


class TestHeliosphereFastAPIInstrumentor(BaseHttpInstrumentorTest):

    ROUTE_PATTERN = '/test/{test_id}'

    def _create_fastapi_app(self):
        app = FastAPI()

        @app.post(self.ROUTE_PATTERN)
        async def test_endpoint(test_id: int):
            response = Response(f'Test ID: {test_id}')
            response.headers[self.RESPONSE_TEST_HEADER_KEY] = self.RESPONSE_TEST_HEADER_VALUE
            return response

        return app

    def test_instrument(self):
        test_id = 8

        app = self._create_fastapi_app()
        client = TestClient(app)

        headers = {self.REQUEST_TEST_HEADER_KEY: self.REQUEST_TEST_HEADER_VALUE}
        data = "Request Data!"
        client.post(f'/test/{test_id}', data=data, headers=headers)

        self.tracer_provider.force_flush()

        fastapi_span = None
        for span in self.span_exporter.get_finished_spans():
            if span.attributes.get("otel.library.name") == "heliosphere.instrumentation.fastapi":
                fastapi_span = span

        route = fastapi_span.attributes.get('http.route')
        self.assertEqual(route, self.ROUTE_PATTERN)

        self.assert_request_headers(fastapi_span)

        # Todo: uncomment after adding functionality for extracting the request body
        # self.assert_request_body(fastapi_span, data)

        self.assert_response_headers(fastapi_span)
        self.assert_response_body(fastapi_span, f'Test ID: {test_id}')
