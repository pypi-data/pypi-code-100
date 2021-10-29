import logging
import time
from typing import Optional, Iterable

from eventy.messaging.agent import Agent, Handler, Guarantee
from eventy.messaging.service import Service
from eventy.messaging.store import Cursor, Store
from eventy.record import Record, Response, RecordType
from eventy.trace_id.local import local_trace

__all__ = [
    'App',
]

logger = logging.getLogger(__name__)


class App:

    def __init__(
        self,
        store: Store,
        app_service: Service,
        ext_services: Iterable[Service] = None,
        agents: Iterable[Agent] = None,
        handlers: Iterable[Handler] = None,
        read_batch_size: int = 1,
        read_timeout_ms: Optional[int] = None,
        write_timeout_ms: Optional[int] = None,
        ack_timeout_ms: Optional[int] = None,
        commit_timeout_ms: Optional[int] = None,
    ):
        self._store = store
        self._app_service = app_service
        self._ext_services = ext_services or []
        self._all_handlers = list()
        if handlers is not None:
            for handler in handlers:
                self._all_handlers.append(handler)
        if agents is not None:
            for agent in agents:
                for handler in agent.handlers:
                    self._all_handlers.append(handler)

        self._read_batch_size = read_batch_size
        self._read_timeout_ms = read_timeout_ms
        self._write_timeout_ms = write_timeout_ms
        self._ack_timeout_ms = ack_timeout_ms
        self._commit_timeout_ms = commit_timeout_ms

    def _get_service_for_name(self, service_name: Optional[str]):
        if service_name is None:
            return self._app_service
        for service in self._ext_services:
            if service.name == service_name:
                return service
        raise ValueError(f"Service {service_name} not found.")

    def _get_topics_to_register(self) -> list[str]:
        topics: set[str] = set()
        topics.add(self._app_service.request_topic)
        for handler in self._all_handlers:
            logger.debug(f"Found handler {handler}.")
            service = self._get_service_for_name(handler.service_name)
            topics.add(service.topic_for(handler.record_type))
        return list(sorted(topics))

    def _get_handlers_for_record(self, record: Record, guarantee: Guarantee) -> list[Handler]:
        handlers: list[Handler] = list()
        for handler in self._all_handlers:
            if (
                handler.record_type == record.type
                and handler.record_name == record.name
                and handler.delivery_guarantee == guarantee
                and self._get_service_for_name(handler.service_name).namespace == record.namespace
            ):
                if isinstance(record, Response):
                    if record.destination == self._app_service.namespace:
                        handlers.append(handler)
                else:
                    handlers.append(handler)
        return handlers

    def _get_topic_for_record(self, record: Record) -> str:
        if record.type == RecordType.EVENT or record.type == RecordType.RESPONSE:
            return self._app_service.topic_for(record.type)
        for service in self._ext_services:
            if service.namespace == record.namespace:
                return service.topic_for(record.type)
        raise ValueError(f"No topic for record {record}.")

    def run(self) -> None:
        for topic in self._get_topics_to_register():
            logger.debug(f"Will register to topic: {topic}.")
            self._store.register_topic(topic, Cursor.ACKNOWLEDGED)

        while True:
            records = list(
                self._store.read(
                    max_count=self._read_batch_size,
                    timeout_ms=self._read_timeout_ms,
                    auto_ack=False,
                )
            )
            if records:
                logger.debug(f"Received {len(records)} new records.")
            else:
                time.sleep(0.05)
                continue

            # At Least Once
            for record in records:
                with local_trace(correlation_id=record.correlation_id):
                    for handler in self._get_handlers_for_record(record, Guarantee.AT_LEAST_ONCE):
                        for output_record in handler.handle_record(record):
                            self._store.write(
                                output_record,
                                self._get_topic_for_record(output_record),
                                self._write_timeout_ms,
                            )

            # Exactly Once
            self._store.start_transaction()
            self._store.ack(self._ack_timeout_ms)
            for record in records:
                with local_trace(correlation_id=record.correlation_id):
                    for handler in self._get_handlers_for_record(record, Guarantee.EXACTLY_ONCE):
                        for output_record in handler.handle_record(record):
                            self._store.write(
                                output_record,
                                self._get_topic_for_record(output_record),
                                self._write_timeout_ms,
                            )
            self._store.commit(self._commit_timeout_ms)

            # At Most Once
            for record in records:
                with local_trace(correlation_id=record.correlation_id):
                    for handler in self._get_handlers_for_record(record, Guarantee.AT_MOST_ONCE):
                        for output_record in handler.handle_record(record):
                            self._store.write(
                                output_record,
                                self._get_topic_for_record(output_record),
                                self._write_timeout_ms,
                            )
