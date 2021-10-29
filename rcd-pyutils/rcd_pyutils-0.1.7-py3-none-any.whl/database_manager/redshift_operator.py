import os
import numpy as np
import pandas as pd
from typing import Any, List, Dict, Tuple, Set
from sqlalchemy import create_engine, inspect
from sqlalchemy import Table, MetaData, Column, Integer, SmallInteger, BigInteger, String, Float, Boolean, \
    Date
from rcd_pyutils.database_manager.s3_operator import S3Operator


def send_to_redshift(database: str, schema: str, table: str, df: pd.DataFrame, **kwargs: Any) -> None:
    """
        Function send_to_redshift.
        Use this function to send data to s3 bucket and redshift(using copy).

        Args:
            database (str): The name of database in redshift.
            schema(str): The name of schema in redshift&s3.
            table(str): The name of the table to save.
            df(pd.DataFrame): The dataframe to send.

        Kwargs:
            check(bool): False by default. If True, check the column type and length is consistent as current table in redshift.
            drop(bool): (Avoid to use!) False by default. If True, drop the datatable which exists already.
            debug(bool): False by default. If True, print debug information.

            bucket(str): Datamart bucket by default. S3 Bucket name to save the data.

        Examples:
            >>> from rcd_pyutils import database_manager
            >>> database_manager.send_to_redshift(database="my_database", schema="my_schema", table="my_table", df=my_dataframe)
    """
    so = S3Operator()
    so.bucket = kwargs.get("bucket", os.environ.get("S3_BUCKET_DATAMART"))
    so.send_to_s3_obj(df=df, s3_file_path=os.path.join(schema, f"{table}.csv"), sep="|")

    ro = RedshiftOperator(database=database, debug=kwargs.get('debug', False))
    ro.schema = schema
    ro.table = table
    if kwargs.get("drop") is True:
        ro.drop_table()
    ro.process_table(bucket=kwargs.get("bucket", os.environ.get("S3_BUCKET_DATAMART")), df=df, sep="|",
                     check=kwargs.get("check", False))

    df_sent = ro.read_from_redshift()
    if df_sent.shape != df.shape:
        raise ValueError("❌Original table and the table from redshift doesn't have the same shape.")


def read_from_redshift(database: str, method: str, **kwargs) -> pd.DataFrame:
    """
        Function read_from_redshift.
        Use this function to read data from redshift.

        Args:
            database(str): The name of database in redshift.
            method(str): Default "auto", retreive data with limit and select, or "sql" retreive data with sql query.
        Kwargs:
            schema(str): The name of schema in redshift.
            table(str): The name of the table in redshift.
            limit(int): The line limit to read. Default None.
            select(str): The content to select. Default "*".

            debug(bool): False by default. If True, print debug information.

        Examples:
            >>> from rcd_pyutils import database_manager
            >>> database_manager.read_from_redshift(database="my_database", method="auto", schema="my_schema", table="my_table")
            >>> database_manager.read_from_redshift(database="my_database", method="sql", sql_query='SELECT * FROM my_schema.my_table')
    """
    ro = RedshiftOperator(database=database, debug=kwargs.get('debug', False))
    ro.schema = kwargs.get("schema")
    ro.table = kwargs.get("table")
    if method == "auto":
        df_from_redshift = ro.read_from_redshift(limit=kwargs.get("limit", None), select=kwargs.get("select", "*"))
    elif method == "sql":
        df_from_redshift = ro.read_sql_from_redshift(sql_query=kwargs.get("sql_query", None))
    else:
        raise ValueError(f"Unrecognized method: {method}")
    return df_from_redshift


class RedshiftOperator:
    """
    RedshiftOperator, build redshift connection, read data from or send data to redshift.

    Args:
        database (str): The database for connection.

    Examples:
        >>> from rcd_pyutils import database_manager
        >>> ro = database_manager.RedshiftOperator()
        >>> ro.read_from_redshift(schema="my_schema", table="my_table", limit=10)
    """

    def __init__(self, database: str = os.environ.get("REDSHIFT_DB"), debug: bool = False) -> None:
        self.redshift_user = os.environ.get("REDSHIFT_USER")
        self.redshift_password = os.environ.get("REDSHIFT_PASSWORD")
        self.redshift_host = os.environ.get("REDSHIFT_HOST")
        self.redshift_database = database
        if database is None:
            raise ValueError(f"❌Input database not defined in .env")
        self.engine = create_engine(
            f"redshift+psycopg2://{self.redshift_user}:{self.redshift_password}@{self.redshift_host}:5439/{self.redshift_database}",
            echo=debug)
        self.conn = self.engine.connect()
        self._schema = None
        self._table = None

        # Session = sessionmaker(bind=self.engine)
        # self.session = Session()

    """
        property
    """

    @property
    def schema(self) -> str:
        return self._schema

    @schema.setter
    def schema(self, schema: str) -> None:
        print(f"☑️Setting schema to {schema}")
        self._schema = schema

    @property
    def table(self) -> str:
        return self._table

    @table.setter
    def table(self, table: str) -> None:
        print(f"☑️Setting table to {table}")
        self._table = table

    """
        read method
    """

    def read_from_redshift(self, limit: bool = None, select: str = "*") -> pd.DataFrame:
        sql_limit = limit if limit else "NULL"
        query = f"SELECT {select} FROM {self._schema}.{self._table} LIMIT {sql_limit}"
        df_result = pd.read_sql_query(query, self.engine)
        return df_result

    def read_sql_from_redshift(self, sql_query: str) -> pd.DataFrame:
        df_result = pd.read_sql_query(sql_query, self.engine)
        return df_result

    """
        static method for calculating data type and length
    """

    @staticmethod
    def get_char_length(string: str) -> int:
        return len(str(string).encode('utf8'))

    @staticmethod
    def shift_bit_length(x: int) -> int:
        return 1 << (x - 1).bit_length() if x != 1 else 2

    @staticmethod
    def get_int_type(integer: int) -> int:
        if integer in range(-32768, 32767):
            int_type = SmallInteger
        elif integer in range(-2147483648, 2147483647):
            int_type = Integer
        elif integer in range(-9223372036854775808, 9223372036854775807):
            int_type = BigInteger
        else:
            raise ValueError(f"❌Unrecognized integer type: {integer}")
        return int_type

    @staticmethod
    def detect_type(df: pd.DataFrame) -> Dict:
        dict_type = dict()
        for col in df.columns:
            # check for int without NA and with NA
            try:
                is_int = np.issubdtype(df[col].dtype, int)
            except TypeError:
                is_int = np.issubdtype(type(df[col].dtype), pd.Int64Dtype)

            if is_int:
                dict_type[col] = RedshiftOperator.get_int_type(df[col].abs().max())
            elif np.issubdtype(df[col].dtype, float):
                dict_type[col] = Float
            elif np.issubdtype(df[col].dtype, np.datetime64):
                dict_type[col] = Date
            elif np.issubdtype(df[col].dtype, np.bool_):
                dict_type[col] = Boolean
            elif np.issubdtype(df[col].dtype, np.string_) | np.issubdtype(df[col].dtype, np.object_):
                char_max_len = df[col].map(RedshiftOperator.get_char_length).max()
                dict_type[col] = String(RedshiftOperator.shift_bit_length(int(char_max_len)))
            else:
                raise ValueError(f"❌Unrecognized type: {df[col].dtype}")
        return dict_type

    """
         table oriented method
    """

    def detect_table(self) -> bool:
        inspect_engine = inspect(self.engine)
        table_exists = inspect_engine.has_table(schema=self._schema, table_name=self._table)
        return table_exists

    def detect_table_structure(self, df: pd.DataFrame) -> List:
        print("🧮Calculating the best AWS type and length for each column...")
        lst_type_pair = RedshiftOperator.detect_type(df).items()
        # print(inspect_engine.get_table_names(schema=schema))
        # print("rcd_pyutils start")
        # rcd_pyutils = inspect_engine.get_columns(table_name=table_name, schema=schema)
        # print("rcd_pyutils end")
        return lst_type_pair

    def clean_table(self) -> None:
        self.conn.execute(f"TRUNCATE TABLE {self._schema}.{self._table}")

    def drop_table(self) -> None:
        metadata = MetaData()
        datatable = Table(self._table, metadata, schema=self._schema)
        datatable.drop(self.engine, checkfirst=False)

    def create_table(self, lst_type: List) -> None:
        print(f"🔁{self._schema}.{self._table} structure doesn't exist, creating...")
        metadata = MetaData()
        query_tuple = tuple(Column(column_name, sql_type) for column_name, sql_type in lst_type)
        datatable = Table(
            self._table, metadata,
            *query_tuple,
            schema=self._schema
        )
        datatable.create(self.engine, checkfirst=True)
        print(f"🏗Table Structure Created!")

    def get_current_structure(self) -> List:
        print(f"❗️{self._schema}.{self._table} structure exists, retrieving current structure...")
        get_current_len_query = f"""
        SELECT table_schema, table_name, column_name, data_type, character_maximum_length
        FROM information_schema.columns
        WHERE table_schema = '{self._schema}'
        AND table_name = '{self._table}'
        AND data_type = 'character varying'
        ORDER BY table_name;
        """
        df_current_structure = self.conn.execute(get_current_len_query)
        lst_current_structure = [(row[2], row[4]) for row in df_current_structure]
        return lst_current_structure

    def check_structure_consistency(self, df: pd.DataFrame) -> List:
        # check varchar type
        lst_current_structure = self.get_current_structure()
        lst_new_structure = [(type_pair[0], type_pair[1].length) for type_pair in self.detect_table_structure(df) if
                             isinstance(type_pair[1], String)]
        new_varchar = set(lst_new_structure) - set(lst_current_structure)
        return new_varchar

    def update_structure(self, iter_new_structure: Set) -> None:
        print(f"⚠️There are some columns need update: {iter_new_structure}")
        self.clean_table()
        for column, new_len in iter_new_structure:
            update_query = f"""
            ALTER TABLE "{self._schema}"."{self._table}"
            ALTER COLUMN "{column}" TYPE varchar({new_len});
            """
            self.conn.execution_options(isolation_level="AUTOCOMMIT").execute(update_query)
        print(f"✨Table Structure Updated!")

    def copy_from_s3(self, bucket: str, prefix: str, s3_table: str, sep: str, redshift_schema: str, redshift_table: str) -> None:
        s3_file_path = os.path.join(bucket, prefix, f"{s3_table}.csv")
        query = f"""
        COPY {redshift_schema}.{redshift_table} 
        FROM 's3://{s3_file_path}' 
        WITH CREDENTIALS 'aws_access_key_id={os.environ.get('AWS_ACCESS_KEY_ID')};aws_secret_access_key={os.environ.get('AWS_SECRET_ACCESS_KEY')}'
        REGION '{os.environ.get('AWS_DEFAULT_REGION')}'
        DELIMITER '{sep}'
        REMOVEQUOTES
        IGNOREHEADER 1
        """
        result = self.conn.execution_options(autocommit=True).execute(query)
        result.close()
        print(f"🥳Table is copied to redshift from S3.")

    """
      summary method
    """

    def process_table(self, bucket: str, df: pd.DataFrame, sep: str, check: bool = False) -> None:
        table_exists = self.detect_table()
        if table_exists and (check is False):
            pass
        elif table_exists and (check is True):
            iter_new_structure = self.check_structure_consistency(df=df)
            if len(iter_new_structure) > 0:
                self.update_structure(iter_new_structure=iter_new_structure)
            else:
                print(f"🥳Table Structure is consistent!")
        else:
            lst_type = self.detect_table_structure(df=df)
            self.create_table(lst_type=lst_type)
        self.clean_table()
        self.copy_from_s3(bucket=bucket, prefix=self._schema, s3_table=self._table, sep=sep, redshift_schema=self._schema,
                          redshift_table=self._table)
