import datetime
import functools
import io
from importlib import import_module
from typing import (
    Any,
    BinaryIO,
    Callable,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

import _io

from neuroio.constants import sentinel

ImageType = Union[BinaryIO, Tuple[str, io.BytesIO], bytes]


def validate_month_str(month_str: str) -> None:
    try:
        datetime.datetime.strptime(month_str, "%Y-%m")
    except ValueError:
        raise ValueError(
            f"Incorrect month format in {month_str}, should be YYYY-MM"
        )


def get_package_version() -> str:
    from neuroio import __version__

    return __version__


F = TypeVar("F", bound=Callable[..., Any])


def cached_property(f: F) -> property:
    return property(functools.lru_cache()(f))


def prepare_image_processing(
    image: ImageType, filename: str = "image"
) -> dict:
    if isinstance(image, (bytes, bytearray)):
        image_data = io.BytesIO(image)
    elif isinstance(image, _io.BufferedReader):
        image_data = image
        filename = image.name
    elif isinstance(image, tuple):
        filename, image_data = image
    else:
        raise Exception("Wrong image datatype")

    return {"image": (filename, image_data)}


def process_query_params(params: dict) -> dict:
    for key, item in params.items():
        if isinstance(item, list):
            params[key] = ",".join(map(str, item))
    return params


def request_dict_processing(
    local_items: dict, exclude: Optional[List[str]] = None
) -> dict:
    inner_exclude: List[str] = ["self"]
    if exclude is not None:
        inner_exclude.extend(exclude)

    return dict(
        filter(
            lambda kwarg: kwarg[1] is not sentinel
            and kwarg[0] not in inner_exclude,
            local_items.items(),
        )
    )


def request_query_processing(
    local_items: dict, exclude: Union[List[str], None] = None
) -> dict:
    if exclude is None:
        exclude = []
    return process_query_params(request_dict_processing(local_items, exclude))


def request_form_processing(
    local_items: dict, exclude: Union[List[str], None] = None
) -> dict:
    if exclude is None:
        exclude = []
    return {
        key: str(value)
        for key, value in request_dict_processing(local_items, exclude).items()
    }
