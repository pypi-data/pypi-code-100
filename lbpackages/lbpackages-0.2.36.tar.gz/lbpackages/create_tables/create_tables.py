"""Implements a function to create a DB stock table."""
import os

from lbpackages.exceptions.exceptions import DBException
from lbpackages.models.dbclient import DBApi
from lbpackages.models.stocks import Base


def create_tables():
    """Creates the 'stock_value' table into the stocks db.

    Uses the data model defined in the stocks module.
    Gets the USER and PASSWORD data to conect to the db from environment.

    Returns
    -------
        DBError:
            If the functions fails, it raises a DBException. Otherwise it prints a success message.
    """
    try:
        db_kwargs = {
            "dialect": "postgresql",
            "user": os.getenv("USER"),
            "password": os.getenv("PASS"),
            "host": "stock-data-postgres",
            "port": 5432,
            "db": "stocks",
        }

        engine = DBApi(**db_kwargs).get_engine()
        Base.metadata.create_all(engine)

        print("Table created succesfully")
    except:
        raise DBException from None
