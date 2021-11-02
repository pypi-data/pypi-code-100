"""Implements a client definition to interact with the DB."""
import pandas as pd
from sqlalchemy import create_engine

class DBApi():
    """Parent class to conect to a DB using SQLAlchemy."""
    def __init__(self, dialect, host, port, user, password, db):
        self.dialect = dialect
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self._engine = None

    def get_engine(self):
        db_uri = f"{self.dialect}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        if not self._engine:
            self._engine = create_engine(db_uri)
        return self._engine

    def connect(self):
        return self.get_engine().connect()

class DBClient(DBApi):
    """Implements methods to interact with the DB."""
    def __init__(self, dialect, host, port, user, password, db):
        DBApi.__init__(self, dialect, host, port, user, password, db)

    @staticmethod
    def _cursor_columns(cursor):
        if hasattr(cursor, 'keys'):
            return cursor.keys()
        else:
            return [c[0] for c in cursor.description]

    def execute(self, sql, connection=None):
        if connection is None:
            connection = self.connect()
        return connection.execute(sql)

    def insert_from_frame(self, df, table, if_exists='append', index=False, **kwargs):
        connection = self._connect()
        with connection:
            df.to_sql(table, connection, if_exists=if_exists, index=index, **kwargs)

    def to_frame(self, *args, **kwargs):
        cursor = self.execute(*args, **kwargs)
        if not cursor:
            return
        data = cursor.fetchall()
        if data:
            df = pd.DataFrame(data, columns=self._cursor_columns(cursor))
        else:
            df = pd.DataFrame()
        return df
