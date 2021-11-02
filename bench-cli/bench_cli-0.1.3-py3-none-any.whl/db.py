import pandas as pd
import psycopg2 as pc
import time
from io import StringIO
from pathlib import Path

sql = Path("bench/sql/")


class Database:
    def __init__(self, host, port, dbname, user, password, verbose=False):
        """
        Class for PostgreSQL database session.

        Parameters
        ----------
        host : str
            PostgreSQL database host address. (Defaults to UNIX socket if not provided).
        port : str
            PostgreSQL database connection port number. (Defaults to 5342 if not provided).
        dbname : str
            PostgreSQL database name.
        user: str
            PostgreSQL database username used to authenticate.
        password : str
            PostgreSQL database password used to authenticate.
        verbose : bool
            Display verbose output for the pipeline. Defaults to False.

        Attributes
        ----------
        host : str
            PostgreSQL database host address. (Defaults to UNIX socket if not provided).
        port : str
            PostgreSQL database connection port number. (Defaults to 5342 if not provided).
        dbname : str
            PostgreSQL database name.
        user: str
            PostgreSQL database username used to authenticate.
        password : str
            PostgreSQL database password used to authenticate.
        c: psycopg2.connection
            Handles the connection to a PostgreSQL database instance. It encapsulates a database session.
        cur : psycopg2.cursor()
            Allows Python to execute PostgreSQL commands in a database session.

        """
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.c = self.c()
        if self.c is not None:
            self.cur = self.cur()
        else:
            self.cur = None
        self.verbose = verbose

    def c(self):
        """PostgreSQL database connection.

        Returns
        -------
        psycopg2.connection
            Handles the connection to a PostgreSQL database instance. It encapsulates a database session.

        """
        retries = 3
        for n in range(retries):
            try:
                c = pc.connect(
                    host=self.host,
                    port=self.port,
                    dbname=self.dbname,
                    user=self.user,
                    password=self.password,
                )
                return c
            except Exception as error:
                print(f"Could not establish a connection with database: {self.dbname}")
                print("Reconnecting to the database in 2 seconds...")
                time.sleep(2)
        raise Exception(f"Failed to connect to the database within {retries} tries.")

    def cur(self):
        """PostgreSQL database cursor.

        Returns
        -------
        psycopg2.cursor()
            Allows Python to execute PostgreSQL commands in a database session.

        """
        try:
            cur = self.c.cursor()
        except pc.OperationalError as e:
            print(f"Could not establish a cursor for database: {self.dbname}")
            raise

        return cur

    def init(self):
        """Creates main and temporary tables in PostgreSQL database.
        Executes "create_tables.sql", "create_temp_tables.sql" queries in PostgreSQL database.

        Returns
        -------
        psycopg2.commit()
            Commits pending transactions to the database.

        Raises
        -------
        Exception
            psycopg2 error has occured.

        """
        cursor = self.cur

        try:
            tables = open(sql / "create_tables.sql", "r")
            temp_tables = open(sql / "create_temp_tables.sql", "r")
            cursor.execute(tables.read())
            cursor.execute(temp_tables.read())
            self.c.commit()
            if self.verbose == True:
                print(f"Tables have been created in {self.dbname}")

        except (Exception, pc.DatabaseError) as error:
            print("Error: %s" % error)

    def load(self, symbol, dfs):
        """Bulk copies API data to temp tables then bulk inserts to main tables.
        Executes "copy.sql", "find_columns.sql", "merge_stock.sql", "merge.sql", "update_fk.sql" queries in the PostgreSQL database.

        Parameters
        ----------
        symbol : str
            Ticker for stock
        dfs : tuple(pd.DataFrame, pd.DataFrame, pd.DataFrame)
            Tuple of pd.DataFrames to be bulk inserted for the specified symbol.

        Returns
        -------
        psycopg2.commit()
            Commits pending transactions to the database.

        Raises
        -------
        Exception
            psycopg2 error has occured.

        """
        cursor = self.cur

        def wrap(string):
            wrapped = f"'{string}'"
            return wrapped

        symbol_wrap = wrap(symbol)

        # define tablenames
        tablenames = ["stock", "fundamentals", "metrics"]

        for (df, table) in zip(dfs, tablenames):

            if table == "stock":
                if self.verbose == True:
                    print(f"Handling table {table} for {symbol}")

                # Read csv to buffer
                buffer = StringIO()
                df.to_csv(buffer, sep=",", index=False, header=False)
                buffer.seek(0)

                # Find table column names
                tablename = "'{}'".format(table)
                column_query = open(sql / "find_columns.sql", "r")
                cursor.execute(column_query.read().format(tablename))
                query_result = cursor.fetchall()
                queried_columns = [i[0] for i in query_result]
                columns = ",".join(queried_columns)

                try:
                    # copy to temp table
                    if self.verbose == True:
                        print(f"Copying data to temp table {table} for {symbol}")
                    copy_query = open(sql / "copy.sql", "r")
                    temp_table = "t" + table
                    cursor.copy_expert(
                        copy_query.read().format(temp_table, columns), buffer
                    )

                    # merge temp table to prod table
                    if self.verbose == True:
                        print(f"Now upserting to {table} for {symbol}")
                    merge_query = open(sql / "merge_stock.sql", "r")
                    cursor.execute(merge_query.read().format(columns, symbol_wrap))

                    self.c.commit()

                except (Exception, pc.DatabaseError) as error:
                    print("Error: %s" % error)
                    self.c.rollback()
                    return 1
                buffer.truncate(0)

            else:
                if self.verbose == True:
                    print(f"Handling table {table} for {symbol}")
                # Read csv to buffer
                buffer = StringIO()
                df.to_csv(buffer, sep=",", index=False, header=False)
                buffer.seek(0)

                # Find table column names
                tablename = "'{}'".format(table)
                column_query = open(sql / "find_columns.sql", "r")
                cursor.execute(column_query.read().format(tablename))
                query_result = cursor.fetchall()
                queried_columns = [i[0] for i in query_result]
                columns = ",".join(queried_columns)

                # Copy DataFrame to table
                try:
                    # copy to temp table
                    if self.verbose == True:
                        print(f"Copying data to temp table {table} for {symbol}")
                    copy_query = open(sql / "copy.sql", "r")
                    temp_table = "t" + table
                    cursor.copy_expert(
                        copy_query.read().format(temp_table, columns), buffer
                    )

                    # merge temp table to prod table
                    if self.verbose == True:
                        print(f"Now upserting to {table} for {symbol}")
                    merge_query = open(sql / "merge.sql", "r")
                    cursor.execute(
                        merge_query.read().format(columns, table, temp_table)
                    )

                    # update foreign keys
                    update_fk = open(sql / "update_fk.sql", "r")
                    fk_update = update_fk.read()
                    cursor.execute(fk_update.format(table, symbol_wrap))

                    self.c.commit()

                except (Exception, pc.DatabaseError) as error:
                    print("Error: %s" % error)
                    self.c.rollback()
                    return 1
                buffer.truncate(0)
        if self.verbose == True:
            print(f"Bulk upload of {symbol} finished!")
