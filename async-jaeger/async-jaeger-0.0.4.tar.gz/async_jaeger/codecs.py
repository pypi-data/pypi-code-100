import struct
import urllib.parse
from abc import ABC, abstractmethod

from opentracing import (
    InvalidCarrierException,
    SpanContextCorruptedException,
)

from async_jaeger.constants import (
    BAGGAGE_HEADER_KEY,
    BAGGAGE_HEADER_PREFIX,
    DEBUG_ID_HEADER_KEY,
    TRACE_ID_HEADER
)
from async_jaeger.span_context import SpanContext


class BaseCodec(ABC):
    @abstractmethod
    def inject(self, span_context, carrier):
        pass

    @abstractmethod
    def extract(self, carrier):
        pass


class TextCodec(BaseCodec):
    def __init__(
            self,
            url_encoding=False,
            trace_id_header=TRACE_ID_HEADER,
            baggage_header_prefix=BAGGAGE_HEADER_PREFIX,
            debug_id_header=DEBUG_ID_HEADER_KEY,
            baggage_header=BAGGAGE_HEADER_KEY
    ):
        self.url_encoding = url_encoding
        self.trace_id_header = trace_id_header.lower().replace('_', '-')
        self.baggage_prefix = baggage_header_prefix.lower().replace('_', '-')
        self.debug_id_header = debug_id_header.lower().replace('_', '-')
        self.baggage_header = baggage_header
        self.prefix_length = len(baggage_header_prefix)

    def inject(self, span_context, carrier):
        if not isinstance(carrier, dict):
            raise InvalidCarrierException('carrier not a collection')
        # Note: we do not url-encode the trace ID because the ':' separator
        # is not a problem for HTTP header values
        carrier[self.trace_id_header] = span_context_to_string(
            trace_id=span_context.trace_id, span_id=span_context.span_id,
            parent_id=span_context.parent_id, flags=span_context.flags)
        baggage = span_context.baggage
        if baggage:
            for key, value in baggage.items():
                encoded_key = key
                if isinstance(key, (bytes,)):
                    encoded_key = str(key, 'utf-8')
                if self.url_encoding:
                    encoded_value = urllib.parse.quote(value)
                else:
                    if isinstance(key, (bytes,)):
                        encoded_value = str(value, 'utf-8')
                    else:
                        encoded_value = value
                # Leave the below print(), you will thank me next time you
                # debug unicode strings
                # print('adding baggage', key, '=>', value, 'as', encoded_key,
                # '=>', encoded_value)
                header_key = '%s%s' % (self.baggage_prefix, encoded_key)
                carrier[header_key] = encoded_value

    def extract(self, carrier):
        if not hasattr(carrier, 'items'):
            raise InvalidCarrierException('carrier not a collection')
        trace_id, span_id, parent_id, flags = None, None, None, None
        baggage = None
        debug_id = None
        for key, value in carrier.items():
            uc_key = key.lower()
            if uc_key == self.trace_id_header:
                if self.url_encoding:
                    value = urllib.parse.unquote(value)
                trace_id, span_id, parent_id, flags = \
                    span_context_from_string(value)
            elif uc_key.startswith(self.baggage_prefix):
                if self.url_encoding:
                    value = urllib.parse.unquote(value)
                attr_key = key[self.prefix_length:]
                if baggage is None:
                    baggage = {attr_key.lower(): value}
                else:
                    baggage[attr_key.lower()] = value
            elif uc_key == self.debug_id_header:
                if self.url_encoding:
                    value = urllib.parse.unquote(value)
                debug_id = value
            elif uc_key == self.baggage_header:
                if self.url_encoding:
                    value = urllib.parse.unquote(value)
                baggage = self._parse_baggage_header(value, baggage)
        if not trace_id or not span_id:
            # reset all IDs
            trace_id, span_id, parent_id, flags = None, None, None, None
        if not trace_id and not debug_id and not baggage:
            return None
        return SpanContext(trace_id=trace_id, span_id=span_id,
                           parent_id=parent_id, flags=flags,
                           baggage=baggage, debug_id=debug_id)

    def _parse_baggage_header(self, header, baggage):
        for part in header.split(','):
            kv = part.strip().split('=')
            if len(kv) == 2:
                if not baggage:
                    baggage = {}
                baggage[kv[0]] = kv[1]
        return baggage


class BinaryCodec(BaseCodec):
    """
    Implements inject/extract of SpanContext to/from binary that compatible
    with golang implementation
    https://github.com/jaegertracing/jaeger-client-go/blob/master/propagation.go#L177-L290
    Supports propagation of trace_id, span_id, flags and baggage
    """
    def inject(self, span_context, carrier):
        if not isinstance(carrier, bytearray):
            raise InvalidCarrierException('carrier not a bytearray')
        # check if we have 128 bit trace_id, break it into two 64 units
        max_int64 = 0xFFFFFFFFFFFFFFFF
        if span_context.trace_id > max_int64:
            high = (span_context.trace_id >> 64) & max_int64
            low = span_context.trace_id & max_int64
        else:
            high = 0
            low = span_context.trace_id
        carrier += struct.pack('>QQQQBI', high, low, span_context.span_id or 0,
                               span_context.parent_id or 0, span_context.flags,
                               len(span_context.baggage))

        for k, v in span_context.baggage.items():
            carrier += self._pack_baggage_item(k, v)

    def extract(self, carrier):
        if not isinstance(carrier, bytearray):
            raise InvalidCarrierException('carrier not a bytearray')
        baggage = {}
        (
            high_trace_id, low_trace_id, span_id, parent_id, flags,
            baggage_count
        ) = struct.unpack('>QQQQBI', carrier[:37])
        # if high_trace_id isn't 0, then we are dealing with 128bit trace id
        # integer, therefore unpack into 1 number
        if high_trace_id:
            trace_id = (high_trace_id << 64) | low_trace_id
        else:
            trace_id = low_trace_id

        if baggage_count != 0:
            baggage_data = carrier[37:]
            for _ in range(baggage_count):
                key, value, bytes_read = self._unpack_baggage_item(
                    baggage_data
                )
                baggage[key] = value
                baggage_data = baggage_data[bytes_read:]

        return SpanContext(trace_id=trace_id, span_id=span_id,
                           parent_id=parent_id, flags=flags, baggage=baggage)

    def _pack_baggage_item(self, key, value):
        baggage = bytearray()
        if not isinstance(key, bytes):
            key = key.encode('utf-8')
        baggage += struct.pack('>I', len(key))
        baggage += key

        if not isinstance(value, bytes):
            value = value.encode('utf-8')
        baggage += struct.pack('>I', len(value))
        baggage += value
        return baggage

    def _unpack_baggage_item(self, baggage):
        bytes_read = 0
        key, b_read = self._read_kv(baggage)
        bytes_read += b_read
        value, b_read = self._read_kv(baggage[bytes_read:])
        bytes_read += b_read
        return key, value, bytes_read

    def _read_kv(self, data):
        data_len = struct.unpack('>i', data[:4])[0]
        data_value = struct.unpack('>' + 'c' * data_len, data[4:4 + data_len])
        bytes_read = 4 + data_len
        return b''.join(data_value).decode('utf-8'), bytes_read


def span_context_to_string(trace_id, span_id, parent_id, flags):
    """
    Serialize span ID to a string
        {trace_id}:{span_id}:{parent_id}:{flags}

    Numbers are encoded as variable-length lower-case hex strings.
    If parent_id is None, it is written as 0.

    :param trace_id:
    :param span_id:
    :param parent_id:
    :param flags:
    """
    parent_id = parent_id or 0
    return '{:x}:{:x}:{:x}:{:x}'.format(trace_id, span_id, parent_id, flags)


def span_context_from_string(value):
    """
    Decode span ID from a string into a TraceContext.
    Returns None if the string value is malformed.

    :param value: formatted {trace_id}:{span_id}:{parent_id}:{flags}
    """
    if type(value) is list and len(value) > 0:
        # sometimes headers are presented as arrays of values
        if len(value) > 1:
            raise SpanContextCorruptedException(
                'trace context must be a string or array of 1: "%s"' % value)
        value = value[0]
    if not isinstance(value, (str,)):
        raise SpanContextCorruptedException(
            'trace context not a string "%s"' % value)
    parts = value.split(':')
    if len(parts) != 4:
        raise SpanContextCorruptedException(
            'malformed trace context "%s"' % value)
    try:
        trace_id = int(parts[0], 16)
        span_id = int(parts[1], 16)
        parent_id = int(parts[2], 16)
        flags = int(parts[3], 16)
        if trace_id < 1 or span_id < 1 or parent_id < 0 or flags < 0:
            raise SpanContextCorruptedException(
                'malformed trace context "%s"' % value)
        if parent_id == 0:
            parent_id = None
        return trace_id, span_id, parent_id, flags
    except ValueError as e:
        raise SpanContextCorruptedException(
            'malformed trace context "%s": %s' % (value, e))


def header_to_hex(header):
    if not isinstance(header, (str,)):
        raise SpanContextCorruptedException(
            'malformed trace context "%s", expected hex string' % header)

    try:
        return int(header, 16)
    except ValueError:
        raise SpanContextCorruptedException(
            'malformed trace context "%s", expected hex string' % header)
