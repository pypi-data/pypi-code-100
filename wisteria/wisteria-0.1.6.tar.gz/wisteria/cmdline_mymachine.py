#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    Wisteria Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Wisteria.
#    Wisteria is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Wisteria is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Wisteria.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    Wisteria project : wisteria/cmdline_mymachine.py

    Display informations about the current machine.

    ___________________________________________________________________________

    o  mymachine(detailslevel=1)
"""
import platform

import psutil
import cpuinfo

from wisteria.msg import msgreport


def mymachine(detailslevel=1):
    """
        mymachine()

        Display informations about the current machine.

        This functions relies on the following packages:
        - platform
        - psutil        (external package, to be displayed)
        - py-cpuinfo    (external package, to be displayed)

        _______________________________________________________________________

        ARGUMENT: (int)detailslevel:
                        0: minimal      (one line)
                        1: normal       (several lines)
                        2: full details (several lines)
    """
    if detailslevel == 0:
        msgreport(f"{platform.system()} ({platform.release()}) "
                  f"/ {cpuinfo.get_cpu_info()['brand_raw']}")
        return

    # ---- platform package ---------------------------------------------------
    infos = {'platform': platform.system(),
             'platform-release': platform.release(),
             'platform-version': platform.version(),
             'architecture': platform.machine(),
             'processor': platform.processor(),
             }

    # ---- psutil package -----------------------------------------------------
    try:
        cpufreq = psutil.cpu_freq()
        vmemory = psutil.virtual_memory()

        infos["(psutil) physical cores"] = psutil.cpu_count(logical=False)
        infos["(psutil) total cores"] = psutil.cpu_count(logical=True)
        infos["(psutil) max frequency"] = f"{cpufreq.max:.2f}Mhz"
        infos["(psutil) min frequency"] = f"{cpufreq.min:.2f}Mhz"
        infos["(psutil) current frequency"] = f"{cpufreq.current:.2f}Mhz"

        infos["(psutil) virtual memory/total"] = f"{vmemory.total/1000000000:.2f}Go"
        infos["(psutil) virtual memory/used"] = f"{vmemory.used/1000000000:.2f}Go"
        infos["(psutil) virtual memory/free"] = f"{vmemory.free/1000000000:.2f}Go"

    except ImportError:
        msgreport("Please note that not all informaton could be displayed "
                  "since package 'psutil' is not installed. "
                  "You can install it with: `$ pip install psutil` ."
                  "Confer https://psutil.readthedocs.io/en/latest/ ")

    # ---- cpuinfo package ----------------------------------------------------
    try:
        for key, value in cpuinfo.get_cpu_info().items():
            if key == "brand_raw" or detailslevel == 2:
                infos["(cpuinfo) "+str(key)] = value

    except ImportError:
        msgreport("Please note that not all informaton could be displayed "
                  "since package 'cpuinfo' is not installed. "
                  "You can install it with: `$ pip install py-cpuinfo` ."
                  "Confer https://pypi.org/project/py-cpuinfo/ ")

    # -------------------------------------------------------------------------
    # final output
    # -------------------------------------------------------------------------
    for key, value in infos.items():
        msgreport(f"* {key:>30} : {value}")
