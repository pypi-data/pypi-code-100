import os
import re
from datetime import datetime, timedelta

from muninn.struct import Struct

PRODUCT_TYPES = {}


def parse_timestamp(timestamp):
    if timestamp in ("00000000", "00000000000000", "00000000T000000", "00-00-0000", "00-00-0000T00:00:00"):
        return datetime.min
    if timestamp in ("99999999", "99999999999999", "99999999T999999", "99-99-9999", "99-99-9999T99:99:99"):
        return datetime.max
    for format_string in ("%Y%m%d", "%Y%m%d%H%M%S", "%Y%m%dT%H%M%S", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(timestamp, format_string)
        except ValueError:
            pass
    return None


class GenericProduct(object):

    def __init__(self, product_type, filename_pattern):
        self.use_enclosing_directory = False
        self.use_hash = False  # For compatibility with muninn versions before 5.1
        self.hash_type = None
        self.product_type = product_type
        self.filename_pattern = filename_pattern

    def parse_filename(self, filename):
        match = re.match(self.filename_pattern, os.path.basename(filename))
        if match:
            return match.groupdict()
        return None

    def identify(self, paths):
        if len(paths) != 1:
            return False
        return re.match(self.filename_pattern, os.path.basename(paths[0])) is not None

    def archive_path(self, properties):
        name_attrs = self.parse_filename(properties.core.physical_name)
        validity_start = properties.core.validity_start
        parts = [self.product_type]
        if 'validity_month' in name_attrs:
            parts.append(validity_start.strftime("%Y"))
        elif 'validity_day' in name_attrs:
            parts.append(validity_start.strftime("%Y"))
            parts.append(validity_start.strftime("%m"))
        elif 'validity_start' in name_attrs:
            parts.append(validity_start.strftime("%Y"))
            parts.append(validity_start.strftime("%m"))
            parts.append(validity_start.strftime("%d"))
        return os.path.join(*parts)

    def get_validity_range(self, name_attrs):
        validity_start = None
        validity_stop = None
        if 'validity_year' in name_attrs:
            validity_start = datetime.strptime(name_attrs['validity_year'], "%Y")
            validity_stop = datetime(validity_start.year + 1, 1, 1)
        elif 'validity_month' in name_attrs:
            validity_start = datetime.strptime(name_attrs['validity_month'], "%Y%m")
            year = validity_start.year + validity_start.month // 12
            month = validity_start.month % 12 + 1
            validity_stop = datetime(year, month, 1)
        elif 'validity_day' in name_attrs:
            validity_start = datetime.strptime(name_attrs['validity_day'], "%Y%m%d")
            validity_stop = validity_start + timedelta(days=1)
        else:
            if 'validity_start' in name_attrs:
                validity_start = parse_timestamp(name_attrs['validity_start'])
            if 'validity_stop' in name_attrs:
                validity_stop = parse_timestamp(name_attrs['validity_stop'])
        return (validity_start, validity_stop)

    def analyze(self, paths):
        inpath = paths[0]
        name_attrs = self.parse_filename(inpath)
        properties = Struct()
        core = properties.core = Struct()
        core.product_name = os.path.splitext(os.path.basename(inpath))[0]
        core.validity_start, core.validity_stop = self.get_validity_range(name_attrs)
        if 'creation_date' in name_attrs:
            core.creation_date = parse_timestamp(name_attrs['creation_date'])
        return properties


def product_types():
    return PRODUCT_TYPES.keys()


def product_type_plugin(product_type):
    return GenericProduct(product_type, PRODUCT_TYPES[product_type])


def init():
    config_file = os.environ.get("MUNINN_GENERIC_PRODUCT_CONFIG", "")
    if config_file:
        with open(config_file, "r") as file:
            for line in file.read().splitlines():
                product_type, pattern = line.split(' ', 1)
                PRODUCT_TYPES[product_type] = pattern


init()
