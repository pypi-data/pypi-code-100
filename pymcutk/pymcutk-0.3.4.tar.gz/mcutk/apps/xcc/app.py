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

import os
import re
import glob
import platform
import logging
import os.path as Path

from mcutk.apps.decorators import build
from mcutk.apps.idebase import IDEBase, BuildResult
from mcutk.apps.cmake import generate_build_cmdline
from mcutk.elftool import transform_elf_basic


class APP(IDEBase):
    """
    Xtensa XCC compiler.
    """

    OSLIST = ["Windows", "Linux", "Darwin"]


    @property
    def is_ready(self):
        return os.path.exists(self.path)

    @build
    def build_project(self, project, target, logfile, **kwargs):
        """Return a command line string.

        Arguments:
            project {xcc.Project} -- xcc project object
            target {string} -- target name
            logfile {string} -- log file path

        Returns:
            string -- commandline string.
        """
        self.path = os.path.normpath(self.path)
        os.environ["XCC_DIR"] = self.path
        # try to set xtensa_system
        xtensa_core = project.get_xtensa_core()
        if xtensa_core:
            tool_dir = os.path.basename(os.path.dirname(self.path))
            xtensa_system = os.path.abspath(os.path.join(
                self.path,
                "../../../builds/",
                "{}/{}/config".format(tool_dir, xtensa_core)))
            if os.path.exists(xtensa_system):
                logging.info("XTENSA_SYSTEM=%s", xtensa_system)
                os.environ["XTENSA_SYSTEM"] = xtensa_system

        return generate_build_cmdline(project, target, logfile)

    def transform_elf(self, type, in_file, out_file):
        """xt-objcopy."""
        objcopy_tool = Path.join(self.path, 'bin/xt-objcopy')
        if platform.system() == 'Windows':
            objcopy_tool += ".exe"
        return transform_elf_basic(type, in_file, out_file, executor=objcopy_tool)

    @staticmethod
    def get_latest():
        """Search and return a latest instance from system."""
        if platform.system() == 'Windows':
            # RI-2019.1-win32\XtensaTools\bin
            default_loc = "C:/usr/xtensa/"
        else:
            default_loc = '/opt/xtensa/'

        path_pattern = default_loc + "XtDevTools/install/tools/*/XtensaTools"
        path_list = glob.glob(path_pattern)
        if not path_list:
            return
        path = path_list[0]
        version = os.path.basename(os.path.dirname(path))
        return APP(path, version=version)

    @staticmethod
    def parse_build_result(exitcode, logfile):
        if exitcode != 0:
            return BuildResult.map("error")

        if not logfile:
            return BuildResult.map("pass")

        warn_ptr = re.compile(r'warning:')
        with open(logfile) as fobj:
            for line in fobj:
                if warn_ptr.search(line) is not None:
                    return BuildResult.map("warning")

        return BuildResult.map("pass")
