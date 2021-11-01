from IPython.core.display import display
from pyspark.sql import DataFrame

try:
    from pysparkbundle.dataframe.DataFrameShowMethodInterface import DataFrameShowMethodInterface
except ImportError:
    DataFrameShowMethodInterface = object


class DataFrameDisplay(DataFrameShowMethodInterface):
    def show(self, df: DataFrame):
        display(df.limit(5).toPandas())
