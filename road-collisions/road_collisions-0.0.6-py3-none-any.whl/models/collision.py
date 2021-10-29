import os
import glob
import json

from road_collisions import logger
from road_collisions.constants import (
    WEEKDAY_MAP,
    GENDER_MAP,
    VEHICLE_TYPE_MAP,
    HOUR_MAP,
    CIRCUMSTANCS_MAP,
    SEVERITY_MAP,
    COUNTY_MAP
)
from road_collisions.models.generic import (
    GenericObject,
    GenericObjects
)
from road_collisions.models.raw_collision import RawCollision

WEEKDAY_MAP_VALS = WEEKDAY_MAP.values()
GENDER_MAP_VALS = GENDER_MAP.values()
VEHICLE_TYPE_MAP_VALS = VEHICLE_TYPE_MAP.values()
HOUR_MAP_VALS = HOUR_MAP.values()
CIRCUMSTANCS_MAP_VALS = CIRCUMSTANCS_MAP.values()
SEVERITY_MAP_VALS = SEVERITY_MAP.values()
COUNTY_MAP_VALS = COUNTY_MAP.values()


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


class Collision(GenericObject, RawCollision):

    def __init__(self, **kwargs):
        self.data = {}
        for prop in data_props:
            self.data[prop] = kwargs[prop]

        super().__init__()

    @staticmethod
    def parse(data):
        if isinstance(data, Collision):
            return data

        if isinstance(data, dict):
            if 'data' in data.keys():
                return Collision(
                    **RawCollision.parse(
                        data
                    ).data
                )
            else:
                # from serialization
                return Collision(
                    **data
                )

    @property
    def id(self):
        return hash(str(self.serialize()))

    def serialize(self):
        return {
            'lat': self.geo[0],
            'lng': self.geo[1],
            'year': self.year,
            'weekday': self.weekday,
            'gender': self.gender,
            'age': self.age,
            'vehicle_type': self.vehicle_type,
            'vehicle': self.vehicle,
            'hour': self.hour,
            'circumstances': self.circumstances,
            'num_fatal': self.num_fatal,
            'num_minor': self.num_minor,
            'num_notinjured': self.num_notinjured,
            'num_serious': self.num_serious,
            'num_unknown': self.num_unknown,
            'speed_limit': self.speed_limit,
            'severity': self.severity,
            'county': self.county,
            'carrf': self.carrf,
            'carri': self.carri,
            'class2': self.class2,
            'goodsrf': self.goodsrf,
            'goodsri': self.goodsri,
            'mcycrf': self.mcycrf,
            'mcycri': self.mcycri,
            'otherrf': self.otherrf,
            'otherri': self.otherri,
            'pcycrf': self.pcycrf,
            'pcycri': self.pcycri,
            'pedrf': self.pedrf,
            'pedri': self.pedri,
            'psvrf': self.psvrf,
            'psvri': self.psvri,
            'unknrf': self.unknrf,
            'unknri': self.unknri
        }

    @property
    def geo(self):
        return [self.data['lat'], self.data['lng']]

    @property
    def lat(self):
        return self.data['lat']

    @property
    def lng(self):
        return self.data['lng']

    @property
    def year(self):
        if isinstance(self.data['year'], int):
            if self.data['year'] > 2000:
                return self.data['year']
        return int(f'20{str(self.data["year"]).zfill(2)}')

    @property
    def weekday(self):
        if self.data['weekday'] in WEEKDAY_MAP_VALS:
            return self.data['weekday']

        return WEEKDAY_MAP[
            int(self.data['weekday'])
        ]

    @property
    def gender(self):
        gender = None

        if self.data['gender'] in GENDER_MAP_VALS:
            return self.data['gender']

        try:
            gender = GENDER_MAP[
                self.data['gender'].lower()
            ]
        except KeyError:
            logger.debug('Can not parse gender: %s', self.data['gender'])
            gender = self.data['gender']

        return gender

    @property
    def age(self):
        age = None

        if isinstance(self.data['age'], int):
            if self.data['age'] % 10 == 0:
                return self.data['age']

        if self.data['age'] is None:
            return None

        try:
            age = int(self.data['age']) * 10
        except ValueError:
            logger.debug('Can not parse age: %s', self.data['age'])

        return age

    @property
    def vehicle_type(self):
        if self.data['vehicle_type'] in VEHICLE_TYPE_MAP_VALS:
            return self.data['vehicle_type']

        return VEHICLE_TYPE_MAP.get(
            int(self.data['vehicle_type']),
            self.data['vehicle_type']
        )

    @property
    def vehicle(self):
        return self.data['vehicle']

    @property
    def hour(self):
        if self.data['hour'] in HOUR_MAP_VALS:
            return self.data['hour']

        hour = None
        try:
            hour = HOUR_MAP.get(
                int(self.data['hour']),
                self.data['hour']
            )
        except ValueError:
            hour = self.data['hour']

        return hour

    @property
    def circumstances(self):
        if self.data['circumstances'] in CIRCUMSTANCS_MAP_VALS:
            return self.data['circumstances']

        circumstances = None
        try:
            circumstances = CIRCUMSTANCS_MAP.get(
                int(self.data['circumstances']),
                self.data['circumstances']
            )
        except ValueError:
            circumstances = self.data['circumstances']

        return circumstances

    @property
    def num_fatal(self):
        return int(self.data['num_fatal'])

    @property
    def num_minor(self):
        return int(self.data['num_minor'])

    @property
    def num_notinjured(self):
        return int(self.data['num_notinjured'])

    @property
    def num_serious(self):
        return int(self.data['num_serious'])

    @property
    def num_unknown(self):
        return int(self.data['num_unknown'])

    @property
    def speed_limit(self):
        if isinstance(self.data['speed_limit'], int):
            return self.data['speed_limit']

        if self.data['speed_limit'] is None:
            return None

        speed_limit = None
        try:
            speed_limit = int(self.data['speed_limit'])
        except ValueError:
            logger.debug(
                'Could not parse speed limit: %s',
                self.data['speed_limit']
            )

        return speed_limit

    @property
    def severity(self):
        if self.data['severity'] in SEVERITY_MAP_VALS:
            return self.data['severity']

        return SEVERITY_MAP[
            int(self.data['severity'])
        ]

    @property
    def county(self):
        county_lower = self.data['county'].lower()
        if county_lower in COUNTY_MAP_VALS:
            return county_lower

        return COUNTY_MAP[
            int(self.data['county'])
        ]

    # NOT SURE WHAT THE BELOW DO

    @property
    def carrf(self):
        return int(self.data['carrf'])

    @property
    def carri(self):
        return int(self.data['carri'])

    @property
    def class2(self):
        # TODO: looks interesting
        return int(self.data['class2'])

    @property
    def goodsrf(self):
        return int(self.data['goodsrf'])

    @property
    def goodsri(self):
        return int(self.data['goodsri'])

    @property
    def mcycrf(self):
        return int(self.data['mcycrf'])

    @property
    def mcycri(self):
        return int(self.data['mcycrf'])

    @property
    def otherrf(self):
        return int(self.data['otherrf'])

    @property
    def otherri(self):
        return int(self.data['otherri'])

    @property
    def pcycrf(self):
        return int(self.data['pcycrf'])

    @property
    def pcycri(self):
        return int(self.data['pcycri'])

    @property
    def pedrf(self):
        return int(self.data['pedrf'])

    @property
    def pedri(self):
        return int(self.data['pedri'])

    @property
    def psvrf(self):
        return int(self.data['psvrf'])

    @property
    def psvri(self):
        return int(self.data['psvri'])

    @property
    def unknrf(self):
        return int(self.data['unknrf'])

    @property
    def unknri(self):
        return int(self.data['unknri'])


class Collisions(GenericObjects):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('child_class', Collision)
        super().__init__(*args, **kwargs)

    @staticmethod
    def from_file(filepath):
        data = None
        with open(filepath, 'r') as f:
            data = json.loads(f.read())

        collisions = Collisions()
        for collision_dict in data:
            collisions.append(
                Collision.parse(
                    collision_dict
                )
            )

        return collisions

    @staticmethod
    def from_dir(dirpath):
        collisions = Collisions()
        for filename in glob.iglob(f'{dirpath}/**', recursive=True):
            if os.path.splitext(filename)[-1] != '.json':
                continue
            collisions.extend(
                Collisions.from_file(
                    filename
                )._data
            )

        return collisions

    def filter(self, **kwargs):
        '''
        By whatever props that exist
        '''
        logger.debug('Filtering from %s' % (len(self)))

        filtered = [
            d for d in self if all(
                [
                    getattr(d, attr) == kwargs[attr] for attr in kwargs.keys()
                ]
            )
        ]

        return Collisions(
            data=filtered
        )

    def write(self, write_file):
        with open(write_file, 'w') as f:
            f.write(json.dumps(self.serialize()))

    @staticmethod
    def load_all():
        import road_collisions
        return Collisions.from_dir(
            os.path.join(road_collisions.__path__[0], 'resources')
        )
