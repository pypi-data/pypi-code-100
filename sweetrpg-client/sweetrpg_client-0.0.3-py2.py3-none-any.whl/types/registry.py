# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Type registry.
"""

from ..constants import *
from ..types import *
from sweetrpg_library_objects.api.volume.schema import VolumeAPISchema

_types = {
    VOLUME: {
        ENDPOINT_PATH: 'volumes',
        API_SCHEMA_CLASS: VolumeAPISchema,
    }
}
