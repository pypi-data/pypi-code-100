from __future__ import annotations

import functools
import os
import signal
import subprocess
import sys
import threading
import time
import traceback
from types import FrameType
from typing import Dict, Iterable, Iterator, NamedTuple, Protocol

_POLL_INTERVAL = 0.1
_SIGNAL_TIMEOUT = 15
_MONITOR_THREAD_TIMEOUT = 5
_CONDITION_CHECK_INTERVAL = 1
_CONDITION_CHECK_TIMEOUT = 10


class WorkerConfig(NamedTuple):
    name: str
    num_workers: int
    cmd: list[str]
    env: dict[str, str] | None = None
    start_condition_cmd: list[str] | None = None
    stop_signal: str = 'SIGTERM'
    stop_order: int = 1
    signal_to_pg: bool = False


WorkerConfigDict = Dict[str, WorkerConfig]


class WorkerEntry(NamedTuple):
    worker_config: WorkerConfig
    process_wraper_list: list[ProcessWrapper]


class ProcessWrapper(NamedTuple):
    parent_worker_config: WorkerConfig

    name: str
    popen_obj: subprocess.Popen
    monitor: threading.Thread

    @property
    def pid(self) -> int:
        return self.popen_obj.pid

    @property
    def pgid(self) -> int:
        return os.getpgid(self.pid)


class _PrinterType(Protocol):
    def __call__(self, prefix: str, txt: str, *, is_stdout: bool = False) -> None:
        ...


def _make_progress_wrapper_iter(worker_entries: Iterable[WorkerEntry]) -> Iterator[ProcessWrapper]:
    for worker_entry in worker_entries:
        for progress_wrapper in worker_entry.process_wraper_list:
            yield progress_wrapper


def _process_launcher(
    term_event: threading.Event,
    printer: _PrinterType,
    worker_entry: WorkerEntry,
) -> None:
    worker_config = worker_entry.worker_config

    if worker_config.start_condition_cmd is not None:
        printer(worker_config.name, 'Check start condition...')

        while not term_event.is_set():
            try:
                condition_result = subprocess.run(
                    worker_config.start_condition_cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT,
                    timeout=_CONDITION_CHECK_TIMEOUT,
                )
                if condition_result.returncode == 0:
                    break
            except Exception:
                pass

            printer(worker_config.name, 'Start condition is not met')

            time.sleep(_CONDITION_CHECK_INTERVAL)

    for idx in range(worker_config.num_workers):
        if term_event.is_set():
            return

        process_name = f'{worker_config.name}_{idx + 1}'

        popen_obj = subprocess.Popen(
            worker_config.cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=worker_config.env,
            text=True,
            start_new_session=True,
        )

        monitor = threading.Thread(
            target=functools.partial(_process_monitor, printer, process_name, popen_obj),
            daemon=True,
        )
        monitor.start()

        process_wrapper = ProcessWrapper(
            parent_worker_config=worker_config,
            name=process_name,
            popen_obj=popen_obj,
            monitor=monitor,
        )

        printer(process_name, f'Started a process (PID {process_wrapper.pid}, PGID {process_wrapper.pgid})')

        worker_entry.process_wraper_list.append(process_wrapper)


def _process_monitor(
    printer: _PrinterType,
    process_name: str,
    popen_obj: subprocess.Popen,
) -> None:
    assert popen_obj.stdout is not None

    while True:
        try:
            output: str = popen_obj.stdout.readline()
        except Exception:
            print(
                'Error while reading outputs from "%s"\n%s' % (process_name, traceback.format_exc()),
                flush=True,
            )
            break

        if not output:
            break

        printer(process_name, output.rstrip(), is_stdout=True)

    while True:
        retcode = popen_obj.poll()
        if retcode is not None:
            break
        time.sleep(_POLL_INTERVAL)

    printer(process_name, f'Terminated (retcode: {retcode})')


def run(worker_config_dict: WorkerConfigDict) -> None:
    '''Run a set of processes defined by `worker-config`

    .. note:: Example Configuration

        import os

        worker_config = {
            'manager': {
                'num_workers': 1,
                'cmd': ['python', 'launcher_manager.py'],
                'env': {
                    'MANAGER_IN_PORT': '80',
                    'MANAGER_OUT_PORT': '1234',
                },
                'stop_order': 3
            },
            'http-server': {
                'num_workers': 1,
                'cmd': [
                    'gunicorn',
                    '-c', './assets/gunicorn_conf.py',
                    'launcher_http_server:server.app',
                ],
                'stop_order': 2
            },
            'http-server-nginx': {
                'num_workers': 1,
                'cmd': ['nginx', '-g', 'daemon off;'],
                'start_condition_cmd': [
                    'curl',
                    '--fail', '-s',
                    'http://0.0.0.0:8080/ping',
                ],
                'stop_signal': 'SIGQUIT'
            },
            'tcp-server': {
                'num_workers': int(os.environ.get('TCP_SERVER_NUM_WORKERS', 1)),
                'cmd': ['python', 'launcher_tcp_server.py'],
                'stop_order': 2
            }
        }
    '''

    term_signal = signal.Signals.SIGTERM
    term_event = threading.Event()

    def _signal_handler(signum: int, frame: FrameType) -> None:
        if term_event.is_set():
            print('Forced termination of manager', flush=True)
            sys.exit(1)

        nonlocal term_signal
        term_signal = signal.Signals(signum)
        term_event.set()
        print('Signal handler called with signal :', term_signal.name, flush=True)

    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)

    max_name_length = max(
        len('%s_%d' % (worker_config.name, worker_config.num_workers + 1))
        for worker_config in worker_config_dict.values()
    )

    def _printer(prefix: str, txt: str, *, is_stdout: bool = False) -> None:
        formatstr = '%-{:d}s %s %s'.format(max_name_length)
        print(formatstr % (prefix, '|' if is_stdout else '>', txt), flush=True)

    worker_entries: list[WorkerEntry] = []
    for worker_config in worker_config_dict.values():
        if worker_config.stop_signal.upper() not in signal.Signals.__members__:
            raise RuntimeError('Invalid stop signal', worker_config)

        worker_entry = WorkerEntry(worker_config, [])
        worker_entries.append(worker_entry)

        worker_process_launcher = threading.Thread(
            target=functools.partial(_process_launcher, term_event, _printer, worker_entry),
            daemon=True
        )
        worker_process_launcher.start()

    # Monitor the liveness of all worker processes
    any_done_process_wrapper: ProcessWrapper | None = None
    try:
        while not term_event.is_set():
            for process_wrapper in _make_progress_wrapper_iter(worker_entries):
                if process_wrapper.popen_obj.poll() is not None:
                    any_done_process_wrapper = process_wrapper
                    term_event.set()
                    break

                time.sleep(_POLL_INTERVAL)

        else:
            print(
                'Terminate all processes... (cuased by %s)' % (
                    any_done_process_wrapper.name if any_done_process_wrapper else 'signal'
                ),
                flush=True
            )

    except Exception:
        traceback.print_exc()

    stop_order_to_worker_entries: dict[int, list[WorkerEntry]] = {}
    for worker_entry in worker_entries:
        stop_order = worker_entry.worker_config.stop_order
        if stop_order not in stop_order_to_worker_entries:
            stop_order_to_worker_entries[stop_order] = []
        stop_order_to_worker_entries[stop_order].append(worker_entry)

    for _, target_worker_entries in sorted(stop_order_to_worker_entries.items()):
        for process_wrapper in _make_progress_wrapper_iter(target_worker_entries):
            retcode = process_wrapper.popen_obj.poll()
            if retcode is not None:
                continue

            stop_signal = signal.Signals[process_wrapper.parent_worker_config.stop_signal.upper()]

            _printer(
                process_wrapper.name,
                f'{stop_signal.name} is requested (PID: {process_wrapper.pid}, PGID: {process_wrapper.pgid})',
            )

            if process_wrapper.parent_worker_config.signal_to_pg:
                os.killpg(process_wrapper.pgid, stop_signal.value)
            else:
                os.kill(process_wrapper.pid, stop_signal.value)

        wait_until_ts = time.monotonic() + _SIGNAL_TIMEOUT
        while time.monotonic() < wait_until_ts:
            for process_wrapper in _make_progress_wrapper_iter(target_worker_entries):
                retcode = process_wrapper.popen_obj.poll()
                if retcode is None:
                    break
            else:
                break
            time.sleep(_POLL_INTERVAL)
        else:
            print('Timeout while waiting the termination of worker processes', flush=True)

        wait_until_ts = time.monotonic() + _MONITOR_THREAD_TIMEOUT
        while time.monotonic() < wait_until_ts:
            for process_wrapper in _make_progress_wrapper_iter(target_worker_entries):
                process_wrapper.monitor.join(0)
                if process_wrapper.monitor.is_alive():
                    break
            else:
                break
            time.sleep(_POLL_INTERVAL)
        else:
            print('Timeout while waiting the termination of monitor threads', flush=True)

    for process_wrapper in _make_progress_wrapper_iter(worker_entries):
        if process_wrapper.monitor.is_alive():
            print(f'Live monitor thread : {process_wrapper.name}', flush=True)
