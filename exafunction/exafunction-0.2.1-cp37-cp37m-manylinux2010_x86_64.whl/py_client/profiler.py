# Copyright Exafunction, Inc.

from exa.common_pb.common_pb2 import PerfCounters
import exa._C as _C

class Profiler:
    def __init__(self, c: _C.Profiler):
        self._c = c

    def count(self):
        perf_counters = PerfCounters()
        ser_perf_counters = self._c.count()
        perf_counters.ParseFromString(ser_perf_counters)
        return perf_counters
