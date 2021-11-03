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
from typing import List

from bbutil.lang.parser.language import Languages
from bbutil.lang.parser.pyfile import PythonFile


from bbutil.utils import full_path

__all__ = [
    "Domain"
]


class Domain(object):

    def __repr__(self):
        return self.domain

    def __init__(self, root_path: str, domain: str):
        self.root_path: str = root_path
        self.domain: str = domain
        self.path: str = full_path("{0:s}/.locales/{1:s}".format(self.root_path, self.domain))
        self.pot: str = full_path("{0:s}/.locales/{1:s}/{1:s}.pot".format(self.root_path, self.domain))
        self.lang: List[Languages] = []
        self.files: List[PythonFile] = []
        return
