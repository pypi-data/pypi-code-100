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

import gettext

from typing import Optional, Any, List

__all__ = [
    "Domain",
]

lang_domain = None


class Domain(object):

    def __init__(self, localedir: str, domain: str, use_dummy: bool, ignore, used_lang: str):
        self.localedir: str = localedir
        self.domain: str = domain
        self.gettext: Optional[gettext.translation] = None
        self.lang = None
        self.is_set: bool = False
        self.ignore = ignore
        self.callback: List[Any] = []
        self.used_lang: str = used_lang
        self.use_dummy: bool = use_dummy
        return

    @staticmethod
    def _dummy(text: str):
        return text

    def create(self):
        if self.is_set is True:
            return

        if self.ignore is not None:
            self.use_dummy = True

        if self.use_dummy is True:
            self.lang = self._dummy
            self.is_set = True
            return

        used_catalog = [
            self.used_lang
        ]

        self.gettext = gettext.translation(self.domain, localedir=self.localedir, languages=used_catalog)
        self.gettext.install()

        self.lang = self.gettext.gettext
        self.is_set = True
        return

    def load(self):
        for _callback in self.callback:
            _callback(self.lang)
        return
