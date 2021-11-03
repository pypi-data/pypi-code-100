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
Project interface definition.
"""
import abc
import os
import glob

from mcutk.exceptions import ProjectNotFound, InvalidTarget



class ProjectBase(object):
    """
    Abstract class representing a basic project.

    This class defines common interfaces and attributes for a Project object.
    To add new toolchain and it's project class, you should inherit from this
    base.
    """
    __metaclass__ = abc.ABCMeta

    # project extension
    PROJECT_EXTENSION = None

    # NXP MCU SDK MANIFEST object
    SDK_MANIFEST = None

    SDK_ROOT = None

    @classmethod
    def frompath(cls, path):
        """Return a project instance from a given file path or directory.

        If path is a directory, it will search the project file and return an instance.
        Else this will raise mcutk.apps.exceptions.ProjectNotFound.
        """
        if not cls.PROJECT_EXTENSION:
            raise ValueError("%s.PROJECT_EXTENSION is not defined! Please report bug!" % cls)

        if os.path.isfile(path) and path.endswith(cls.PROJECT_EXTENSION):
            return cls(path)

        try:
            project_file = glob.glob(path + "/*" + cls.PROJECT_EXTENSION)[0]
        except IndexError:
            raise ProjectNotFound("Not found project %s in specific folder"%cls.PROJECT_EXTENSION)

        return cls(project_file)

    def __init__(self, path, *args, **kwargs):
        """Defaqult Constructor"""
        self.prjpath = path
        self.prjdir = os.path.dirname(path)
        self._conf = None
        self._targets = list()
        self.sdk_root = None

    @property
    def targets(self):
        """Get targets"""
        return list(self._targets)

    @property
    def targetsinfo(self):
        """Returns a dict about the targets data.

        Example:
        {
            "Debug":   "debug_output_dir/output_name",
            "Release": "release_output_dir/output_name",
        }
        """
        return self._conf

    @abc.abstractproperty
    def name(self):
        """Get project name"""
        return

    def map_target(self, input_target):
        """Try to return correct target value by using string to match.

        If not found InvalidTarget exception will be raised.
        """
        input_target = input_target.strip()
        # map for mdk
        for tname in self.targets:
            if input_target == tname or input_target in tname.split():
                return tname

        # map for general
        for tname in self.targets:
            if input_target.lower() in tname.lower():
                return tname

        for tname in self.targets:
            print("!@ avaliable target: %s" % tname)

        msg = "Cannot map the input target: {}, project: {}, valid targets: {}"\
            .format(input_target, self.prjpath, str(self.targets))
        raise InvalidTarget(msg)

    @property
    def idename(self):
        """Name of toolchain/ide"""
        return str(self.__module__).split('.')[-2]

    def to_dict(self):
        """Dump project basic info to a dict.

        Sample:
            {
                'toolchain': "iar",
                'targets': ["debug", "release"],
                'project': "C:/path/project/",
                'name': "hello_world_project"
            }
        """
        return {
            'toolchain': self.idename,
            'targets': self.targets,
            'project': self.prjpath,
            'name': self.name
        }
