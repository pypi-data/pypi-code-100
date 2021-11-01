# This file is placed in the Public Domain.

import unittest

from gcd.obj import Cfg
from gcd.ofn import fmt
from gcd.run import Runtime, getmain
from gcd.run import Cfg as RunCfg


class Test_Kernel(unittest.TestCase):
    def test_cfg(self):
        self.assertTrue("gcd.run.Cfg" in str(RunCfg))
