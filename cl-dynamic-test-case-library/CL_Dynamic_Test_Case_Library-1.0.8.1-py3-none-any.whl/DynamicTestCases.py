from robot.running.model import TestSuite

class CreateDynamicTestCases(object):
    ROBOT_LISTENER_API_VERSION = 3
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = 0.1

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        self.current_suite = None

    def _start_suite(self, suite, result):
        """
        Starts running the suite of test cases that were dynamically created via
        the python module create_test_case
        and remove the test suite placeholder test so that it
        is not counted in the test results metrics
        """
        self.current_suite = suite
        self.current_suite.tests.clear()  # remove placeholder test

	def create_test_case(self, tc_name, kwname, arguments):
        """
        Creates a dynamic test case for the tc_name (test case name) and uses the keyword and 
        arguments (keyword arguments) provided as a template to run the test case for each row
        of data in the excel data file worksheet

        'tc_name' is the test case name
        'kwname' is the keyword to call
        'arguments' are the arguments to pass to the keyword

        Example:
            Create Test Case   Test Case Name
            ...     Keyword Name    Arg1   Arg2  Arg3
        """
        tc = self.current_suite.tests.create(name=tc_name)
        tc.body.create_keyword(name=kwname, args=arguments)

# To get the class to load, the module needs to have a class
# with the same name as the module. This makes that happen:
globals()[__name__] = CreateDynamicTestCases