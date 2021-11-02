def encode_id(value: int, length: int, encoding: str = 'big') -> str:
    return value.to_bytes(length, encoding).hex()


def encode_trace_id(trace_id: int) -> str:
    if trace_id.bit_length() <= 64:
        return encode_id(trace_id, 8)
    return encode_id(trace_id, 16)


def decode_id(id_hex: str) -> int:
    return int.from_bytes(bytes.fromhex(id_hex), 'big')


def encode_span_id(span_id):
    return encode_id(span_id, 8)
