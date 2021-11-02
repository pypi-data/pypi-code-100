from bench.stock import Stock
from bench.db import Database
from alive_progress import alive_bar
import sys
import os


class Pipeline:
    def __init__(
        self,
        period,
        num_periods,
        verbose=False,
    ):
        """
        Class for executing the Bench pipeline.

        Parameters
        ----------
        host : str
            PostgreSQL database host address. (Defaults to UNIX socket if not provided).
        port : str
            PostgreSQL database connection port number. (Defaults to 5342 if not provided).
        user: str
            PostgreSQL database username used to authenticate.
        dbname : str
            PostgreSQL database name.
        password : str
            PostgreSQL database password used to authenticate.
        version : str
            API version. Can be "stable" or "test".
        token : str
            API token for IEX Cloud.
        period : str
            Period intervals for financial data. Can be "annual" or "quarterly"
        num_periods : int
            The number of historical periods.
        watchlist : list
            A list of tickers. eg. ['FB', 'AAPL', 'NFLX', 'MSFT']
        verbose : bool
            Display verbose output for the pipeline. Defaults to False.

        """
        self.host = os.getenv("BENCH_DB_HOST")
        self.port = os.getenv("BENCH_DB_PORT")
        self.user = os.getenv("BENCH_DB_USER")
        self.dbname = os.getenv("BENCH_DB_NAME")
        self.password = os.getenv("BENCH_DB_PASSWORD")
        self.version = os.getenv("BENCH_IEX_VERSION")
        if self.version == "test":
            self.token = os.getenv("BENCH_IEX_TEST_TOKEN")
        else:
            self.token = os.getenv("BENCH_IEX_TOKEN")
        self.period = period
        self.num_periods = num_periods
        self.watchlist = (os.getenv("BENCH_WATCHLIST")).split(",")
        self.verbose = verbose

    def process(self):
        """Initializes the Stock class for each ticker in the watchlist and stores data to a dict of DataFrames.

        Returns
        -------
        Dictionary of DataFrames
            Dictionary with company, fundamental, and metrics data for each ticker.

        """
        frames = {}
        print("Downloading data...")
        with alive_bar(len(self.watchlist)) as bar:
            for ticker in self.watchlist:
                try:
                    s = Stock(
                        ticker=ticker,
                        token=self.token,
                        version=self.version,
                        period=self.period,
                        num_periods=self.num_periods,
                    )
                    frames[ticker] = (s.company, s.fundamentals, s.metrics)
                    bar()
                except Exception as e:
                    print(
                        "Error encountered while processing ticker: {}".format(ticker)
                    )
                    pass

        empty = bool(frames.values())

        if empty == False:
            print("Failed to fetch stocks in the watchlist")
            sys.exit(1)

        return frames

    def load(self, db, frames):
        """Loads the dictionary of DataFrames to the PostgreSQL database."""
        stocks = [*frames]
        print("Loading stock data to the database...")
        with alive_bar(len(stocks)) as bar:
            for stock in stocks:
                try:
                    bar()
                    dfs = frames[stock]
                    db.load(stock, dfs)
                    if self.verbose == True:
                        print("done loading {stock}".format(stock))
                except Exception as e:
                    pass

    def run(self):
        """Runs the pipeline"""
        dataframe_dict = self.process()

        try:
            db = Database(
                host=self.host,
                port=self.port,
                user=self.user,
                dbname=self.dbname,
                password=self.password,
                verbose=self.verbose,
            )

            db.init()

            self.load(db, dataframe_dict)

        except Exception as error:
            print(error)
            sys.exit()

        finally:
            if db.c is not None:
                db.c.close()
