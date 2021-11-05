import base64
import json
import zlib


def encode(origin):
    compressed = zlib.compress(json.dumps(origin).encode())

    return base64.b64encode(compressed)[:: -1].decode()


def decode(origin):
    decompressed = base64.b64decode(origin[:: -1])

    return json.loads(zlib.decompress(decompressed))
