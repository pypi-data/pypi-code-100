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

import logging
import os
import glob
from xml.etree import ElementTree as ET
from distutils.version import LooseVersion


class SDKManifest(object):
    """NXP MCUXpresso SDK Manifest Parser."""

    @classmethod
    def find(cls, dirs):
        """Find manifest from given directories."""
        if not isinstance(dirs, list):
            dirs = [dirs]
        manifests = list()
        for dir in dirs:
            manifestfilelist = glob.glob("{0}/*_manifest*.xml".format(dir))
            for per_file in manifestfilelist:
                manifest_obj = cls(per_file)
                if manifest_obj:
                    manifests.append(manifest_obj)

        return manifests

    @classmethod
    def find_from_parents(cls, dir):
        """Find manifest from the give path of parent.
        """
        abs_path = os.path.abspath(dir.replace('\\', '/'))
        def _search_dir():
            current_dir = abs_path
            while True:
                parent_dir = os.path.dirname(current_dir)
                # system root
                if parent_dir == current_dir:
                    break
                manifest = cls.find_max_version(parent_dir)
                if manifest:
                    return manifest
                current_dir = parent_dir

        manifest = _search_dir()
        if manifest:
            return manifest

    @classmethod
    def find_max_version(cls, dirs):
        """Find and return the maximum version of manifest from given paths."""
        if isinstance(dirs, str):
            dirs = [dirs]
        manifests = SDKManifest.find(dirs)
        if not manifests:
            return None
        return sorted(manifests, key=lambda m: LooseVersion(m.manifest_version))[-1]

    def __init__(self, filepath):
        self._filepath = filepath
        self._xmlroot = ET.parse(filepath).getroot()
        self._sdk_root = os.path.dirname(filepath)
        self._id = self._xmlroot.attrib['id']
        self._manifest_version = self._xmlroot.attrib['format_version']
        self._sdk_name = self._xmlroot.attrib["id"]
        self._sdk_version = self._xmlroot.find('./ksdk').attrib['version']

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        else:
            return False

    @property
    def filepath(self):
        return self._filepath

    @property
    def id(self):
        return self._id

    @property
    def sdk_version(self):
        return self._sdk_version

    @property
    def sdk_name(self):
        return self._sdk_name

    @property
    def format_version(self):
         return self._manifest_version

    @property
    def manifest_version(self):
        return self._manifest_version

    @property
    def sdk_root(self):
        return self._sdk_root

    @property
    def boards(self):
        xpath = './boards/board'
        nodes = self._xmlroot.findall(xpath)
        return [n.attrib['id'] for n in nodes]

    @property
    def toolchains(self):
        xpath = './toolchains/toolchain'
        nodes = self._xmlroot.findall(xpath)
        return [n.attrib['id'] for n in nodes]

    def find_example(self, example_id):
        """Return a dict which contain exmaple attributes.

        Keys:
            - id
            - name
            - toolchain
            - brief
            - category
            - path
        """
        xpath = './boards/board/examples/example[@id="{0}"]'.format(example_id)
        example_info = dict()
        node = self._xmlroot.find(xpath)
        if node is None:
            logging.debug("Cannot found example in manifest, id: %s", example_id)
            return

        example_info.update(node.attrib)
        xml_node = node.find('./external[@type="xml"]')
        xml_filename = xml_node.find('./files').attrib['mask']
        example_info['example.xml'] = xml_filename
        return example_info

    def dump_examples(self):
        """Return a list of examples.
        """
        xpath = './boards/board/examples/example'
        examples = list()
        for example_node in self._xmlroot.findall(xpath):
            examples.append({
                'toolchain': example_node.attrib['toolchain'].split(" "),
                'path': example_node.attrib['path'],
                'name': example_node.attrib['name']
            })
        return examples
