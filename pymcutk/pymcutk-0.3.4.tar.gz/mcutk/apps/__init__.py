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

from mcutk.exceptions import (ProjectNotFound, ProjectParserError, InstallError)

__all__ = ["appfactory", "factory"]



def appfactory(name):
    """Return specific APP class.

    Example 1, basic:
        >>> APP = appfactory('iar')
        <mcutk.apps.iar.APP object at 0x1023203>

    Example 2, get the latest instance by scanning your system:
        >>> app = appfactory('iar').get_latest()
        >>> print app.path
        C:/program files(x86)/IAR Systems/IAR Workbench/
        >>> print app.version
        8.22.2

    Example 3, create app instance directly:
        >>> APP = appfactory('iar')
        >>> app = APP('/path/to/ide', version='1.0.0')
        >>> print app.path
        C:/program files(x86)/IAR Systems/IAR Workbench/
        >>> print app.version
        8.22.2

    Example 4, load and parse the project:
        >>> project = appfactory('iar').Project('/path/to/project')
        >>> print project.name
        hello_world
        >>> print project.targets
        ['debug', 'release']

    """
    import importlib
    idemodule = importlib.import_module("mcutk.apps.%s"%(name))
    appcls = getattr(idemodule, "APP")
    projcls = getattr(idemodule, "Project")
    appcls.Project = projcls
    return appcls


def factory(name):
    """Return specific app module"""
    import importlib
    try:
        idemodule = importlib.import_module("mcutk.apps.%s"%(name))
    except ImportError:
        pass
    return idemodule
