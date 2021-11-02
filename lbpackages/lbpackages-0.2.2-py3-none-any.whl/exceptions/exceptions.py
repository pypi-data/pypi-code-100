"""Implements errors and exceptions."""


class DBException(Exception):
    """
    Exception raised for errors while creating the stocks table in the DB.

    Atributes
    ----------
        message: str
             explanation of the error
    """
    def __init__(self) -> None:
        """Constructor of the class."""

        message = "There was some kind of problem creating the table"
        Exception.__init__(self, message)
