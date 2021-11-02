import os
import pkg_resources
import time
import traceback
from types import TracebackType
from typing import Union, Mapping, Any, Optional, Tuple

import thriftpy2
from opentracing import Reference, ReferenceType

from async_jaeger.constants import MAX_TRACEBACK_LENGTH, MAX_TAG_VALUE_LENGTH


SPEC_PATH = pkg_resources.resource_filename('async_jaeger', 'jaeger.thrift')
SPEC = thriftpy2.load(SPEC_PATH, 'jaeger_thrift')


MAX_SIGNED_ID = (1 << 63) - 1
MAX_UNSIGNED_ID = (1 << 64)

TagType = Union[bool, int, float, str, bytes]


def timestamp_to_microseconds(value: float) -> int:
    return int(value * 1000000)


def get_right_64_bits(value: int) -> int:
    return value & (MAX_UNSIGNED_ID - 1)


def get_left_64_bits(value: int) -> int:
    return (value >> 64) & (MAX_UNSIGNED_ID - 1)


def split_trace_id(value: int) -> Tuple[int, int]:
    return (
        (value >> 64) & (MAX_UNSIGNED_ID - 1),
        value & (MAX_UNSIGNED_ID - 1)
    )


def union_trace_id(left, right) -> int:
    return (
        (left << 64) + right
    )


def convert_unsigned_int_to_signed(value: int) -> int:
    # thrift defines ID fields as i64, which is signed,
    # therefore we convert large IDs (> 2^63) to negative longs
    if value > MAX_SIGNED_ID:
        value -= MAX_UNSIGNED_ID
    return value


def make_tag(
        key: str,
        value: TagType,
        max_length: int = MAX_TAG_VALUE_LENGTH,
        max_traceback_length: int = MAX_TRACEBACK_LENGTH
) -> SPEC.Tag:
    kwargs = {'key': key}

    if isinstance(value, bool):
        kwargs.update(vType=SPEC.TagType.BOOL, vBool=value)
    elif isinstance(value, int):
        kwargs.update(vType=SPEC.TagType.LONG, vLong=value)
    elif isinstance(value, float):
        kwargs.update(vType=SPEC.TagType.DOUBLE, vDouble=value)
    elif isinstance(value, bytes):
        kwargs.update(vType=SPEC.TagType.BINARY, vBinary=value)
    elif isinstance(value, TracebackType):
        value = ''.join(traceback.format_tb(value))
        kwargs.update(
            vType=SPEC.TagType.STRING,
            vStr=(
                value[:max_traceback_length]
                if len(value) > max_traceback_length else value
            )
        )
    elif isinstance(value, str):
        kwargs.update(
            vType=SPEC.TagType.STRING,
            vStr=value[:max_length] if len(value) > max_length else value
        )
    else:
        raise TypeError('Unsupported tag type')

    return SPEC.Tag(**kwargs)


def make_process(
        service_name: str,
        tags: Mapping[str, TagType],
        max_length: int = MAX_TAG_VALUE_LENGTH
) -> SPEC.Process:
    return SPEC.Process(
        serviceName=service_name,
        tags=[
            make_tag(key, value, max_length=max_length)
            for key, value in tags.items()
        ]
    )


def make_span_ref(reference: Reference) -> SPEC.SpanRef:
    if reference.type == ReferenceType.CHILD_OF:
        ref_type = SPEC.SpanRefType.CHILD_OF
    elif reference.type == ReferenceType.FOLLOWS_FROM:
        ref_type = SPEC.SpanRefType.FOLLOWS_FROM
    else:
        raise ValueError('Unknown reference type %r' % reference.type)

    return SPEC.SpanRef(
        refType=ref_type,
        traceIdLow=convert_unsigned_int_to_signed(get_right_64_bits(reference.referenced_context.trace_id)),
        traceIdHigh=convert_unsigned_int_to_signed(get_left_64_bits(reference.referenced_context.trace_id)),
        spanId=convert_unsigned_int_to_signed(reference.referenced_context.span_id),
    )


def make_log(
        fields: Mapping[str, Any],
        timestamp: Optional[float] = None,
        max_length: int = MAX_TAG_VALUE_LENGTH,
        max_traceback_length: int = MAX_TRACEBACK_LENGTH
) -> SPEC.Log:
    return SPEC.Log(
        timestamp=timestamp_to_microseconds(timestamp or time.time()),
        fields=[
            make_tag(key, value, max_length, max_traceback_length)
            for key, value in fields.items()
        ]
    )


def make_span(span) -> SPEC.Span:
    return SPEC.Span(
        traceIdLow=convert_unsigned_int_to_signed(get_right_64_bits(span.trace_id)),
        traceIdHigh=convert_unsigned_int_to_signed(get_left_64_bits(span.trace_id)),
        spanId=convert_unsigned_int_to_signed(span.span_id),
        parentSpanId=convert_unsigned_int_to_signed(span.parent_id) if span.parent_id else 0,
        operationName=span.operation_name,
        references=(
            [make_span_ref(ref) for ref in span.references]
            if span.references else []
        ),
        flags=span.flags,
        startTime=timestamp_to_microseconds(span.start_time),
        duration=timestamp_to_microseconds(span.end_time - span.start_time),
        tags=span.tags,
        logs=span.logs
    )


def make_batch(spans, process):
    return SPEC.Batch(
        spans=[make_span(span) for span in spans],
        process=process,
    )

