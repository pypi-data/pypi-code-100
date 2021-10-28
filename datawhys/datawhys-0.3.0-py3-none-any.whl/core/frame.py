from pandas import DataFrame

from datawhys.core.series import DataWhysSeries


class DataWhysFrame(DataFrame):
    """
    A DataWhysFrame object is a pandas.DataFrame that has certain
    DataWhys specific operations and methods.

    The DataWhysFrame object is composed of 1 or more DataWhysSeries
    objects. The inner workings of the DataWhysFrame ensures that
    each variable is instantiated as a DataWhysSeries.

    For additional reference specific to the Pandas DataFrame object
    and features, please refer to the Pandas API

    **Parameters**

    data: ndarray, Iterable, dict, DataFrame, or DataWhysFrame
        Dict can contain Series, DataWhysSeries, arrays, constants,
        or list-like objects.

    **Examples**

    >>> from datawhys.core.frame import DataWhysFrame
    >>> import pandas as pd
    >>> df = pd.read_csv('path/to/file.csv')
    >>> dwf = DataWhysFrame(df)

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def _constructor(self):
        return DataWhysFrame

    @property
    def _constructor_sliced(self):
        return DataWhysSeries
