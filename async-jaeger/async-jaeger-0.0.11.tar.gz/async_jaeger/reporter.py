import asyncio
import logging
from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Any, Optional, Mapping, List

import aiohttp
from aiohttp import ClientSession, hdrs
from thriftpy2.utils import serialize

from async_jaeger import thrift
from async_jaeger.constants import DEFAULT_FLUSH_INTERVAL, MAX_TAG_VALUE_LENGTH
from async_jaeger.metrics import MetricsFactory, Metrics, LegacyMetricsFactory
from async_jaeger.span import Span
from async_jaeger.thrift import TagType
from async_jaeger.utils import ErrorReporter


default_logger = logging.getLogger(__name__)


class BaseReporter(ABC):
    """Abstract class."""
    def set_process(
            self,
            service_name: str,
            tags: Mapping[str, TagType],
            max_length: int = MAX_TAG_VALUE_LENGTH
    ):
        pass

    @abstractmethod
    def report_span(self, span: Span):
        pass

    async def close(self):
        pass


class NullReporter(BaseReporter):
    """Ignores all spans."""
    def report_span(self, span: Span):
        pass


class InMemoryReporter(BaseReporter):
    """Stores spans in memory and returns them via get_spans()."""
    def __init__(self):
        super().__init__()
        self.spans: List[Span] = []

    def report_span(self, span: Span):
        self.spans.append(span)

    def get_spans(self) -> List[Span]:
        return self.spans[:]


class LoggingReporter(NullReporter):
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger if logger else default_logger

    def report_span(self, span: Span):
        self.logger.info('Reporting span %s', span)


class HttpReporter(NullReporter):
    """Receives completed spans from Tracer and submits them via HTTP."""
    def __init__(
        self,
        url: str = 'http://127.0.0.1:14268/api/traces',
        session: ClientSession = None,
        queue_capacity: int = 100,
        batch_size: int = 10,
        flush_interval: Optional[float] = DEFAULT_FLUSH_INTERVAL,
        error_reporter: Optional[ErrorReporter] = None,
        metrics: Optional[Metrics] = None,
        metrics_factory: Optional[MetricsFactory] = None,
        **kwargs: Any
    ):
        self.url = url
        self.logger = kwargs.get('logger', default_logger)
        self.queue = asyncio.Queue(maxsize=queue_capacity)
        self.batch_size = batch_size
        self.flush_interval = flush_interval or None
        self.stop = object()
        self.stopped = False
        self._process = None

        if session:
            self.session = session
            self._close_session = False
        else:
            self.session = ClientSession()
            self._close_session = True

        self.metrics_factory = metrics_factory or LegacyMetricsFactory(
            metrics or Metrics()
        )
        self.metrics = ReporterMetrics(self.metrics_factory)
        self.error_reporter = error_reporter or ErrorReporter(Metrics())
        self.task = asyncio.create_task(self._consume_queue())

    def set_process(
            self,
            service_name: str,
            tags: Mapping[str, TagType],
            max_length: int = MAX_TAG_VALUE_LENGTH
    ):
        self._process = thrift.make_process(
            service_name=service_name, tags=tags, max_length=max_length
        )

    def report_span(self, span: Span):
        try:
            if self.stopped:
                self.metrics.reporter_dropped(1)
            else:
                self.queue.put_nowait(span)
        except asyncio.queues.QueueFull:
            self.metrics.reporter_dropped(1)

    async def _consume_queue(self):
        spans = []
        stopped = False
        while not stopped:
            while len(spans) < self.batch_size:
                try:
                    # using timeout allows periodic flush with smaller packet
                    timeout = (
                        self.flush_interval
                        if self.flush_interval and spans
                        else None
                    )
                    span = await asyncio.wait_for(
                        self.queue.get(), timeout=timeout
                    )
                except asyncio.TimeoutError:
                    break
                else:
                    if span == self.stop:
                        stopped = True
                        self.queue.task_done()
                        # don't return yet, submit accumulated spans first
                        break
                    else:
                        spans.append(span)
            if spans:
                await self._submit(spans)
                for _ in spans:
                    self.queue.task_done()
                spans = spans[:0]
            self.metrics.reporter_queue_length(self.queue.qsize())
        self.logger.info('Span publisher exited')

    async def _submit(self, spans):
        try:
            batch = thrift.make_batch(spans=spans, process=self._process)
            serialized_batch = serialize(batch)
            async with self.session.post(
                    self.url,
                    data=serialized_batch,
                    headers={hdrs.CONTENT_TYPE: 'application/x-thrift'}
            ) as resp:
                if resp.status != HTTPStatus.ACCEPTED:
                    raise aiohttp.ClientResponseError(
                        resp.request_info, resp.history, code=resp.status
                    )
            self.logger.debug('sent %r spans', len(spans))
            self.metrics.reporter_success(len(spans))
        except Exception as e:
            self.metrics.reporter_failure(len(spans))
            self.error_reporter.error(
                'Failed to submit traces to jaeger-collector: %s', e
            )

    async def close(self):
        self.stopped = True
        await self.queue.put(self.stop)
        await self.queue.join()
        if self._close_session:
            await self.session.close()


class ReporterMetrics(object):
    """Reporter specific metrics."""
    def __init__(self, metrics_factory: MetricsFactory):
        self.reporter_success = metrics_factory.create_counter(
            name='jaeger:reporter_spans', tags={'result': 'ok'}
        )
        self.reporter_failure = metrics_factory.create_counter(
            name='jaeger:reporter_spans', tags={'result': 'err'}
        )
        self.reporter_dropped = metrics_factory.create_counter(
            name='jaeger:reporter_spans', tags={'result': 'dropped'}
        )
        self.reporter_queue_length = metrics_factory.create_gauge(
            name='jaeger:reporter_queue_length'
        )


class CompositeReporter(BaseReporter):
    """Delegates reporting to one or more underlying reporters."""
    def __init__(self, *reporters: BaseReporter):
        self.reporters = reporters

    def set_process(
            self,
            service_name: str,
            tags: Mapping[str, TagType],
            max_length: int = MAX_TAG_VALUE_LENGTH
    ):
        for reporter in self.reporters:
            reporter.set_process(service_name, tags)

    def report_span(self, span: Span):
        for reporter in self.reporters:
            reporter.report_span(span)

    async def close(self):
        await asyncio.gather(*(
            reporter.close() for reporter in self.reporters
        ))
