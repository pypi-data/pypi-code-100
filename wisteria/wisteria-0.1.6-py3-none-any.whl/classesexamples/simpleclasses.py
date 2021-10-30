#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    Wisteria Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Wisteria.
#    Wisteria is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Wisteria is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Wisteria.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    Wisteria project : wisteria/classesexamples/simpleclasses.py

    Some extremely simple classes.


    ___________________________________________________________________________

    o  MetaClass class
    o  RegularClass class
    o  RegularClassDict class
    o  RegularClassList class
"""


class MetaClass(type):
    def __new__(cls):
        pass


class RegularClass:

    def __eq__(self, other):
        return type(self) == type(other)

    async def async_method():
        pass

    @classmethod
    def class_method(cls):
        pass

    def generator(self):
        yield None

    def method(self):
        pass

    @staticmethod
    def static_method():
        pass


class RegularClassInheritedDict(dict):
    def __eq__(self, other):
        return type(self) == type(other) and \
            tuple(items for items in self.items()) == tuple(items for items in other.items())

    def __init__(self):
        dict.__init__(self)
        self["str_key"] = "value"


class RegularClassInheritedList(list):
    def __eq__(self, other):
        return type(self) == type(other) and \
            tuple(items for items in self) == tuple(items for items in other)

    def __init__(self):
        list.__init__(self)
        self.append("random string")
