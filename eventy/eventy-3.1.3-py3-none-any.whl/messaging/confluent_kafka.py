import logging
import time
from concurrent.futures import Future
from threading import Thread
from time import sleep
from typing import Iterable, Optional

from confluent_kafka import Producer, Consumer, Message

from eventy.config import SERVICE_NAME
from eventy.messaging.errors import MessagingError
from eventy.messaging.store import Store, Cursor
from eventy.record import Record
from eventy.serialization import RecordSerializer
from eventy.serialization.errors import SerializationError

__all__ = [
    'CKStore',
]

logger = logging.getLogger(__name__)


class CKStore(Store):
    """
    Kafka implementation of a record store, using Confluent kafka library
    """

    transactional_producer: Producer
    immediate_producer: Producer
    consumer: Consumer
    poll_thread: Thread

    def __init__(
        self,
        serializer: RecordSerializer,
        bootstrap_servers: list[str],
        group_id: Optional[str] = None,
        transactional_id: Optional[str] = None,
        sasl_username: Optional[str] = None,
        sasl_password: Optional[str] = None,
    ) -> None:
        """
        Initialize the store

        :param serializer: Record serializer (read and write)
        :param bootstrap_servers: Kafka bootstrap servers (producer and consumer)
        :param group_id: Kafka group id (consumer)
        :param transactional_id: Kafka transactional id (producer)
        :param sasl_username: Optional username (if SASL PLAIN kafka connection, producer and consumer)
        :param sasl_password: Optional password (if SASL PLAIN kafka connection, producer and consumer)
        """
        # Initialize read_from services
        super().__init__()
        # Kafka config
        self.serializer = serializer
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id or SERVICE_NAME
        self.transactional_id = transactional_id or SERVICE_NAME
        self.sasl_username = sasl_username
        self.sasl_password = sasl_password
        # Other attributes
        self.initialized = False
        self.in_transaction = False
        self.cancelled = False

    def register_topic(self, topic: str, cursor: Cursor = Cursor.ACKNOWLEDGED):
        if cursor != Cursor.ACKNOWLEDGED:
            raise NotImplementedError(f"Only {Cursor.ACKNOWLEDGED} implemented for now.")
        super().register_topic(topic, cursor)
        logger.info(f"Registered topic {topic}: {cursor}.")

    def _check_initialized(self) -> None:
        if self.initialized:
            return

        logger.info(f"Initialize Kafka producer and consumer.")

        # configs
        transactional_producer_config = {
            'bootstrap.servers': ','.join(self.bootstrap_servers),
            'transactional.id': self.transactional_id,
            'enable.idempotence': 'true',
        }
        immediate_producer_config = {
            'bootstrap.servers': ','.join(self.bootstrap_servers),
            'enable.idempotence': 'true',
        }
        consumer_config = {
            'bootstrap.servers': ','.join(self.bootstrap_servers),
            'group.id': self.group_id,
            'enable.auto.commit': 'false',
            'auto.offset.reset': 'earliest',
            'isolation.level': 'read_committed',
        }

        # SASL authentication
        if self.sasl_username and self.sasl_password:
            for config in [
                transactional_producer_config,
                immediate_producer_config,
                consumer_config,
            ]:
                config.update(
                    {
                        'sasl_mechanism': 'PLAIN',
                        'sasl_plain_username': self.sasl_username,
                        'sasl_plain_password': self.sasl_password,
                    }
                )

        # producers
        self.transactional_producer = Producer(transactional_producer_config)
        self.transactional_producer.init_transactions()
        self.immediate_producer = Producer(immediate_producer_config)

        # consumer
        consumer_topics = [topic for topic in self.topics]
        self.consumer = Consumer(consumer_config)
        if consumer_topics:
            self.consumer.subscribe(consumer_topics)

        # poll loop
        def poll_loop():
            while not self.cancelled:
                self.immediate_producer.poll()
                self.immediate_producer.poll()
                sleep(0.001)
                # self.transactional_producer.poll(0.05)

        self.poll_thread = Thread(target=poll_loop)
        self.poll_thread.start()

        self.initialized = True

    def read(
        self,
        max_count: int = 1, timeout_ms: Optional[int] = None, auto_ack: bool = False
    ) -> Iterable[Record]:
        self._check_initialized()

        messages: list[Message] = self.consumer.consume(max_count, _ms2sec(timeout_ms))
        for message in messages:
            if message.error():
                logger.error(f"Could not read messages, cause: {message.error()}.")
            else:
                logger.debug(f"New message read {message.topic()}:{message.offset()}")
                # noinspection PyArgumentList
                # PyCharm is wrong, there is no payload arg
                encoded = message.value()
                try:
                    record = self.serializer.decode(encoded)
                    yield record
                    if auto_ack:
                        self.consumer.commit(message=message, asynchronous=False)
                except SerializationError as e:
                    logger.error(f"Could not read message, cause: {e}.")

    def ack(self, timeout_ms=None) -> None:
        self._check_initialized()

        if self.in_transaction:
            logger.info(f"Ack read messages in transaction.")
            self.transactional_producer.send_offsets_to_transaction(
                self.consumer.position(self.consumer.assignment()),
                self.consumer.consumer_group_metadata(),
                _ms2sec(timeout_ms)
            )
        else:
            logger.info(f"Ack read messages outside transaction.")
            self.consumer.commit(asynchronous=False)

    def _write(self, producer: Producer, record: Record, topic: str, timeout_ms=None) -> None:

        # handle callback
        future_result: Future = Future()

        def ack(err, msg):
            if err:
                logger.debug(f"Produced with errors: {err}.")
                future_result.set_exception(MessagingError(err))
            else:
                logger.debug(f"Produced successfully.")
                future_result.set_result(msg)

        # produce message
        producer.produce(
            topic=topic,
            value=self.serializer.encode(record),
            key=record.partition_key,
            on_delivery=ack
        )
        logger.debug(f"Will produce record {record} on {topic}.")

        # wait callback
        # TODO: timeout
        count = 0
        while not future_result.done():
            count = min(count + 1, 50)
            time.sleep(0.01 * count)

        # handle exceptions
        if exception := future_result.exception():
            raise exception

    def write(self, record: Record, topic: str, timeout_ms=None) -> None:
        self._check_initialized()

        if self.in_transaction:
            self._write(self.transactional_producer, record, topic, timeout_ms)
        else:
            self._write(self.immediate_producer, record, topic, timeout_ms)

    def write_now(self, record: Record, topic: str, timeout_ms=None) -> None:
        self._check_initialized()

        self._write(self.immediate_producer, record, topic, timeout_ms)

    def start_transaction(self) -> None:
        self._check_initialized()

        if self.in_transaction:
            raise MessagingError(f"Already in a transaction.")
        self.transactional_producer.begin_transaction()
        self.in_transaction = True

    def commit(self, timeout_ms: Optional[int] = None) -> None:
        self._check_initialized()

        if not self.in_transaction:
            raise MessagingError(f"Not in a transaction.")
        self.transactional_producer.commit_transaction(_ms2sec(timeout_ms))
        self.in_transaction = False

    def abort(self, timeout_ms: Optional[int] = None) -> None:
        self._check_initialized()

        if not self.in_transaction:
            raise MessagingError(f"Not in a transaction.")
        self.transactional_producer.abort_transaction(_ms2sec(timeout_ms))
        self.in_transaction = False

    def __del__(self):
        if self.initialized:
            logger.debug(f"Waiting poll thread to join.")
            self.cancelled = True
            self.poll_thread.join()
            logger.debug(f"Poll thread joined.")


def _ms2sec(timeout_ms: Optional[int]) -> float:
    timeout_sec = -1.0
    if timeout_ms:
        timeout_sec = timeout_ms / 1000
    return timeout_sec
