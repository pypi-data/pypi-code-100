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
    Wisteria project : wisteria/dmfile.py

    DMFile class (=disk/in-memory file).

    Use DMFile to open on disk and in-memory files. You may use DMFile objects
    with Python 'with' statement.


    ___________________________________________________________________________

    o  DMFile class
"""
from io import StringIO


class DMFile:
    """
        DMFile class

        Disk/in-memory file. Very simple class allowing to open in-memory and on disk
        files.

        _______________________________________________________________________

        o  __enter__(self)
        o  __exit__(self, exc_type, exc_val, exc_tb)
        o  __init__(self, name, mode="r")
        o  __iter__(self)
        o  close(self)
        o  read(self)
        o  write(self, string)
    """
    def __enter__(self):
        """
            DMFile.__enter__()
        """
        return self

    def __exit__(self,
                 exc_type,
                 exc_val,
                 exc_tb):
        """
            DMFile.exit()
        """
        self.close()

    def __init__(self,
                 name,
                 mode="r"):
        """
            DMFile.__init__()
        """
        self.in_memory = name[0] == ":" and name[-1] == ":"
        if not self.in_memory:
            self.name = name
            #   pylint: disable=consider-using-with
            self.obj = open(name, mode=mode, encoding="utf-8")
        else:
            self.name = name[1:-1]
            self.obj = StringIO()

    def __iter__(self):
        """
            DMFile.__iter__()
        """
        for line in self.read().split("\n"):
            yield line

    def close(self):
        """
            DMFile.close()
        """
        if self.obj:
            self.obj.close()

    def read(self):
        """
            DMFile.read()
        """
        if not self.in_memory:
            self.obj.seek(0)
            return self.obj.read()

        # on disk:
        self.obj.seek(0)
        return self.obj.read()

    def write(self,
              string):
        """
            DMFile.write()
        """
        self.obj.write(string)
