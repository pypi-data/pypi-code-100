from helios.base import HeliosBase, HeliosTags  # noqa: F401 (ignore lint error: imported but not used)
from helios.helios import Helios
from typing import Optional, Union, Dict


def initialize(api_token: str,
               service_name: str,
               enabled: bool = False,
               collector_endpoint: Optional[str] = None,
               sampling_ratio: Optional[Union[float, int, str]] = 1.0,
               environment: Optional[str] = None,
               resource_tags: Optional[Dict[str, Union[bool, float, int, str]]] = None,
               **kwargs) -> Helios:
    return Helios(api_token, service_name, enabled, collector_endpoint,
                  sampling_ratio, environment, resource_tags, **kwargs)
