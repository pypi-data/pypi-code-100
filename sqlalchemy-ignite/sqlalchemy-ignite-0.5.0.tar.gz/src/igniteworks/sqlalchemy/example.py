# Register SQLAlchemy dialect
import re
import sys

from sqlalchemy.dialects import registry
# Test engine and table
from sqlalchemy.engine import create_engine


def main():
    """
    Register IgniteDialect class in module 'dialect'
    as SQLAlchemy dialect

    registry.register("igniteworks", "igniteworks.sqlalchemy.dialect", "dialect")

    """
    registry.register("igniteworks", "dialect", "dialect")

    """
    Sample how to assign connection parameters to Apache
    Ignite connection
    """
    connect_args = {
        'servers': '127.0.0.1:10800',
        'timeout': 20.0
    }

    engine = create_engine('igniteworks://', connect_args=connect_args)
    connection = engine.connect()

    sql = "SELECT * FROM \"SQL_PUBLIC_CITY\".\"City\""
    # sql = "GET KEYS FROM CITY"
    result = connection.execute(sql)
    # print(result)
    for row in result.fetchall():
        print(row)


if __name__ == '__main__':
    sys.exit(main())
