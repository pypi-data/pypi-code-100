# Copyright Exafunction, Inc.

from dataclasses import dataclass
from typing import Dict, List, Optional
import inspect
import sys
import numpy as np

from exa.common_pb.common_pb2 import ValueMetadata
from exa.py_client.module import Module
from exa.py_client.profiler import Profiler
from exa.py_value import Value, ValueCompressionType
import exa._C as _C

@dataclass
class ModuleContextSpec:
    module_tag: Optional[str] = None
    module_hash: Optional[str] = None
    cpu_memory_limit_mb: int = 0
    gpu_memory_limit_mb: int = 0
    ignore_exec_serialize: bool = False

@dataclass
class PlacementGroupSpec:
    module_contexts: List[ModuleContextSpec]
    value_pool_size: int = 100 * 1024 * 1024
    runner_fraction: float = 0.1

# Hack to override inspect.getfile to work in IPython
def new_getfile(object, _old_getfile=inspect.getfile):
    if not inspect.isclass(object):
        return _old_getfile(object)

    # Lookup by parent module (as in current inspect)
    if hasattr(object, '__module__'):
        object_ = sys.modules.get(object.__module__)
        if hasattr(object_, '__file__'):
            return object_.__file__

    # If parent module is __main__, lookup by methods (NEW)
    for name, member in inspect.getmembers(object):
        if inspect.isfunction(member) and object.__qualname__ + '.' + member.__name__ == member.__qualname__:
            return inspect.getfile(member)
    else:
        raise TypeError('Source for {!r} not found'.format(object))

inspect.getfile = new_getfile

class Session:
    def __init__(self,
        scheduler_address: str,
        external_scheduler: bool = False,
        placement_groups = {},
        disable_fault_tolerance = False,
        profile_log_file_path = "",
        local_pool_size = 2 * 1024 * 1024 * 1024,
        default_compression_type = ValueCompressionType.UNCOMPRESSED,
    ):
        if not isinstance(default_compression_type, ValueCompressionType):
            raise TypeError("default_compression_type must be of type ValueCompressionType")
        self._c = _C.Session(
            scheduler_address,
            external_scheduler,
            placement_groups,
            disable_fault_tolerance,
            profile_log_file_path,
            local_pool_size,
            int(default_compression_type),
        )

    def close(self):
        self._c = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def _check_closed(self):
        if self._c is None:
            raise ValueError("Session is closed")

    def session_id(self) -> int:
        self._check_closed()
        return self._c.session_id()

    def new_module(self, module_tag: str, config: Dict[str, bytes] = {}) -> Module:
        self._check_closed()
        return Module(self._c.new_module(module_tag, config))

    def new_module_from_hash(self, module_hash: str, config: Dict[str, bytes] = {}) -> Module:
        self._check_closed()
        return Module(self._c.new_module_from_hash(module_hash, config))

    def new_module_from_cls(self, module_cls, config: Dict[str, bytes] = {}):
        config = config.copy()
        if "_py_module_cls" in config:
            raise ValueError("Config for SerializedPythonModule may not contain key _py_module_cls")
        if "_py_module_name" in config:
            raise ValueError("Config for SerializedPythonModule may not contain key _py_module_name")
        config["_py_module_cls"] = inspect.getsource(module_cls)
        config["_py_module_name"] = module_cls.__name__.encode()
        return self.new_module("SerializedPythonModule", config)

    def _allocate_value(self, metadata: ValueMetadata):
        ser_metadata = b''
        if metadata is not None:
            ser_metadata = metadata.SerializeToString()
        return Value(self._c.allocate_value(ser_metadata))

    def allocate_bytes(self, size: int):
        self._check_closed()
        metadata = ValueMetadata()
        metadata.size = size
        metadata.bytes.SetInParent()
        return self._allocate_value(metadata)

    def from_bytes(self, val: bytes) -> Value:
        self._check_closed()
        v = self.allocate_bytes(len(val))
        v.set_bytes(val)
        return v

    def _allocate_numpy(
        self,
        dtype: np.dtype,
        shape: List[int],
    ) -> Value:
        metadata = Value._get_tensor_metadata(dtype, shape)
        v = self._allocate_value(metadata)
        return v

    def from_numpy(self, val: np.ndarray) -> Value:
        self._check_closed()
        v = self._allocate_numpy(val.dtype, val.shape)
        v.numpy()[:] = val
        return v

    def start_profiling(self):
        return Profiler(self._c.start_profiling())

    def _enable_glog_stacktrace(self):
        self._check_closed()
        self._c._enable_glog_stacktrace()
