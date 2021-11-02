from logging import getLogger

from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
from tests.instrumentation.base import BaseInstrumentorTest

_LOG = getLogger(__name__)


class TestHeliospherKafkaInstrumentor(BaseInstrumentorTest):
    """
    For running these tests we need to have a kafka server running locally (see `self.bootstrap_servers`)
     with a topic named as defined in `self.topic`
    """

    def setUp(self):
        super().setUp()
        self.topic = "test"
        self.bootstrap_servers = ['localhost:9093']
        self.admin = KafkaAdminClient(bootstrap_servers=self.bootstrap_servers, client_id="admin")

        if self.topic not in self.admin.list_topics():
            self.admin.create_topics(new_topics=[NewTopic(name=self.topic, num_partitions=1, replication_factor=1)])

    def tearDown(self) -> None:
        self.admin.delete_topics([self.topic])
        super().tearDown()

    def test_instrument(self):
        try:
            producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)
            consumer = KafkaConsumer(self.topic, group_id='my-group',
                                     bootstrap_servers=self.bootstrap_servers, auto_offset_reset='earliest')
        except Exception:
            self.fail(f"No bootstrap servers were found on {self.bootstrap_servers}. please run a kafka container")

        producer.send(self.topic, b'this is a test message')

        # Consume a record and open a span within the consumer context
        for message in consumer:
            tracer = self.tracer_provider.get_tracer(__name__)
            with tracer.start_as_current_span("my-app") as span:
                span.set_attribute("key", "value")
            consumer.commit()
            # we are only consuming a single message, we break the loop here so the consumer won't wait for new messages
            break

        producer.close()
        consumer.close()
        self.tracer_provider.force_flush()
        spans = self.span_exporter.get_finished_spans()

        self.assertEqual(3, len(spans))
        producer_span = spans[0]
        internal_span = spans[1]
        consumer_span = spans[2]

        self.assertEqual(producer_span.context.trace_id, consumer_span.context.trace_id)
        self.assertEqual(consumer_span.context.trace_id, internal_span.context.trace_id)
        self.assertEqual(producer_span.context.span_id, consumer_span.parent.span_id)
        self.assertEqual(consumer_span.context.span_id, internal_span.parent.span_id)
