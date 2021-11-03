import sys

from pyignite import Client


def main():
    print('Start test...')

    client = Client()
    client.connect('127.0.0.1', 10800)

    CITY_CREATE_TABLE_QUERY = '''CREATE TABLE City (
        ID INT(11),
        Name CHAR(35),
        CountryCode CHAR(3),
        District CHAR(20),
        Population INT(11),
        PRIMARY KEY (ID, CountryCode)
    ) WITH "CACHE_NAME=COUNTRY"'''

    client.sql(CITY_CREATE_TABLE_QUERY)

    CITY_INSERT_QUERY = '''INSERT INTO City(
        ID, Name, CountryCode, District, Population
    ) VALUES (?, ?, ?, ?, ?)'''

    CITY_DATA = [
        [3793, 'New York', 'USA', 'New York', 8008278],
        [3794, 'Los Angeles', 'USA', 'California', 3694820],
        [3795, 'Chicago', 'USA', 'Illinois', 2896016],
        [3796, 'Houston', 'USA', 'Texas', 1953631],
        [3797, 'Philadelphia', 'USA', 'Pennsylvania', 1517550],
        [3798, 'Phoenix', 'USA', 'Arizona', 1321045],
        [3799, 'San Diego', 'USA', 'California', 1223400],
        [3800, 'Dallas', 'USA', 'Texas', 1188580],
    ]

    for row in CITY_DATA:
        client.sql(CITY_INSERT_QUERY, query_args=row)

    CITY_SELECT_QUERY = "SELECT * FROM City"

    result = client.sql(CITY_SELECT_QUERY, include_field_names=True)
    field_names = next(result)

    rows = []
    for row in result:
        columns = []
        for field_name, field_value in zip(field_names, row):
            column = {field_name: field_value}
            columns.append(column)

        rows.append(row)

    for row in rows:
        print(row)

    caches = client.get_cache_names()
    print(caches)

    for cacheName in caches:
        cache = client.get_cache(cacheName)
        cfg = cache.settings
        if 200 in cfg:
            print(cfg.get(200))


if __name__ == '__main__':
    sys.exit(main())
