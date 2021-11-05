import atexit
import os
import signal
import sys
import threading
from datetime import datetime
from typing import Any, Dict, List, Optional

from urllib3.exceptions import MaxRetryError

from openapi_client.models.experiment_metric_entry import ExperimentMetricEntry
from openapi_client.models.experiment_metrics_update_api_payload import (
    ExperimentMetricsUpdateAPIPayload,
)
from openapi_client.models.influxdb_experiment_plot_file import (
    InfluxdbExperimentPlotFile,
)
from openapi_client.models.local_experiment_finish_api_payload import (
    LocalExperimentFinishAPIPayload,
)
from openapi_client.models.response_experiment_info import ResponseExperimentInfo
from vessl.cli._util import Endpoint
from vessl.internal.collector import (
    Collector,
    IOCollector,
    K8sCollector,
    SystemMetricCollector,
    UserMetricCollector,
)
from vessl.util import logger
from vessl.util.api import VesslApi
from vessl.util.common import safe_cast
from vessl.util.constant import VESSL_IMAGE_PATH, VESSL_PLOTS_FILETYPE_IMAGE, WEB_HOST
from vessl.util.exception import InvalidExperimentError, VesslApiException
from vessl.util.image import Image

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

        self._get_experiment_from_environment()

    def _get_experiment_from_environment(self):
        experiment_id = os.environ.get("VESSL_EXPERIMENT_ID", None)
        access_token = os.environ.get("VESSL_ACCESS_TOKEN", None)

        if experiment_id is None or access_token is None:
            return

        self.api.update_access_token(access_token)
        try:
            self._experiment = self.api.experiment_read_by_idapi(
                experiment_id=experiment_id
            )
        except VesslApiException:
            pass

    def _get_experiment_from_args(
        self, experiment_name_or_number=None, message: str = None
    ) -> ResponseExperimentInfo:

        if experiment_name_or_number is None:
            # Prevent circular import
            from vessl.experiment import create_local_experiment

            expr = create_local_experiment(message=message)
            logger.debug(f"Created experiment {expr.id}")
            return expr

        # Prevent circular import
        from vessl.experiment import read_experiment

        expr = read_experiment(experiment_name_or_number)
        if not expr.is_local or expr.local_execution_spec is None:
            raise InvalidExperimentError(
                f"{expr.name}: cannot use Vessl-managed experiment."
            )
        if expr.status != "running":
            raise InvalidExperimentError(f"{expr.name}: experiment must be running.")

        return expr

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
        if self._mode == MODE_NOT_STARTED:
            print(f"Initializing a new experiment...")
            self.api.initialize()
            self._experiment: ResponseExperimentInfo = self._get_experiment_from_args(
                experiment_name_or_number, message
            )

        canonical_experiment_slug = (
            f"{self._experiment.organization.name}/"
            f"{self._experiment.project.name}/{self._experiment.name}"
        )
        print(
            f"Connected to experiment: {self._experiment.organization.name}/{self._experiment.project.name}/{self._experiment.name} "
            f"({Endpoint.experiment.format(self._experiment.organization.name, self._experiment.project.name, self._experiment.number)})"
        )

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
        finished_expr = self._experiment
        self._mode = MODE_NOT_STARTED
        self._experiment: Optional[ResponseExperimentInfo] = None
        print(
            f"Finished experiment: {finished_expr.organization.name}/{finished_expr.project.name}/{finished_expr.name}"
        )

    def log(self, payload: Dict[str, Any], step: Optional[int] = None) -> int:
        if self._experiment is None:
            logger.warning("Invalid. Use `vessl.init()` first.")
            return -1

        metric_payload = {}
        image_payload = {}
        for k, v in payload.items():
            if isinstance(v, list) and all(isinstance(i, Image) for i in v):
                image_payload[k] = v
            elif isinstance(v, Image):
                image_payload[k] = [v]
            else:
                metric_payload[k] = v

        if metric_payload or step:
            self._user_metric_collector.handle_step(step)

        if image_payload:
            self._update_images(image_payload)
        if metric_payload:
            payloads = [
                self._user_metric_collector.build_metric_payload(metric_payload)
            ]
            if self._mode == MODE_NOT_STARTED:
                self.api.experiment_metrics_update_api(
                    self._experiment.id,
                    experiment_metrics_update_api_payload=ExperimentMetricsUpdateAPIPayload(
                        metrics=payloads
                    ),
                )
                return self._user_metric_collector.step
            return self._user_metric_collector.log_metrics(payloads)

    def _update_images(self, row: Dict[str, List[Image]]):
        path_to_caption = {}
        for images in row.values():
            for image in images:
                path_to_caption[image.path] = image.caption

        source_path = os.path.join(VESSL_IMAGE_PATH, "")
        assert self._experiment
        dest_volume_id = self._experiment.experiment_plot_volume
        dest_path = "/"

        from vessl.volume import copy_volume_file  # to avoid circular import

        files = copy_volume_file(
            source_volume_id=None,
            source_path=source_path,
            dest_volume_id=dest_volume_id,
            dest_path=dest_path,
            recursive=True,
        )

        for images in row.values():
            for image in images:
                image.flush()

        if files:
            plot_files = [
                InfluxdbExperimentPlotFile(
                    step=None,
                    path=file.path,
                    caption=path_to_caption[file.path],
                    timestamp=datetime.utcnow().timestamp(),
                )
                for file in files
                if file.path in path_to_caption
            ]
        else:
            plot_files = []

        workload_id = safe_cast(os.environ.get("VESSL_WORKLOAD_ID", None), int)

        payloads: List[ExperimentMetricEntry] = []
        for f in plot_files:
            payload = {
                VESSL_PLOTS_FILETYPE_IMAGE: f,
                "workload_id": workload_id,
            }
            payloads.append(self._user_metric_collector.build_image_payload(payload))

        if self._mode == MODE_NOT_STARTED:
            self.api.experiment_metrics_update_api(
                self._experiment.id,
                experiment_metrics_update_api_payload=ExperimentMetricsUpdateAPIPayload(
                    metrics=payloads
                ),
            )
        else:
            self._user_metric_collector.log_images(payloads)
