from django.http import HttpResponse, HttpRequest
from django.test.utils import override_settings, setup_test_environment
from django.urls import path
from django.test.client import Client
from django.views.decorators.http import require_http_methods

from tests.instrumentation.base_http_instrumentor_test import BaseHttpInstrumentorTest


RESPONSE_TEST_HEADER_KEY = 'response-test-header'
RESPONSE_TEST_HEADER_VALUE = 'response_test_header'

ROUTE_PATTERN = '<int:test_id>/'


# Basic Django view for testing
@require_http_methods(['GET', 'POST'])
def index(request: HttpRequest, test_id: int = 0):
    response = HttpResponse(f'Test ID: {test_id}')
    response[RESPONSE_TEST_HEADER_KEY] = RESPONSE_TEST_HEADER_VALUE
    return response


urlpatterns = [
    path('', index),
    path(ROUTE_PATTERN, index)
]


class TestHeliosphereDjangoInstrumentor(BaseHttpInstrumentorTest):

    def setUp(self):
        super().setUp()
        setup_test_environment()

    @override_settings(ROOT_URLCONF=__name__)
    def test_instrument(self):
        test_id = 5

        # Must add 'HTTP_' prefix to the header, otherwise django ignores it
        # (https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.META)
        headers = {f'HTTP_{self.REQUEST_TEST_HEADER_KEY}': self.REQUEST_TEST_HEADER_VALUE}
        request_body = {'param1': 1, 'param2': 2}
        client = Client()
        client.post(f'/{test_id}/', data=request_body, content_type='text/html; charset=UTF-8', **headers)

        self.tracer_provider.force_flush()
        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(len(spans), 1)

        django_span = spans[0]
        self.assertEqual(django_span.attributes.get('otel.library.name'), 'opentelemetry.instrumentation.django')

        route = django_span.attributes.get('http.route', None)
        self.assertEqual(route, ROUTE_PATTERN)

        self.assert_request_headers(django_span)
        self.assert_request_body(django_span, str(request_body))

        self.assert_response_headers(django_span)
        self.assert_response_body(django_span, f'Test ID: {test_id}')
