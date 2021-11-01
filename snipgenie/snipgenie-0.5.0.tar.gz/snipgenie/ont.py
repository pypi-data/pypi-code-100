#!/usr/bin/env python

"""
    snipgenie ONT utils.
    Created Oct 2021
    Copyright (C) Damien Farrell

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 3
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import sys,os,subprocess
import glob,platform,shutil
from .qt import *
import pandas as pd
import numpy as np
import pylab as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from . import widgets
import geopandas as gpd

home = os.path.expanduser("~")
module_path = os.path.dirname(os.path.abspath(__file__)) #path to module

def run_guppy(path,out,threads_per_caller,num_callers,chunks_per_runner,gpu_runners_per_device):

    cmd = 'guppy_basecaller -i {p} -s {o} --cpu_threads_per_caller {tpc} --num_callers {nc} --chunks_per_runner {cpr} \
        --gpu_runners_per_device {grpd} \
        -c {c} -x "cuda:0"'.format(o=out,p=path,c=cfg,tpc=threads_per_caller,nc=num_callers,
                                   cpr=chunks_per_runner,grpd=gpu_runners_per_device)
    print (cmd)
    st=time.time()
    tmp = subprocess.check_output(cmd, shell=True)
    elapsed=time.time()-st
    return elapsed

def join_fastq(path, out):
    import gzip
    files = os.path.join(path,'*.fastq')
    cmd = 'cat {f} > {o}'.format(f=files,o=out)
    print (cmd)
    subprocess.check_output(cmd,shell=True)
    cmd = 'gzip %s' %out
    print ('compressing')
    subprocess.check_output(cmd,shell=True)
    return

    
