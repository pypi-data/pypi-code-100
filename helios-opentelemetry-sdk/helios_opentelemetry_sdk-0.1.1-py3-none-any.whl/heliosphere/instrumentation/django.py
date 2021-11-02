import importlib
from logging import getLogger

from opentelemetry.trace import Span

from heliosphere.instrumentation.base_http_instrumentor import HeliosphereBaseHttpInstrumentor

_LOG = getLogger(__name__)


class HeliosphereDjangoInstrumentor(HeliosphereBaseHttpInstrumentor):

    MODULE_NAME = 'opentelemetry.instrumentation.django'
    INSTRUMENTOR_NAME = 'DjangoInstrumentor'

    def __init__(self):
        super().__init__(self.MODULE_NAME, self.INSTRUMENTOR_NAME)
        if self.get_instrumentor() is not None:
            try:
                django_mod = importlib.import_module('django.conf')
                django_settings = getattr(django_mod, 'settings', None)
                if django_settings is not None:
                    django_settings.configure()
            except Exception as err:
                _LOG.warning(err)

    def instrument(self, tracer_provider=None):
        if self.get_instrumentor() is None:
            return

        self.get_instrumentor().instrument(tracer_provider=tracer_provider, response_hook=self.response_hook)

    @staticmethod
    def response_hook(span: Span, request, response) -> None:
        """
        :param span: an object of type
        :param request: an object of type requests.HttpRequest
        :param response: an object of type requests.HttpResponse
        """
        HeliosphereDjangoInstrumentor.base_request_hook(span, request.headers, request.body)
        HeliosphereDjangoInstrumentor.base_response_hook(span, response.headers, response.content)
