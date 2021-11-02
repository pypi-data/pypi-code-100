from tests.instrumentation.base_http_instrumentor_test import BaseInstrumentorTest

from fakeredis import FakeStrictRedis as Redis


class TestHeliospherRedisInstrumentor(BaseInstrumentorTest):

    def test_instrument(self):
        key = "myTestKey"
        value = "myTestValue"
        set_statement = f"SET {key} {value}"
        get_statement = f"GET {key}"

        redis_client = Redis()
        redis_client.set(key, value)
        redis_client.get(key)

        self.tracer_provider.force_flush()
        spans = self.span_exporter.get_finished_spans()

        self.assertEqual(len(spans), 2)
        for span in spans:
            self.assertEqual(span.attributes.get("otel.library.name"), "opentelemetry.instrumentation.redis")
            expected_statement = set_statement if span.name == "SET" else get_statement
            self.assertEqual(span.attributes.get("db.statement"), expected_statement)

            # Todo (after merging  https://github.com/heliosphere-io/opentelemetry-python-contrib/pull/3)
            # if span.name == "GET":
            #     self.assertEqual(span.attributes.get(HeliospherRedisInstrumentor.RESPONSE_ATTRIBUTE_NAME), value)
