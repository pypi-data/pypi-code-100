import enum

class IncompleteTestDefinition(Exception):
    pass

class UnknownTestTypeException(Exception):
    pass

class TestResult:
    NOT_STARTED = 'NOT_STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED_WITH_SUCCESS = 'COMPLETED_WITH_SUCCESS'
    COMPLETED_WITH_FAILURE = 'COMPLETED_WITH_FAILURE'
    
class Test():
    def __init__(self,input_name,is_critical):
        """
        Default constructor, setting some optional fields and crashing is required fields are not there.
            name = test name
            inputName = reference to input
            isCritical = would it be something to stop the run? #TODO
            isSequential = shall it be run as one and only test or parallel run is ok? #TODO
        """
        self.status = TestResult.NOT_STARTED
        self.inputName = input_name
        if self.inputName == None:
            raise IncompleteTestDefinition(f"test_input is missing for test {self.name}")
        self.isCritical = is_critical   

    def __str__(self):
        return f"Test class: '{type(self).__name__}', for {self.inputName}, isCritical:'{self.isCritical}'"

class PresenceTest(Test):
    """That is actually a test without any extra params, parent class fields are enough"""
    def __init__(self,input_name,is_critical):
        super().__init__(input_name,is_critical)

class FreshEnoughTest(Test):
    """One extra field, acceptable max age in hours."""
    def __init__(self,input_name,test_definition,is_critical):
        super().__init__(input_name,is_critical)
        self.maxAgeInHours = int(test_definition)
    
    def __str__(self):
        prefix = super().__str__()
        return prefix + f", acceptable age in hours: {self.maxAgeInHours}"
        
class ColumnsBasedTest(Test):
    def __init__(self,input_name,test_definition,is_critical):
        super().__init__(input_name,is_critical)
        self.columns = test_definition
        if self.columns == None:
            raise IncompleteTestDefinition(f"test_columns is missing for '{self.name}' test")
        if type(self.columns) != list:
            raise IncompleteTestDefinition(f"test_columns is not a list(?) for '{self.name}' test")
        if len(self.columns)==0:
            raise IncompleteTestDefinition(f"test_columns is an empty list for '{self.name}' test")
    
    def __str__(self):
        prefix = super().__str__()
        return prefix + f", columns details: {self.columns}"

class UniquenessTest(ColumnsBasedTest):
    def __init__(self,input_name,test_definition,is_critical):
        super().__init__(input_name,test_definition,is_critical)

class FormatTest(ColumnsBasedTest):
    def __init__(self,input_name,test_definition,is_critical):
        super().__init__(input_name,test_definition,is_critical)
    
class SumDeltaWithinLimitsTest(Test):
    def __init__(self,input_name,test_definition,is_critical):
        super().__init__(input_name,is_critical)
        self.allowedChangePercentage = test_definition["allowed_change_percentage"]
        self.sumColumn = test_definition["sum_column"]
    def __str__(self):
        msg = super().__str__()
        msg = msg + f"allowed % change: {self.allowedChangePercentage}, "
        msg = msg + f"for total on {self.sumColumn} column."
        return msg
        
        