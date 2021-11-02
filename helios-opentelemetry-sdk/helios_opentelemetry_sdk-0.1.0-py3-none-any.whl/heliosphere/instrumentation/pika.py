from opentelemetry.trace import Span

from heliosphere.instrumentation.base import HeliosphereBaseInstrumentor


class HeliospherePikaInstrumentor(HeliosphereBaseInstrumentor):

    MODULE_NAME = 'opentelemetry.instrumentation.pika'
    INSTRUMENTOR_NAME = 'PikaInstrumentor'

    def __init__(self):
        super().__init__(self.MODULE_NAME, self.INSTRUMENTOR_NAME)

    def instrument(self, tracer_provider=None):
        if self.get_instrumentor() is None:
            return

        self.get_instrumentor().instrument(tracer_provider=tracer_provider,
                                           publish_hook=self.publish_hook,
                                           consume_hook=self.consume_hook)

    @staticmethod
    def publish_hook(span: Span, body: bytes, properties):
        if span and span.is_recording():
            span.set_attribute("messaging.payload", body.decode())

    @staticmethod
    def consume_hook(span: Span, body: bytes, properties):
        if span and span.is_recording():
            span.set_attribute("messaging.payload", body.decode())
