import os
import typing
from collections import defaultdict
from datetime import datetime
from numbers import Number
from typing import Dict, List, Optional, SupportsFloat, Union

from openapi_client.models import (
    InfluxdbExperimentPlotFile,
    InfluxdbExperimentPlotMetric,
    ResponseExperimentInfo,
)
from vessl import vessl_api
from vessl.experiment import (
    read_experiment_by_id,
    update_experiment_plots_files,
    update_experiment_plots_metrics,
)
from vessl.util import logger
from vessl.util.constant import VESSL_IMAGE_PATH, VESSL_PLOTS_FILETYPE_IMAGE
from vessl.util.exception import VesslApiException
from vessl.util.image import Image
from vessl.volume import copy_volume_file

ImageRowType = Dict[str, List[Image]]
MetricRowType = Dict[str, SupportsFloat]
RowType = Union[ImageRowType, MetricRowType]

current_experiment: Optional[ResponseExperimentInfo] = None


def _update_current_experiment():
    global current_experiment
    experiment_id = os.environ.get("VESSL_EXPERIMENT_ID", None)
    access_token = os.environ.get("VESSL_ACCESS_TOKEN", None)

    if experiment_id is None or access_token is None:
        return

    vessl_api.update_access_token(access_token)
    current_experiment = read_experiment_by_id(int(experiment_id))


def get_current_experiment() -> Optional[ResponseExperimentInfo]:
    global current_experiment
    if current_experiment != None:
        return current_experiment

    _update_current_experiment()
    return current_experiment


def get_current_experiment_id() -> int:
    assert current_experiment
    assert current_experiment.id
    return current_experiment.id
