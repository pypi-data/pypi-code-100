#  The MIT License (MIT)
#
#  Copyright (c) 2021. Scott Lau
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import unittest

import numpy as np
import pandas as pd
from pandas import ExcelWriter


class PandasTestCase(unittest.TestCase):
    def test_pivot_table(self):
        data = pd.read_excel("pandas测试.xlsx", sheet_name="Sheet1", header=0)
        print(data)

        table = pd.pivot_table(
            data,
            values=["较年初", "较季度初", "较月初", "较上周", "较昨日"],
            columns=["指标"],
            index=["所在部门"],
            aggfunc=np.sum,
            fill_value=0,
        )
        print(table)
        with ExcelWriter("pandas_result.xlsx") as excel_writer:
            table.to_excel(
                excel_writer=excel_writer,
                index=True,
            )

    def test_pivot_table2(self):
        data = pd.read_excel("pandas测试2.xlsx", sheet_name="Sheet1", header=0)
        print(data)

        table = pd.pivot_table(
            data,
            values=["贷款合计", "个经小计", "个消小计", "个人业务非息收入小计"],
            columns=["比较类型"],
            index=["所在部门"],
            aggfunc=np.sum,
            fill_value=0,
        )
        print(table)
        with ExcelWriter("pandas_result2.xlsx") as excel_writer:
            table.to_excel(
                excel_writer=excel_writer,
                index=True,
            )


if __name__ == '__main__':
    unittest.main()
