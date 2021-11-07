from enum import Enum


class APIVersion(Enum):
    APRIL_2021 = '2021-04'


BASE_VERSION = APIVersion.APRIL_2021.value
