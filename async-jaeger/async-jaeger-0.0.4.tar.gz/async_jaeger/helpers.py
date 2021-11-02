from contextlib import contextmanager
from typing import List, Optional, Union

from opentracing import Reference

from async_jaeger import Span, SpanContext


def encode_id(value: int, length: int, encoding = 'big') -> str:
    return value.to_bytes(length, encoding).hex()


def encode_trace_id(trace_id: int) -> str:
    if trace_id.bit_length() <= 64:
        return encode_id(trace_id, 8)
    return encode_id(trace_id, 16)


def decode_id(id_hex: str) -> int:
    return int.from_bytes(bytes.fromhex(id_hex), 'big')


def encode_span_id(span_id):
    return encode_id(span_id, 8)


def get_parent_tag_name(trace_id):
    return f'parent.{encode_trace_id(trace_id)}'


def get_parent_tag_value(span_id):
    return encode_span_id(span_id)


@contextmanager
def start_pipeline_span(
        tracer,
        operation_name=None,
        child_of: Union[Span, SpanContext] = None,
        references: Optional[List[Reference]] = None,
        tags=None,
        start_time=None,
        ignore_active_span=False
):
    with tracer.start_span(
            operation_name, child_of, references, tags, start_time,
            ignore_active_span
    ) as span:  # type: Span
        if references:
            for reference in references:
                span.set_tag(
                    get_parent_tag_name(reference.referenced_context.trace_id),
                    get_parent_tag_value(reference.referenced_context.span_id),
                )

        else:
            if child_of:
                span.set_tag(
                    get_parent_tag_name(span.context.trace_id),
                    get_parent_tag_value(span.context.parent_id),
                )

        yield span
