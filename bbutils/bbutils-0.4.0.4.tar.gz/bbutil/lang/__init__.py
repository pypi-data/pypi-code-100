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

import os
import os.path

from typing import Dict, Optional, Any

from bbutil.lang.domain import Domain

__all__ = [
    "parser",

    "domain",

    "Lang"
]

lang_domain = None


class Lang(object):

    def __init__(self):
        self.localedir: Optional[str] = None
        self.do_setup: bool = False
        self.used_lang: Optional[str] = None
        self.ignore = os.getenv("IGNORE_GETTEXT", None)
        self.domains: Dict[str, Domain] = {}
        self.use_dummy: bool = False
        self.is_setup: bool = False
        return

    @staticmethod
    def dummy(text: str):
        return text

    def setup(self, localedir: str, used_lang: str = "en") -> bool:
        self.is_setup = False
        if localedir == "":
            return False

        if os.path.exists(localedir) is False:
            self.use_dummy = True
            return False

        self.localedir = localedir

        if self.used_lang is None:
            self.used_lang = used_lang

        if self.ignore is not None:
            self.use_dummy = True
        self.is_setup = True
        return True

    def _get_domain(self, domain_name: str) -> Optional[Domain]:

        try:
            _domain = self.domains[domain_name]
        except KeyError:
            return None

        return _domain

    def _create_domain(self, domain_name: str) -> Domain:
        _domain = Domain(localedir=self.localedir,
                         domain=domain_name,
                         use_dummy=self.use_dummy,
                         ignore=self.ignore,
                         used_lang=self.used_lang)

        self.domains[_domain.domain] = _domain
        return _domain

    def set_language(self, language: str):
        self.used_lang = language

        for _name in self.domains:
            _domain = self.domains[_name]
            _domain.is_set = False
            _domain.used_lang = self.used_lang
            _domain.create()
            _domain.load()
        return

    def add(self, domain_name: str, callback: Any = None):

        _domain = self._get_domain(domain_name)
        if _domain is None:
            _domain = self._create_domain(domain_name)
            _domain.create()

        _domain.callback.append(callback)
        _domain.load()
        return
