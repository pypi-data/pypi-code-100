#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
THIS FILE IS PART OF NETWORK FOR MWAFU LIBRARY LOVE BOOK STORE BY MATT BELFAST BROWN
setup.py - The core part of the Author Number library.

Author: Matt Belfast Brown 
Creat Date:2021-05-30
Version Date：2021-11-02
Version:1.1.0


THIS PROGRAM IS FREE FOR EVERYONE,IS LICENSED UNDER GPL-3.0
YOU SHOULD HAVE RECEIVED A COPY OF GPL-3.0 LICENSE.

Copyright (C) 2021  Matt Belfast Brown
Copyright (C) 2021  MWAFU LIBRARY LOVE BOOK STORE

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


'''

from setuptools import setup, find_packages

setup(
    name = 'autoauthnumber',
    version = '1.1.0',
    keywords = ('auto', 'author number'),
    description = 'This is a library about automatic number-taking of "General Chinese Author Number Table". At present, there is only one way to take the number, that is, directly looking up the table.In the future, we will adapt to a variety of author numbering methods, please wait.',
    
    
    license = 'GPL-3.0 License',
    url='http://belfast.xiaopangkj.space/nwflbs/about/schedule.html',
    author = 'Matt Brown',
    author_email = 'thedayofthedo@gmail.com',
    py_modules=['autoauthnumber.mk_Pron','autoauthnumber.author_number'],
    include_package_data = True,
    packages = find_packages(),
    platforms = 'any',
    zip_safe=True,
    install_requires = ['pypinyin']
)

