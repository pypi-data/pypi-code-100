"""Class to download stock data from the API and store it."""
import os

import pandas as pd
import requests

from lbpackages.exceptions.exceptions import (
    StocksAvailabilityException,
    StocksApiException,
    StocksProcessingException,
)


class StocksApiClient:
    """Downloads and saves stock information.

    Attributes
    ---------
      api_key: str
        api key to connect to the service
    """

    def __init__(self, api_key: str) -> None:
        """Constructor of the class.

        Parameters
        ----------
          api_key: str
            api key to connect to the service
        """
        self.api_key = api_key

    def _download_data(self, ticker: str, date: str) -> pd.DataFrame:
        """Downloads the ticker data for the given date.

        Parameters
        ----------
          ticker: str
            the stock to download information
          date: str
            the date to download in the format YYYY-MM-DD
        Returns
        -------
          pd.DataFrame
            DataFrame with the stock data for the given date if successful
        Raises
        ------
          StocksApiException
            in case of failure getting the information from the API
        """
        try:
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&datatype=csv&apikey={self.api_key}"
            r = requests.get(url)

            filtered_lines = [
                line[:-1]
                for line in [
                    [ticker] + line.decode("utf-8").split(",")
                    for line in r.iter_lines()
                ]
                if line[1] == date
            ]

            return pd.DataFrame(filtered_lines)
        except:
            raise StocksApiException from None

    def process_stock_data(self, stocks: list, date: str, path: str) -> None:
        """Downloads the stocks information and stores it in the given path.

        Parameters
        ----------
          stocks: list of str
            list of comma separated tickers to download
          date: str
            the date to download in the format YYYY-MM-DD. Discards all others.
          path: str
            absolute path to the directory where data is to be stored
        Returns
        -------
          str
            success message if procesing succeds
        Raises
        ------
          StocksProcessingException
            in case of failure processing the data

        """
        try:
            stocks_df = []
            for ticker in stocks:
                stocks_df.append(self._download_data(ticker, date))
            fn = os.path.join(path, date + "_stocks_data.csv")
            stocks_df = pd.concat(stocks_df)
            if len(stocks_df) == 0:
              raise StocksAvailabilityException from None
            stocks_df.to_csv(fn, index=False, header=False)
            print(f"Data Processed with Success. File saved : {fn}")
        except Exception as e:
            print(e)
            #raise StocksProcessingException from None
