"""
Drop-in replacement for the unittest module to use them in tests for nbgrader assignments.

You can use this module just like the `unittest` module. Just don't call the `main` function to run the tests but
call the `run_nbgrader_test(MyUnittestClass)` function instead.

If your tests all pass, no output will be generated and nbgrader will assign full marks to this cell.
If one of your tests fail, the usual unittest output will be creates and printed to `sys.stderr` and no marks will be
assigned to this cell in nbgrader.
"""
import io
import sys
from typing import Type
from unittest import *


def run_nbgrader_test(testcase: Type[TestCase]):
    """
    Run the given testcase and generates output only on failure or error.

    :param testcase: TestCase subclass
    :return:
    """

    tests = TestLoader().loadTestsFromTestCase(testcase)
    stream = io.StringIO()
    test_runner = TextTestRunner(stream=stream, verbosity=2)
    test_result = test_runner.run(tests)
    if len(test_result.failures) or len(test_result.errors):
        print(stream.getvalue(), file=sys.stderr)
