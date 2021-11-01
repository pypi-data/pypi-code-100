"""Implements errors and exceptions."""


class DBException(Exception):
    """
    Exception raised for errors while creating the stocks table in the DB.

    Attributes
    ----------
        message: str
             explanation of the error
    """

    def __init__(self, message):
        Exception.__init__(self, message)
        self.message = "There was some kind of problem creating the table"
