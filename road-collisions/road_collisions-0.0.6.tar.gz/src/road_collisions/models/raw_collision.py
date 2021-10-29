import os
import glob
import json

from road_collisions import logger
from road_collisions.utils import epsg_900913_to_4326
from road_collisions.models.generic import GenericObject, GenericObjects


data_props = [
    'lat',
    'lng',
    'year',
    'weekday',
    'gender',
    'age',
    'vehicle_type',
    'vehicle',
    'hour',
    'circumstances',
    'num_fatal',
    'num_minor',
    'num_notinjured',
    'num_serious',
    'num_unknown',
    'speed_limit',
    'severity',
    'county',
    'carrf',
    'carri',
    'class2',
    'goodsrf',
    'goodsri',
    'mcycrf',
    'mcycri',
    'otherrf',
    'otherri',
    'pcycrf',
    'pcycri',
    'pedrf',
    'pedri',
    'psvrf',
    'psvri',
    'unknrf',
    'unknri'
]


class RawCollision():

    def __init__(self, **kwargs):
        self.data = kwargs

    @staticmethod
    def parse(data):
        if isinstance(data, RawCollision):
            return data

        lat_lng = list(
            reversed(
                epsg_900913_to_4326(
                    data['geometry']['x'],
                    data['geometry']['y']
                )
            )
        )

        remaps = {  # These are reversed (new: old)
            'gender': 'sex',
            'num_fatal': 'no_fatal',
            'num_minor': 'no_minor',
            'num_notinjured': 'no_notinjured',
            'num_serious': 'no_serious',
            'num_unknown': 'no_unknown',
            'speed_limit': 'splimit',
            'vehicle_type': 'class1',
            'severity': 'type',
            'circumstances': 'prcoltyp'
        }

        parsed = {}

        for prop in data_props:
            parsed[prop] = data['data'].get(remaps.get(prop, prop), None)

        parsed['lat'] = lat_lng[0]
        parsed['lng'] = lat_lng[1]

        return RawCollision(
            **parsed
        )
