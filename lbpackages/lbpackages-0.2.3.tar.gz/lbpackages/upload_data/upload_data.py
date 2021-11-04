"""Class to read data from .csv files and upload it into th DB."""
import os

from sqlalchemy.orm import sessionmaker

from lbpackages.exceptions.exceptions import UploadException
from lbpackages.models import dbclient, stocks


class StocksUploaderDB:
    """Uploads .csv files with stocks data to the DB.

    Attributes
    ----------
    dbclient: lbpackges.models.dbclients.DBApi
      handles DB conections
    path: str
      absolute path to the directory of the .csv files with stocks data
    """

    def __init__(self, dbapi: dbclient.DBApi, path: str) -> None:
        """Constructor for the class.

        Parameters
        ----------
        dbclient: lbpackges.models.dbclients.DBApi
          handles DB conections
        path: str
          absolute path to the directory of the .csv files with stocks data
        """
        self.dbapi = dbapi
        self.path = path
        self._session = None

    def _get_session(self) -> None:
        """Creates DB session to interact with DB using SQLAlchemy."""
        self._session = sessionmaker(bind=self.dbapi.get_engine())()

    @staticmethod
    def _read_file(path: str) -> list:
        """Reads and parses the .csv files with stock data.

        Parameters
        ----------
        path: str
          the absolute path to the directory of the .csv files with stocks data
        Yields
        ------
        list
          a list containing each of the fields of the parsed .csv lines
        """
        files = [
            os.path.join(path, file) for file in os.listdir(path) if ".csv" in file
        ]
        for file in files:
            with open(file, "r", encoding="utf-8") as file_handle:
                for row in file_handle:
                    yield row.split(",")

    def _create_model(self, args: list) -> None:
        """Adds stock data to the ORM model using StockValue class.

        Parameters
        ----------
        args: list
          list with arbitrary stock data to add to the model
        """
        self._session.add(stocks.StockValue(*args))

    def upload_db(self) -> None:
        """Reads the files, procesess the information and uploads to DB.

        Raises
        ------
        UploadException
          in case of error or exception while processing or uploading data.
        """
        try:
            if not self._session:
                self._get_session()

            for line in self._read_file(self.path):
                self._create_model(line)

            self._session.commit()
            self._session.close()

            print("Data Upload Complete")
        except:
            raise UploadException from None
