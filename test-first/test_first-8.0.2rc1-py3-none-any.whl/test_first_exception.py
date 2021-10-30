import unittest

class TestFirstError(Exception): pass
class TestFirstException(unittest.TestCase.failureException): pass
class ScenarioException(TestFirstException): pass
class ExpectationException(TestFirstException): pass
