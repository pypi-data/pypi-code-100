import atexit
import signal
import sys
import threading
from typing import Any, Dict, List, Optional

from urllib3.exceptions import MaxRetryError

from openapi_client.models.experiment_metrics_update_api_payload import (
    ExperimentMetricsUpdateAPIPayload,
)
from openapi_client.models.local_experiment_finish_api_payload import (
    LocalExperimentFinishAPIPayload,
)
from openapi_client.models.response_experiment_info import ResponseExperimentInfo
from vessl.internal.collector import (
    Collector,
    IOCollector,
    K8sCollector,
    SystemMetricCollector,
    UserMetricCollector,
)
from vessl.util import logger
from vessl.util.api import VesslApi
from vessl.util.exception import VesslApiException

MODE_TEST = "TEST"
MODE_NOT_STARTED = "NOT_STARTED"
MODE_SDK = "SDK"
MODE_SIDECAR = "SIDECAR"

SEND_INTERVAL_IN_SEC = 10


class Sender(object):
    def __init__(self, api: VesslApi, experiment_id: int, collectors: List[Collector]):
        self._api = api
        self._experiment_id: int = experiment_id
        self._thread = threading.Thread(target=self._thread_body, daemon=True)
        self._exit = threading.Event()
        self._collectors = collectors

    def stop(self):
        for c in self._collectors:
            c.stop()

        self._exit.set()
        self._thread.join()

    def start(self):
        for c in self._collectors:
            c.start()
        self._thread.start()

    def _thread_body(self):
        while not self._exit.is_set():
            self._send()
            self._exit.wait(timeout=SEND_INTERVAL_IN_SEC)
        self._send()

    def _send(self):
        pairs = [(c, c.collect()) for c in self._collectors]
        for c, m in pairs:
            logger.debug(f"{c} / {m}", str(c), len(m))
        payload = [m for _, metrics in pairs for m in metrics]
        logger.debug(f"sending {len(payload)} payloads")

        try:
            self._api.experiment_metrics_update_api(
                self._experiment_id,
                experiment_metrics_update_api_payload=ExperimentMetricsUpdateAPIPayload(
                    metrics=payload
                ),
            )

            for c, m in pairs:
                c.truncate(len(m))

        except MaxRetryError as e:
            logger.exception("Failed to send metrics to server", exc_info=e)
        except VesslApiException as e:
            logger.exception("Failed to send metrics to server", exc_info=e)
        except Exception as e:
            logger.exception("Unexpected error", exc_info=e)


class VesslRun(object):
    class ExitHook(object):
        def __init__(self, orig_exit):
            self.orig_exit = orig_exit
            self.exit_code = 0

        def exit(self, code=0):
            self.exit_code = code
            self.orig_exit(code)

    __slots__ = [
        "api",
        "_mode",
        "_collectors",
        "_sender",
        "_experiment",
        "_logger",
        "_user_metric_collector",
        "_exit_hook",
    ]

    def __init__(self) -> None:
        self.api = VesslApi()
        self._mode = MODE_NOT_STARTED
        self._experiment: Optional[ResponseExperimentInfo] = None
        self._user_metric_collector = UserMetricCollector()
        self._exit_hook = self.ExitHook(sys.exit)

    def _has_sidecar(self):
        # TODO: implement
        return False

    def _signal_handler(self, signo, frames):
        sys.exit(130)  # job was terminated by the owner

    def _start(self, is_test=False):
        if is_test:
            return

        self._sender.start()

        sys.exit = self._exit_hook.exit
        atexit.register(self._atexit)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _atexit(self):
        self._stop()

    def _stop(self, exit_code=0):
        self._sender.stop()
        sys.exit = self._exit_hook.orig_exit
        self.api.local_experiment_finish_api(
            self._experiment.id,
            local_experiment_finish_api_payload=LocalExperimentFinishAPIPayload(
                exit_code=self._exit_hook.exit_code
            ),
        )

    def init(self, experiment_name_or_number=None, message: str = None, is_test=False):
        from vessl.experiment import create_local_experiment

        self.api.initialize()

        if experiment_name_or_number is None:
            self._experiment = create_local_experiment(message=message)
            logger.debug(f"Created experiment {self._experiment.id}")
        else:
            from vessl.experiment import read_experiment  # Due to circular import

            experiment = read_experiment(experiment_name_or_number)
            if not experiment.is_local or experiment.local_execution_spec is None:
                logger.warning(
                    f"Invalid experiment {experiment.name}: cannot use Vessl-managed experiment."
                )
                return
            if experiment.status != "running":
                logger.warning(
                    f"Invalid experiment {experiment.name}: experiment must be running."
                )
                return

            self._experiment = experiment

        # init exposed to user
        # This should be called from user code
        if self._mode != MODE_NOT_STARTED:
            return
        self._mode = MODE_SDK

        collectors: List[Collector] = []
        if not is_test:
            # When vessl.init() has been called from user code with sidecar (Vessl-Managed)
            if self._has_sidecar():
                collectors = [self._user_metric_collector]

            # When vessl.init() has been called from user code without sidecar daemon (Local)
            else:
                gpu_count = self._experiment.local_execution_spec.gpu_count or 0
                collectors = [
                    IOCollector(),
                    SystemMetricCollector(gpu_count),
                    self._user_metric_collector,
                ]
            self._sender = Sender(self.api, self._experiment.id, collectors)

        self._start(is_test)

    def upload(self, path: str):
        if self._experiment is None:
            logger.warning("Invalid. Use `vessl.init()` first.")
            return

        from vessl.experiment import (
            upload_experiment_output_files,  # Due to circular import
        )

        upload_experiment_output_files(self._experiment.name, path)

    def finish(self):
        if self._experiment is None:
            logger.warning("Invalid. Use `vessl.init()` first.")
            return

        self._stop()

    def log(self, payload: Dict[str, Any], step: Optional[int] = None) -> int:
        if self._experiment is None:
            logger.warning("Invalid. Use `vessl.init()` first.")
            return

        return self._user_metric_collector.log(payload, step)
