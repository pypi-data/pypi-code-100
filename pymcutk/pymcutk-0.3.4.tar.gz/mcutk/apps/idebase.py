#
# MIT License
#
# Copyright 2021 NXP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""
IDE base class definition.
"""
import abc
import os

from enum import Enum
from mcutk.appbase import APPBase
from mcutk.elftool import transform_elf_basic

# default mcutk workspace for eclipse project
DEFAULT_MCUTK_WORKSPACE = os.path.expanduser('~') + '/mcutk_workspace'



class Result(Enum):
    Passed = 0
    PASSED = 0
    Errors = 1
    ERRORS = 1
    Warnings = 2
    WARNINGS = 2
    OtherErrors = 3
    Timeout = 4


class BuildResult(object):
    """The class represent build result object."""

    def __init__(self, result, output):
        self._result = result
        self._output = output

    @property
    def result(self):
        return self._result

    @property
    def output(self):
        return self._output

    @property
    def name(self):
        return self._result.name

    @property
    def value(self):
        return self._result.value

    def set_output(self, v):
        self._output = v

    @classmethod
    def map(cls, result, output=None):
        value = result.lower()
        if value in ("pass", "success", "true", "noerror"):
            ret = Result.Passed

        elif value in ("warnings", "warning"):
            ret = Result.Warnings

        elif value in ("errors", 'error'):
            ret = Result.Errors

        elif value in ('timeout', ):
            ret = Result.Timeout

        else:
            ret = Result.OtherErrors

        return cls(ret, output)


class IDEBase(APPBase):
    """
    An abstract class representing an ide.
    """
    __metaclass__ = abc.ABCMeta

    ISIDE = True

    @staticmethod
    def parse_build_result():
        """Parse the build result: warnning? pass? failed?"""
        raise NotImplementedError()

    def __init__(self, *args, **kwargs):
        name = str(self.__module__).split('.')[-2]
        super(IDEBase, self).__init__(name, *args, **kwargs)

    @abc.abstractmethod
    def build_project(self, project, target, logfile, **kwargs):
        """Return a string about the build command line."""
        pass

    def __str__(self):
        return self.name + "-" + self.version

    def transform_elf(self, type, in_file, out_file):
        """ELF file format converter.
        This is a general method for general ide instance.
        It will calle mcutk/bin/arm-none-eabi-objcopy to do the converter.

        Supported types: bin, ihex, srec.

        Arguments:
            type {str} -- which type you want to convert.
            in_file {str} -- path to elf file.
            out_file {str} -- output file

        Raises:
            ReadElfError -- Unknown elf format will raise such error
            Exception -- Convert failed will raise exception

        Returns:
            bool
        """
        if os.name == 'nt':
            return transform_elf_basic(type, in_file, out_file)
        else:
            raise NotImplementedError("not implemented")
