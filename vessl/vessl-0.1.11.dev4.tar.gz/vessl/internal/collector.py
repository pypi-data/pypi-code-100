import sys
import threading
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Text

import psutil
import pynvml

import vessl
from openapi_client.models import ExperimentMetricEntry
from vessl.util import logger
from vessl.util.image import Image
from vessl.util.logger import set_log_io


class Collector(ABC):
    def __init__(self):
        self.buffer: List[ExperimentMetricEntry] = []
        self.lock = threading.Lock()

    def add(self, entries: List[ExperimentMetricEntry]):
        with self.lock:
            self.buffer += entries

    def collect(self):
        with self.lock:
            return self.buffer[:]

    def truncate(self, idx):
        with self.lock:
            self.buffer = self.buffer[idx:]

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass


class IOCollector(Collector):
    class IOHook(object):
        def __init__(self, io, callback):
            self._io = io
            self._callback = callback

        def write(self, content: Text):
            if content.strip() != "":
                self._callback(time.time(), content)
            self._io.write(content)

        def flush(self):
            self._io.flush()

    def __init__(self):
        super().__init__()

    def start(self):
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr

        stdout_hook = self.IOHook(sys.stdout, self.create_callback("stdout"))
        stderr_hook = self.IOHook(sys.stderr, self.create_callback("stderr"))

        sys.stdout = stdout_hook
        sys.stderr = stderr_hook
        set_log_io(stderr_hook)

    def create_callback(self, io_name):
        def f(ts, content):
            self.add(
                [
                    ExperimentMetricEntry(
                        measurement="log", ts=ts, tags={}, fields={io_name: content}
                    )
                ]
            )

        return f

    def stop(self):
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        set_log_io(self.old_stderr)


class SystemMetricCollector(Collector):
    def __init__(self, gpu_count: int) -> None:
        super().__init__()
        self._gpu_count = gpu_count
        self._proc = psutil.Process()
        self._collect_interval_sec: float = 1
        self._thread = threading.Thread(target=self._thread_body, daemon=True)
        self._exit = threading.Event()

    def start(self):
        self._thread.start()

    def stop(self):
        self._exit.set()
        self._thread.join()

    def _thread_body(self):
        # Call to set latest value and junk return
        # https://psutil.readthedocs.io/en/latest/index.html?highlight=pcputimes#psutil.cpu_percent
        with self._proc.oneshot():
            psutil.cpu_percent()
            self._proc.cpu_percent()

        while not self._exit.is_set():
            self.add(entries=self._stats())
            self._exit.wait(timeout=self._collect_interval_sec)

    def _stats(self) -> List[ExperimentMetricEntry]:
        ts = time.time()
        entries = []
        with self._proc.oneshot():
            entries.append(
                ExperimentMetricEntry(
                    measurement="system_metric",
                    ts=ts,
                    fields={
                        "process_cpu_percent": self._proc.cpu_percent(),
                        "process_mem_percent": self._proc.memory_percent(),
                        "device_cpu_percent": psutil.cpu_percent(),
                        "device_mem_percent": psutil.virtual_memory().percent,
                    },
                    tags={
                        "type": "local",
                    },
                )
            )

        for i in range(self._gpu_count):
            try:
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            except pynvml.nvml.NVMLError:
                continue
            gpu_name = pynvml.nvmlDeviceGetName(handle).decode()
            component = f"{gpu_name} #{i+1}"
            use = pynvml.nvmlDeviceGetUtilizationRates(handle)

            entries.append(
                ExperimentMetricEntry(
                    measurement="system_metric",
                    ts=ts,
                    fields={
                        "device_gpu_util_percent": use.gpu,
                        "device_gpu_mem_percent": use.memory,
                    },
                    tags={
                        "type": "local",
                        "component": component,
                    },
                )
            )

        return entries


class UserMetricCollector(Collector):
    def __init__(self) -> None:
        super().__init__()
        self._step_counter = 0

    def start(self):
        pass

    def stop(self):
        pass

    def log(self, payload: Dict[str, Any], step: Optional[int] = None) -> int:
        if step:
            if step < self._step_counter:
                vessl.log.warn("step cannot go backwards")
        else:
            self._step_counter += 1
            step = self._step_counter

        metric_payload = {}
        image_payload = {}
        for k, v in payload.items():
            if isinstance(v, list) and all(isinstance(i, Image) for i in v):
                image_payload[k] = v
            else:
                metric_payload[k] = v

        ts = time.time()
        if metric_payload:
            self.add(
                [
                    ExperimentMetricEntry(
                        measurement="experiment_plot_metric",
                        ts=ts,
                        tags={"step": str(step)},
                        fields={**metric_payload},
                    )
                ]
            )

        if image_payload:
            self.add(
                [
                    ExperimentMetricEntry(
                        measurement="experiment_plot_file",
                        ts=ts,
                        tags={"step": str(step)},
                        fields={**image_payload},
                    )
                ]
            )
        return step


class K8sCollector(Collector):
    def __init__(self) -> None:
        super().__init__()

    def start(self):
        # TODO
        pass

    def stop(self):
        # TODO
        pass
