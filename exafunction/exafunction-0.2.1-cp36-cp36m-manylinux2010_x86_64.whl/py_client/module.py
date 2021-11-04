# Copyright Exafunction, Inc.

from typing import Dict

from exa.common_pb.common_pb2 import MethodInfo
from exa.py_value import Value
import exa._C as _C

class Module:
    def __init__(self, c: _C.Module):
        self._c = c

    def _check_valid(self):
        if not self._c.is_valid():
            raise ValueError("Module is not valid (was the session closed?)")

    def module_id(self) -> int:
        self._check_valid()
        return self._c.module_id

    def run_method(self, method_name: str, **inputs: Dict[str, Value]) -> Dict[str, Value]:
        self._check_valid()
        cc_inputs = {k: inp._c for k, inp in inputs.items()}
        cc_outputs = self._c.run_method(method_name, cc_inputs)
        return {k: Value(out) for k, out in cc_outputs.items()}

    def run(self, **inputs: Dict[str, Value]) -> Dict[str, Value]:
        return self.run_method("run", **inputs)

    def ensure_local_valid(self, values: Dict[str, Value]):
        self._check_valid()
        cc_values = {k: inp._c for k, inp in values.items()}
        return self._c.ensure_local_valid(cc_values)

    def get_method_info(self, method_name: str = "run"):
        self._check_valid()
        serialized_info = self._c.get_method_info(method_name)
        mi = MethodInfo()
        mi.ParseFromString(serialized_info)
        return mi
