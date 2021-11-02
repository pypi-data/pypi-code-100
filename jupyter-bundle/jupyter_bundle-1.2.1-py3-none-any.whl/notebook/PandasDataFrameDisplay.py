from IPython.core.display import display
import pandas as pd
from daipecore.pandas.dataframe.PandasDataFrameShowMethodInterface import PandasDataFrameShowMethodInterface


class PandasDataFrameDisplay(PandasDataFrameShowMethodInterface):
    def show(self, df: pd.DataFrame):
        display(df.head())
