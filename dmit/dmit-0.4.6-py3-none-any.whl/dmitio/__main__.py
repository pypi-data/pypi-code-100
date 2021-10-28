#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Master module for dmit.dmitio
"""

__author__ = "K. Hintz"
__copyright__ = "Danish Meteorological Institute"

__license__ = "MIT"
__version__ = "0.0.2.2"
__maintainer__ = "K. Hintz"
__email__ = "kah@dmi.dk"
__status__ = "Development"

import sys
import os
sys.path.insert(0, os.path.abspath('./dmitio/'))
import argparse
from argparse import ArgumentDefaultsHelpFormatter

from dmit import ostools
from .arguments import arguments
from .grib import readgrib
from .netcdf import writenc

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def find_files_to_read(args:argparse.Namespace) -> list:
        """Finds the file(s) to read and plot from

        Parameters
        ----------
        args : argparse.Namespace
            Input arguments to dlotter.__main__

        Returns
        -------
        list
            List with path(s) to file(s)
        """

        directory = args.directory

        if args.limit_files > 0:
            inorder = True
        else:
            inorder = False

        files = ostools.find_files(directory, 
                                   prefix=args.prefix, 
                                   postfix=args.postfix,
                                   recursive=False, 
                                   onlyfiles=True,
                                   fullpath=True,
                                   olderthan=None,
                                   inorder=inorder)

        if args.limit_files > 0: 
            if args.limit_files >= len(files):
                limit = len(files)
            else:
                limit = args.limit_files

            files = files[0:limit]

        return files


if __name__ == '__main__':

    modargs = arguments()
    args = modargs.get_args(sys.argv)

    if args.verbose:
        print('---- Input Arguments ----', flush=True)
        for p in args._get_kwargs():
                print("{}: {}".format(p[0], p[1]), flush=True)
        print('---- --------------- ----', flush=True)

    if args.cmd == 'gribtonc':
        files_to_read = find_files_to_read(args)
        
        if args.filetype == 'grib2':
            datareader = readgrib(args, files_to_read)
            data = datareader.data
        else:
            print('Filetype: "{}", not supported.'.format(args.filetype), flush=True)
            sys.exit(1)

        nc_writer = writenc(args, data)