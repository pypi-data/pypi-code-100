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
APP base class definition.
"""
import abc
import os


class APPBase(object):
    """
    An abstract class representing the interface for an app.
    """
    __metaclass__ = abc.ABCMeta

    # @staticmethod
    # @abc.abstractmethod
    # def get_latest():
    #     pass

    def __init__(self, name, path="", version=None, **kwargs):
        """APPBase interface definition.

        Arguments:
            name {string} -- app name
            path {string} -- app path

        Keyword Arguments:
            version {string} -- app version (default: {None})
        """
        self._name = name
        self._path = path
        self.version = version

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value in (None, "None", ""):
            raise ValueError("invalid name")
        self._name = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        if value in (None, "None", ""):
            raise ValueError("invalid path")
        self._path = value

    @abc.abstractproperty
    def is_ready(self):
        return os.path.exists(self._path)

    def show(self):
        attrs = vars(self)
        for attr, value in attrs.items():
            print("{0}: {1}".format(attr, value))

    def __str__(self):
        return "App({}-{})".format(self._name, self.version)
