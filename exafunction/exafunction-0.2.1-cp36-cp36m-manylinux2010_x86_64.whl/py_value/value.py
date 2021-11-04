# Copyright Exafunction, Inc.

import numpy as np
from enum import IntEnum

import exa._C as _C
from exa.common_pb.common_pb2 import ValueMetadata, TensorMetadata, DataType

class ValueCompressionType(IntEnum):
    UNCOMPRESSED = 0
    FLOAT_TO_UINT8_COMPRESSION = 1
    LZ4_COMPRESSION = 2

class Value:
    def __init__(self, c: _C.Value):
        self._c = c

    def _check_valid(self):
        if not self._c.is_valid():
            raise ValueError("Value is not valid (was the session closed?)")

    def clear(self):
        self._c = None

    def value_id(self) -> int:
        self._check_valid()
        return self._c.value_id()

    def bytes(self) -> bytes:
        self._check_valid()
        return bytes(self._c)

    def set_bytes(self, other: bytes):
        self._check_valid()
        self.mutable_bytes_view()[:] = np.frombuffer(other, dtype=np.uint8)

    # Return a view into the underlying value buffer.
    def bytes_view(self) -> np.ndarray:
        self._check_valid()
        ret = self.mutable_bytes_view()
        ret.setflags(write=False)
        return ret

    # Return a mutable view into the underlying value buffer.
    def mutable_bytes_view(self) -> np.ndarray:
        self._check_valid()
        ret = np.frombuffer(self._c, dtype=np.uint8)
        return ret

    def is_gpu(self) -> bool:
        self._check_valid()
        return self._c.is_gpu()

    def is_local_valid(self) -> bool:
        self._check_valid()
        return self._c.is_local_valid()

    def is_mutable(self) -> bool:
        self._check_valid()
        return self._c.is_mutable()

    def is_client_value(self) -> bool:
        self._check_valid()
        return self._c.is_client_value()

    def is_method_value(self) -> bool:
        self._check_valid()
        return self._c.is_method_value()

    def metadata(self) -> ValueMetadata:
        self._check_valid()
        m = ValueMetadata()
        m.ParseFromString(self._c.metadata())
        return m

    def set_metadata(self, v: ValueMetadata) -> None:
        self._check_valid()
        self._c.set_metadata(v.SerializeToString())

    def is_tensor(self) -> bool:
        self._check_valid()
        return self._c.is_tensor()

    NP_TO_PB_DTYPE = {
        np.dtype(np.float32) : DataType.FLOAT32,
        np.dtype(np.float64) : DataType.FLOAT64,
        np.dtype(np.int8) : DataType.INT8,
        np.dtype(np.int16) : DataType.INT16,
        np.dtype(np.int32) : DataType.INT32,
        np.dtype(np.int64) : DataType.INT64,
        np.dtype(np.uint8) : DataType.UINT8,
        np.dtype(np.uint16) : DataType.UINT16,
        np.dtype(np.uint32) : DataType.UINT32,
        np.dtype(np.uint64) : DataType.UINT64,
    }

    PB_TO_NP_DTYPE = {v: k for k, v in NP_TO_PB_DTYPE.items()}

    @classmethod
    def _get_tensor_metadata(cls, dtype, shape, strides = None):
        m = ValueMetadata()
        m.size = np.prod(shape) * np.dtype(dtype).itemsize
        dtype = np.dtype(dtype)
        if dtype not in cls.NP_TO_PB_DTYPE:
            raise ValueError(f"invalid dtype {dtype}")
        m.tensor.dtype = cls.NP_TO_PB_DTYPE[dtype]
        if len(shape) == 0:
            raise ValueError("tensor must have at least 1 dimension")
        if any(s < 0 for s in shape):
            raise ValueError("tensor may not have negative sizes")
        m.tensor.shape.extend(shape)

        if strides is None:
            strides = [0] * len(shape)
            strides[-1] = dtype.itemsize
            for i in range(len(strides) - 1, 0, -1):
                strides[i - 1] = strides[i] * shape[i]
        m.tensor.strides.extend(strides)
        return m

    def numpy(self):
        self._check_valid()
        m = self.metadata()
        if not m.HasField("tensor"):
            raise TypeError("Value is not a tensor, cannot convert to numpy")
        dtype = self.PB_TO_NP_DTYPE[m.tensor.dtype]
        buf = np.frombuffer(self._c, dtype=dtype)
        return np.lib.stride_tricks.as_strided(
            buf, shape = m.tensor.shape, strides = m.tensor.strides)

    def set_compression_type(self, compression_type: ValueCompressionType):
        if not isinstance(compression_type, ValueCompressionType):
            raise TypeError("compression_type must be of type ValueCompressionType")
        self._c.set_compression_type(int(compression_type))
