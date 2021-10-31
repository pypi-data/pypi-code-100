import pandas as pd
from dummit.tests import Test, TestResult,SumDeltaWithinLimitsTest

# here the DataFrame based tests will be done
# as static methods of a class 
# no_duplicates(primary,key)
# format_check(string,int,string,int,int)
# and some more

class DataFrameTester():
    @staticmethod
    def testForFormat(df,test) -> TestResult:
        for column in test.columns:
            column_name = list(column.keys())[0]
            expected_type = list(column.values())[0]
            pandas_type = df[column].dtypes[0]
            if DataFrameTester.pandasTypeMatchesExpectedType(pandas_type,expected_type) == False:
                return TestResult.COMPLETED_WITH_FAILURE
        return TestResult.COMPLETED_WITH_SUCCESS
    
    @staticmethod
    def testForUniqueness(df,test) ->TestResult:
        count = df.shape[0]
        unique_count = df.groupby(test.columns).count().shape[0]
        if count == unique_count: 
            return TestResult.COMPLETED_WITH_SUCCESS
        else:
            return TestResult.COMPLETED_WITH_FAILURE

    @staticmethod
    def pandasTypeMatchesExpectedType(pandas_type,expected_type):
        # this requires more work for more types of course 
        if (pandas_type=="int64" and expected_type =="int"):
            return True
        if (pandas_type=="object" and expected_type =="string"):
            return True
        return False

    @staticmethod
    def testForSumDelta(df_current,df_past, test :SumDeltaWithinLimitsTest) -> TestResult:
        sum_current = df_current[test.sumColumn].sum()
        sum_past = df_past[test.sumColumn].sum()
        delta  = (sum_current-sum_past)/sum_current
        if (delta>test.allowedChangePercentage / 100): 
            return TestResult.COMPLETED_WITH_FAILURE
        if (delta< -1 * test.allowedChangePercentage / 100): 
            return TestResult.COMPLETED_WITH_FAILURE        
        return TestResult.COMPLETED_WITH_SUCCESS