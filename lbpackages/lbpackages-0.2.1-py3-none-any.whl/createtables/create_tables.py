"""Implements a function to create a DB stock table."""
import os

from lbpackages.exceptions.exceptions import DBException
from lbpackages.models.stocks import Base, create_engine


def create_tables():
    """Creates the 'stock_value' table into the stocks db.

    It uses the data model defined in the stocks module.
    It gets the USER and PASSWORD data to conect to the db from environment.

    Returns
    -------

    DBError:
        If the functions fails, it raises a DBException. Otherwise it prints a success message.
    """
    try:
        USER = os.getenv("USER")
        PASS = os.getenv("PASS")

        engine = create_engine(
            f"postgresql://{USER}:{PASS}@stock-data-postgres:5432/stocks"
        )
        Base.metadata.create_all(engine)

        print("Table created succesfully")
    except:
        raise DBException from None
