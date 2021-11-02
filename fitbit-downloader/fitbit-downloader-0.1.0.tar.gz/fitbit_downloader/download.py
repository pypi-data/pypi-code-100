import datetime
from pathlib import Path
from typing import Optional, Type, Any

import fitbit
from pydantic import BaseModel

from fitbit_downloader.client import get_client
from fitbit_downloader.config import Config, Dataset
from fitbit_downloader.logger import logger
from fitbit_downloader.models.activityresponse import ActivityResponse
from fitbit_downloader.models.distanceresponse import DistanceResponse
from fitbit_downloader.models.elevationresponse import ElevationResponse
from fitbit_downloader.models.floorsresponse import FloorsResponse
from fitbit_downloader.models.heartresponse import HeartResponse
from fitbit_downloader.models.sleepresponse import SleepResponse
from fitbit_downloader.models.stepsresponse import StepsResponse


def download_data(config: Config, custom_date: Optional[datetime.date] = None):
    date = custom_date or _yesterday()
    logger.info(f"Downloading data for {date}")
    client = get_client(config)
    if not config.download.out_folder.exists():
        config.download.out_folder.mkdir()
    for dataset in config.download.datasets:
        logger.info(f"Downloading data for {dataset.value}")
        if dataset in (
            Dataset.STEPS,
            Dataset.HEART,
            Dataset.ELEVATION,
            Dataset.DISTANCE,
            Dataset.FLOORS,
        ):
            _download_intraday_data(dataset, client, config, date)
        elif dataset == Dataset.SLEEP:
            _download_sleep_data(dataset, client, config, date)
        elif dataset == Dataset.ACTIVITIES:
            _download_activity_data(dataset, client, config, date)


def _download_intraday_data(
    dataset: Dataset, client: fitbit.Fitbit, config: Config, date: datetime.date
):
    activity_str = f"activities/{dataset.value}"
    data = client.intraday_time_series(activity_str, base_date=date)
    response_cls = _get_intraday_response_class(dataset)
    out_path = _get_out_path(dataset, config, date)
    _save(out_path, data, response_cls)


def _download_sleep_data(
    dataset: Dataset, client: fitbit.Fitbit, config: Config, date: datetime.date
):
    data = client.get_sleep(date)
    out_path = _get_out_path(dataset, config, date)
    _save(out_path, data, SleepResponse)


def _download_activity_data(
    dataset: Dataset, client: fitbit.Fitbit, config: Config, date: datetime.date
):
    data = client.activities(date=date)  # type: ignore
    out_path = _get_out_path(dataset, config, date)
    _save(out_path, data, ActivityResponse)


def _save(out_path: Path, data: dict[str, Any], response_cls: Type[BaseModel]):
    model = response_cls(**data)
    out_path.write_text(model.json(indent=2))


def _get_out_path(dataset: Dataset, config: Config, date: datetime.date) -> Path:
    out_folder = config.download.out_folder / dataset.value
    if not out_folder.exists():
        out_folder.mkdir()
    return out_folder / (date.strftime("%Y-%m-%d") + ".json")


def _get_intraday_response_class(dataset: Dataset) -> Type[BaseModel]:
    if dataset == Dataset.STEPS:
        return StepsResponse
    if dataset == Dataset.HEART:
        return HeartResponse
    if dataset == Dataset.ELEVATION:
        return ElevationResponse
    if dataset == Dataset.DISTANCE:
        return DistanceResponse
    if dataset == Dataset.FLOORS:
        return FloorsResponse
    raise NotImplementedError(f"need to add handling for intraday {dataset.value}")


def _yesterday() -> datetime.date:
    return datetime.date.today() - datetime.timedelta(days=1)
