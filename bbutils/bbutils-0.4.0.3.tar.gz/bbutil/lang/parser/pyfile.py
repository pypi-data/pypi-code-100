#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
#    Copyright (C) 2017, Kai Raphahn <kai.raphahn@laburec.de>
#

import os.path

from typing import Optional

from bbutil.utils import full_path, get_attribute
from bbutil.logging import Logging

__all__ = [
    "PythonFile"
]

log: Optional[Logging] = None


def set_log(logging: Logging):
    global log
    log = logging
    return


class PythonFile(object):

    def __repr__(self):
        return self._basename

    @property
    def basename(self) -> str:
        return self._basename

    def __init__(self,
                 package_path: str,
                 filename: str,
                 module: str,
                 module_filter: str = "",
                 locales: str = ".locales"):

        self._package_path: str = package_path
        self._basename: str = os.path.basename(filename).replace(".py", "")
        self._module: str = module
        self._module_filter: str = module_filter
        self._locales: str = locales

        self.fullname: str = filename
        self.domain: str = ""
        self.classname: str = ""
        self.pot: str = ""
        self.path: str = ""
        return

    def create(self) -> bool:

        _root = full_path("{0:s}/".format(self._package_path))
        _root = "{0:s}{1:s}".format(_root, os.path.sep)
        _filename = self.fullname.replace(_root, "")

        module_path = _filename.replace(".py", "")
        module_path = module_path.replace(os.path.sep, ".")

        if "__init__" in module_path:
            module_path = module_path.replace(".__init__", "")

        if self._module == "":
            self.classname = module_path
        else:
            self.classname = "{0:s}.{1:s}".format(self._module, module_path)

        _info = "{0:s}: {1:s}".format(self._package_path, _filename)
        log.debug3("Parse", _info)

        if self._module_filter not in self.classname:
            return False

        try:
            lang = get_attribute(self.classname, "lang_domain")
        except ImportError as e:
            lang = None
            log.error("Unable to open module: {0:s}".format(self.classname))
            log.exception(e)

        if lang is None:
            return False

        _logtext = "{0:s}: {1:s}".format(lang, self.classname)

        log.inform("Add", _logtext)
        self.domain = lang
        _pot = "{0:s}/{1:s}/_{2:s}.pot".format(self._locales, self.domain, self.classname)
        _path = "{0:s}/{1:s}".format(self._locales, self.domain)
        self.pot = full_path(_pot)
        self.path = full_path(_path)
        return True
