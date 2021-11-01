"""Implements a function to create a DB stock table."""
import os

from lbpackages.errors.errors import DBError
from lbpackages.models.stocks import Base, create_engine


def create_tables():
    """Creates the 'stock_value' table into the stocks db.

    It uses the data model defined in the stocks module.
    It gets the USER and PASSWORD data to conect to the db from environment.

    Returns
    -------
    str:
        If succesfull, the function returns a success message.
    DBError:
        If the functions fails, it raises a DBError.
    """
    try:
        USER = os.getenv("USER")
        PASS = os.getenv("PASS")

        engine = create_engine(
            f"postgresql://{USER}:{PASS}@stock-data-postgres:5432/stocks"
        )
        Base.metadata.create_all(engine)

        return "Table created succesfully"
    except:
        raise DBError from None
