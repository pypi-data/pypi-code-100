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
import logging
from xml.etree import cElementTree as ET

from mcutk.exceptions import ProjectNotFound
from mcutk.apps.projectbase import ProjectBase


class Project(ProjectBase):
    """
    IAR project object

    This class could parser the settings in *.ewp & *.eww.
    """
    PROJECT_EXTENSION = '.ewp'

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)
        self.ewp_file = None
        self.ewp_xml = None

        if self.prjpath.endswith(self.PROJECT_EXTENSION):
            self.ewp_file = self.prjpath
        else:
            # try to find *.ewp automatically
            try:
                self.ewp_file = glob.glob(os.path.join(self.prjdir, "*.ewp").replace("\\", "/"))[0]
            except IndexError:
                raise ProjectNotFound("Could not found IAR project '.ewp'")

        try:
            # iar project must have *.eww file
            self.eww_file = glob.glob(os.path.join(self.prjdir, "*.eww").replace("\\", "/"))[0]
        except IndexError:
            raise ProjectNotFound("Could not found IAR project '.eww'")

        self.ewp_xml = ET.parse(self.ewp_file)
        self._name = os.path.basename(self.ewp_file).split('.')[0]
        self._conf = self._get_all_configuration()
        self._targets = self._conf.keys()

    def _get_all_configuration(self):
        """Read all configuration from *.ewp file

        Raises:
            IOError -- if *.ewp is not exists, it will raise an IOError.

        Returns:
            dict -- targets configuration
        """
        targets = dict()

        for conf in self.ewp_xml.findall("configuration"):
            output_file = ""
            target_name = conf.find("name").text.strip()
            # executable or library, 0: executable, 1: library
            output_type = conf.find(
                "./settings[name='General']/data/option[name='GOutputBinary']/state")\
                    .text.strip()

            if output_type == "0":
                output_dir = conf.find(
                    "./settings[name='General']/data/option[name='ExePath']/state")\
                        .text.strip()
                linkoutput = conf.find(
                    "./settings[name='ILINK']/data/option[name='IlinkOutputFile']/state")

                if linkoutput is not None:
                    output_file = output_dir + '/' +  linkoutput.text.strip()
            else:
                output_file = conf.find(
                    "./settings[name='IARCHIVE']/data/option[name='IarchiveOutput']/state")\
                        .text.strip()

            # Translate IAR Variables to real value
            if output_file and "$PROJ_FNAME$" in output_file:
                output_file = output_file.replace("$PROJ_FNAME$", self._name)

            if output_file and "$PROJ_DIR$" in output_file:
                output_file = output_file.replace("$PROJ_DIR$/", "")

            targets[target_name] = output_file

        return targets

    def get_deps(self):
        """Get project dependecies.
        Return a list of project directory.
        """
        deps = list()
        nodes = self.ewp_xml.findall(
            "configuration/settings[name='ILINK']/data/option[name='IlinkRawBinaryFile']/state"
        )
        for node in nodes:
            if node is not None and node.text:
                p = node.text.strip().replace("$PROJ_DIR$", self.prjdir)
                path = os.path.abspath(p)
                deps.append(path)
        return deps

    def save(self):
        """Save changes"""
        self.ewp_xml.write(self.ewp_file, xml_declaration=True, method='xml', encoding='iso-8859-1')

    def _get_defines(self, target):
        """ Get cc defines nodes in project
        :param target: string type, e.g. "Debug"
        :return: the cc defines ET.element in the given target
        """
        target = self.map_target(target)

        # Get the element including all macro defines
        # Format: <option><name>CCDefines</name><state>DEBUG</state><state>CPU_LPC845M301JBD48</state></option>
        cc_defines = self.ewp_xml.find(".//configuration[name='{}']//option[name='CCDefines']".format(target))
        assert isinstance(cc_defines, ET.Element)
        return cc_defines

    def get_defines(self, target):
        """ get cc defines of given target
        :param target: string type, e.g. "Debug"
        :return: the macro string list
        """
        macros = list()

        cc_defines = self._get_defines(target).findall("./state")
        for node in cc_defines:
            assert isinstance(node, ET.Element)
            macro = node.text
            if macro and macro not in macros:
                macros.append(macro)
        return macros

    def add_defines(self, new, target=None):
        """ add cc defined macro in project target configuration
        :param new: the new macro to add
        :param target: string type, e.g. "Debug", if target not set, will select all targets
        """
        if not new:
            raise ValueError("new macro must be set")

        targets = [self.map_target(target)] if target else self.targets

        changed_flag = False
        for target in targets:
            defines_elem = self._get_defines(target)
            macros = self.get_defines(target)

            if new not in macros:
                new_elem = ET.SubElement(defines_elem, 'state')
                new_elem.text = new
                changed_flag = True
                logging.debug("++macro '%s' in iar target %s", new, target)

        if changed_flag:
            self.save()

    def del_defines(self, old, target=None):
        """ delete cc defined macro in project target configuration
        :old: the macro to remove
        :param target: string type, e.g. "Debug", if target not set, will select all targets
        """
        if not old:
            raise ValueError("target macro must be set to delete")

        targets = [self.map_target(target)] if target else self.targets

        changed_flag = False
        for target in targets:
            defines_elem = self._get_defines(target)
            macros_elems = defines_elem.findall("./state")
            for elem in macros_elems:
                if old == elem.text:
                    defines_elem.remove(elem)
                    changed_flag = True
                    logging.debug("--macro '%s' in iar target %s", old, target)

        if changed_flag:
            self.save()

    @property
    def name(self):
        """Return the application name

        Returns:
            string --- app name
        """
        return self._name
