#!python
import os
import subprocess

from siriushlacon.pctrl.consts import PCTRL_MAIN

os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"
subprocess.Popen("pydm --hide-nav-bar " + PCTRL_MAIN, shell=True)
