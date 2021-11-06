import logging
from ciso8601 import parse_datetime
from influxdb_client import InfluxDBClient, Point
from datetime import datetime
from influxdb_client.client.flux_table import FluxTable
from influxdb_client.client.write_api import SYNCHRONOUS
from dms_influx2.buckets import Buckets
from dms_influx2.decorators import runtime
from dms_influx2.delete import Delete
from dms_influx2.organisations import Organizations
from dms_influx2.query import get_flux_query

logger = logging.getLogger(__name__)


class DmsInflux2(InfluxDBClient):
    def __init__(self, url=None, token=None, org=None, enable_gzip=True, timezone_offset: int = None):
        self.query_str = None
        self.predicates = None

        self.time_offset = timezone_offset
        self.time_shift = f'{timezone_offset}h' if timezone_offset is not None else None

        super().__init__(url=url, token=token, org=org, enable_gzip=enable_gzip, timeout=20_000)

    def buckets_api(self) -> Buckets:
        return Buckets(self)

    def organizations_api(self) -> Organizations:
        return Organizations(self)

    def delete_api(self) -> Delete:
        return Delete(self)

    def _list_tag_values(self, bucket, measurement, tag, **kwargs):
        query = f'import "influxdata/influxdb/schema"\n\nschema.measurementTagValues(' \
                f'bucket: "{bucket}",' \
                f'measurement: "{measurement}",' \
                f'tag: "{tag}")'
        self.query_str = query
        tables = self.query_api().query(query)
        data = []
        for table in tables:
            for record in table.records:
                data.append(record.get_value())
        return data

    def _list_distinct_tags(self, bucket, measurement, tag='description', time_range=None):

        if time_range is None:
            time_range = '100y'

        tables = self._get_tables(bucket=bucket,
                                  measurement=measurement,
                                  time_range=time_range,
                                  last=True,
                                  group_columns=[tag],
                                  distinct=True)
        return self._convert_tables_key(tables, key=tag)

    def _perform_query(self, query, params=None):
        query_api = self.query_api()
        self.query_str = query
        return query_api.query(query, params=params)

    def _convert_tables_key(self, tables, key='description'):
        data = []
        for table in tables:
            for record in table.records:
                value = record.values.get(key)
                if value:
                    data.append(value)
        return data

    @runtime
    def _extract_tables(self, tables: FluxTable, values_name='values') -> list:

        data = []
        for table in tables:
            labels = [i.label for i in table.columns]
            try:
                get_columns = list(filter(lambda x: (x[0] != '_' and x not in ['table', 'result']), labels))
            except Exception as e:
                # TODO try to resolve this error
                for record in table.records:
                    # print(record)
                    logger.error(record)
                    # for i in record:
                    #     print(i)
                continue
            _data = {}
            _values = []
            for record in table.records:
                if not _data:
                    for col in get_columns:
                        _data[col] = record.values.get(col, None)
                # ts = str(record.get_time() + timedelta(hours=2)).split('+')[0]
                ts = str(record.get_time()).split('+')[0]
                _values.append((ts, record.get_value()))
            data.append({**_data, values_name: _values})
        return data

    @runtime
    def _get_tables(self, **kwargs) -> list:
        """Return tables based on flux query"""
        query = get_flux_query(**kwargs, time_shift=self.time_shift, time_offset=self.time_offset)
        return self._perform_query(query=query)

    def list_measurements(self, bucket) -> list:
        """Return list of measurements inside a bucket"""

        query = f'import "influxdata/influxdb/schema"\n\nschema.measurements(bucket: "{bucket}")'
        self.query_str = query
        tables = self.query_api().query(query)
        data = []
        for table in tables:
            for record in table.records:
                data.append(record.get_value())
        return data

    def list_device_ids(self, bucket, measurement=None) -> list:
        """Return list of distinct device_ids (tag=device_id)"""

        return self._list_distinct_tags(bucket=bucket, measurement=measurement, tag='device_id')

    def list_descriptions(self, bucket, measurement=None, time_range=None) -> list:
        """Return list of distinct descriptions"""

        if time_range is None:
            time_range = '100y'

        query = f'''import "influxdata/influxdb/schema"\n\n
        schema.tagValues(
          bucket: "{bucket}",
          tag: "description",
          predicate: (r) => r._measurement == "{measurement}",
          start: -{time_range}
        )'''

        tables = self._perform_query(query=query)
        data = []
        for table in tables:
            for record in table.records:
                data.append(record.get_value())
        return data

    def get_values_count_combined(self, bucket, measurement=None, device_id=None, description=None,
                                  time_range=None, time_from=None, time_to=None,
                                  aggregate_window=None, aggregate_func=None) -> int:

        if time_range is None:
            time_range = '100y'

        local_vars = locals()
        local_vars.pop('self')
        local_vars['count'] = True
        local_vars['keep_only_columns'] = ["_value"]

        tables = self._get_tables(**local_vars)

        values_len = None
        for table in tables:
            for record in table.records:
                values_len = record.get_value()
        return values_len

    def get_values_count(self, bucket, measurement=None, device_id=None, description=None,
                         time_range=None, time_from=None, time_to=None,
                         aggregate_window=None, aggregate_func=None, window_count=None) -> dict:

        if time_range is None:
            time_range = '100y'

        local_vars = locals()
        local_vars.pop('self')
        local_vars['count'] = True
        local_vars['group_columns'] = ["device_id"]
        local_vars['keep_only_columns'] = ["_value", "device_id"]

        tables = self._get_tables(**local_vars)

        data = {}
        for table in tables:
            for record in table.records:
                data[record.values.get("device_id")] = record.get_value()
        return data

    def get_metadata(self, bucket, measurement=None, device_id=None, description=None,
                     time_range=None, time_from=None, time_to=None) -> list:
        """Get len and last value"""

        local_vars = locals()
        local_vars.pop('self')

        data = self.get_last_values(**local_vars)
        data_len = self.get_values_count(**local_vars)

        for item in data:
            device_id = item['device_id']
            if device_id in data_len:
                item['values_count'] = data_len[device_id]
            else:
                item['values_count'] = 0

        return data

    def get_last_values(self, bucket, measurement=None, device_id=None, description=None,
                        time_range=None, time_from=None, time_to=None) -> list:
        """Get last values"""

        local_vars = locals()
        local_vars.pop('self')
        local_vars['time_range'] = '100y'
        local_vars['last'] = True
        local_vars['group_columns'] = ["device_id"]

        tables = self._get_tables(**local_vars)
        # print(tables)

        return self._extract_tables(tables, values_name='last_value')

    def get_values_from_device_id(self, bucket, measurement, device_id, description=None,
                                  time_range=None, time_from=None, time_to=None,
                                  aggregate_window=None, aggregate_func=None,
                                  sort='desc', limit=None, window_count=None):

        if measurement is None:
            raise ValueError("Invalid value for `measurement`, must not be `None`")

        if device_id is None:
            raise ValueError("Invalid value for `device_id`, must not be `None`")

        local_vars = locals()
        local_vars.pop('self')
        local_vars['drop_columns'] = ["unit"]
        local_vars['keep_only_columns'] = ["_value", "_time"]

        tables = self._get_tables(**local_vars)

        values = self._extract_tables(tables)

        return values[0]['values'] if values else None

    def get_data_from_device_id(self, bucket, measurement, device_id, description=None,
                                time_range=None, time_from=None, time_to=None,
                                aggregate_window=None, aggregate_func=None,
                                sort='desc', limit=None, window_count=None) -> dict:

        if measurement is None:
            raise ValueError("Invalid value for `measurement`, must not be `None`")

        if device_id is None:
            raise ValueError("Invalid value for `device_id`, must not be `None`")

        local_vars = locals()
        local_vars.pop('self')

        data = self.get_last_values(bucket=bucket, measurement=measurement, device_id=device_id)
        if data:
            data = data[0]
            data['values'] = self.get_values_from_device_id(**local_vars)
        else:
            data = {}
        return data

    def save_data(self, bucket, data, org=None):
        """ Save data to database

        sample_data = [{
            measurement: <str>,
            device_id: <str> (required),
            device: <str>,
            channel: <str>,
            description: <str>,
            unit: <str> (required),
            values: [[ <utctime>, value], ...] (required)
        }]

        :param org:
        :param bucket:
        :param data: Data to save
        """

        if type(data) == dict:
            data = [data]

        if org is None:
            org = self.org

        points = []
        for item in data:
            if not item['device_id']:
                raise ValueError('Device id must be supplied')
            device_id = item['device_id']
            measurement = item.get('measurement', device_id.split('.')[0])
            device = item.get('device', measurement)
            channel = item.get('channel', device_id.split('.')[1])
            description = item.get('description', None)
            unit = item.get('unit', '')
            for point in item['values']:
                if type(point) not in [list, tuple]:
                    raise ValueError('Point must be `tuple` or `list` example: (2021-01-01 00:00:00, 1)')

                ts = point[0]
                value = float(point[1])

                if type(ts) == datetime:
                    ts = str(ts)

                # Check if string is a valid timestamp
                try:
                    ts = parse_datetime(ts)
                except Exception:
                    raise ValueError('Time is not a valid string')
                #
                # if not utc:
                #     # Convert timestamp to UTC
                #     ts = self.tz.localize(ts)
                #     ts = ts.astimezone(pytz.utc)

                point = Point(measurement) \
                    .tag("device_id", device_id) \
                    .tag("device", device) \
                    .tag("channel", channel) \
                    .tag("unit", unit) \
                    .field("value", value) \
                    .time(time=ts)
                if description is not None:
                    point.tag('description', description)
                points.append(point)

        write_api = self.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=bucket, org=org, record=points)
        write_api.close()

    def _copy_data(self, bucket_from, bucket_to, org_to=None, measurement=None, device_id=None, description=None,
                   time_range=None, time_from=None, time_to=None, aggregate_window=None, aggregate_func=None,
                   sort='desc', limit=None):
        """Copy data from one bucket to another bucket"""

        if org_to is None:
            org_to = self.org

        if time_range is None:
            time_range = '100y'

        query = get_flux_query(bucket=bucket_from, bucket_to=bucket_to, org_to=org_to, measurement=measurement,
                               device_id=device_id, description=description,
                               time_range=time_range, time_from=time_from, time_to=time_to,
                               aggregate_window=aggregate_window,
                               aggregate_func=aggregate_func,
                               sort=None, limit=limit)
        self._perform_query(query)

    def move_data_to_trash(self, bucket, measurement, bucket_trash=None, device_id=None, description=None,
                           time_range=None, time_from=None, time_to=None, delete_afterwords=True):

        if measurement is None:
            raise ValueError("Invalid value for `measurement`, must not be `None`")

        if bucket_trash is None:
            bucket_trash = f'{bucket}_trash_{datetime.now().year}'

        bucket_api = self.buckets_api()
        if not bucket_api.bucket_exists(bucket_name=bucket_trash):
            org = self.organizations_api().get_organization(org_name=self.org)
            bucket_api.create_bucket(bucket_name=bucket_trash, org=org,
                                     description=f"Trash bucket for year {datetime.now().year}")

        self._copy_data(bucket_from=bucket, bucket_to=bucket_trash, measurement=measurement, device_id=device_id,
                        description=description, time_range=time_range, time_from=time_from, time_to=time_to)

        if delete_afterwords:
            device_ids = [device_id] if device_id is not None else []
            descriptions = [description] if description is not None else []
            self.delete_api().delete_data(bucket=bucket, measurements=[measurement], device_ids=device_ids,
                                          descriptions=descriptions, org=self.org,
                                          time_from=time_from, time_to=time_to)
