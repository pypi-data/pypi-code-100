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
import glob
from xml.etree import cElementTree as ET
from mcutk.apps.projectbase import ProjectBase


class Project(ProjectBase):
    """
    KDS project object

    This class could parser the settings in .cproject and .project.
    Parameters:
        prjpath: path of .project

    """

    PROJECT_EXTENSION = '.project'

    def __init__(self, prjpath, *args, **kwargs):
        super(Project, self).__init__(prjpath, *args, **kwargs)
        try:
            self.cprjpath = glob.glob(self.prjdir + "/.cproject")[0]
        except Exception:
            raise IOError(".cproject file not found!")

        self._confs = self._get_all_configuration()
        self._targets = self._confs.keys()

    @property
    def name(self):
        """Return the application name

        Returns:
            string --- app name
        """
        xml_root = ET.parse(self.prjpath).getroot()
        app_name = xml_root.find('./name').text.strip()

        return app_name

    def _get_all_configuration(self):
        """read all configuration from .cproject file

        Raises:
            IOError -- if .cproject is not exists, it will raise an IOError.

        Returns:
            dict -- targets configuration
        """
        targets = {}

        xml_root = ET.parse(self.cprjpath).getroot()

        for per_node in xml_root.findall('.//configuration[@buildArtefactType="org.eclipse.cdt.build.core.buildArtefactType.exe"]'):
            target_name = per_node.attrib.get('name').strip()
            output_dir  = target_name
            output_name = self.name + '.' +  per_node.attrib.get('artifactExtension').strip()
            targets[target_name] = (output_dir, output_name)
        return targets
