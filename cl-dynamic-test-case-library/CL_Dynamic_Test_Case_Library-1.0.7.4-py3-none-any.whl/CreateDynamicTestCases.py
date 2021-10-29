from robot.running.model import TestSuite

class CreateDynamicTestCases(object):
    ROBOT_LISTENER_API_VERSION = 3
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = 0.1

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        self.top_suite = None

    def _start_suite(self, suite, result):
        self.top_suite = suite
        self.top_suite.tests.clear() # remove placeholder test

    def create_test_case(self, tc_name, keyword, *args):
        tc = self.top_suite.tests.create(name=tc_name)
        tc.body.create_keyword(name=keyword, args=args)
        
    def create_test_matrix(self, test_data, test_scenarios):
        for data in test_data:
            for test_scenario in test_scenarios:
                self.create_test_case(f'{test_scenario} - {data}', test_scenario, data)
""" 
  The library uses listener interface 3 to pass objects to the listener methods. 
  It uses the listener as a library, which enables both a listener and keywords to be used in the same file
      to dynamically create test cases
  def _start_suite:
      Starts running the suite of test cases that were dynamically created via
	  the python module create_test_case or create_test_matrix
  def create_test_case:
      Creates a dynamic test case for the tc_name (test case name) that used the keyword and 
	  *args (keyword arguments) provided as a template to run the test case
  def create_test_matrix:	  
      Creates a dynamic test case for each unique combination of test_data and test_scenario
	  provided in the arguments  
  The statement below is required as the module needs a class name that has the same name as a module.	  
"""				
globals()[__name__] = CreateDynamicTestCases