#!/usr/bin/python

"""Correct D#### and map device names.

Tong Zhang <zhangt@frib.msu.edu>
2017-09-29 16:45:08 PM EDT
"""

import re
from phantasy import Settings
from collections import OrderedDict
import json


infile = '../FRIB_FE/FE_settings.json'
outfile = 'settings.json'
settings0 = Settings(infile)

new_setting = OrderedDict()
for k,v in settings0.items():
    _sys, _dev, _num = re.match(r'(.*):(.*)_D([0-9]*)', k).groups()
    #if _dev in ['QHE', 'QVE']: _dev = 'QE'
    n = '{0}:{1}_D{2:04d}'.format(_sys, _dev, int(_num))
    new_setting[n] = v

json.dump(new_setting, open(outfile, 'w'), indent=2)




