import unittest

from net_templates.templar import TemplarBase


class TestTemplarBase(unittest.TestCase):

    TESTED_CLASS = TemplarBase

    def test_get_environment(self):
        env = self.TESTED_CLASS.get_device_type_environment(device_type='ios')



if __name__ == '__main__':
    unittest.main()
