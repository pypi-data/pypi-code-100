from unittest import TestCase

from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from heliosphere import initialize, HeliosphereConfig


class BaseInstrumentorTest(TestCase):

    def setUp(self):
        self.span_exporter = InMemorySpanExporter()

        config = HeliosphereConfig(
            api_token='dummy_token',
            service_name='dummy_service',
            collector_endpoint='http://localhost:4317',
            sampling_ratio=1
        )
        setattr(config, 'span_exporter', self.span_exporter)

        self.hs = initialize(config)
        self.tracer_provider = self.hs.get_tracer_provider()

    def tearDown(self) -> None:
        self.hs.uninstrument()
