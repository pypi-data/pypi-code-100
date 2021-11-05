import unittest
import sys

#unit
print("UNIT TESTS")
loader = unittest.TestLoader()
start_dir = 'unit'
suite = loader.discover(start_dir)

runner = unittest.TextTestRunner()

ret = not runner.run(suite).wasSuccessful()
if not ret:
    #integration IGNORE INTEGRATION TEMP
    # print("INTEGRATION TESTS")
    # loader = unittest.TestLoader()
    # start_dir = 'integration'
    # suite = loader.discover(start_dir)
    #
    # runner = unittest.TextTestRunner()
    #
    # ret = not runner.run(suite).wasSuccessful()
    sys.exit(ret)