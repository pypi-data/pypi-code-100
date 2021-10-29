#! /usr/bin/env python3
from setuptools import setup
import pathlib

setup(
    name                =   "sre_parse36",
    description         =   "Python 3.6 sre_parse module",
    author              =   "Python Software Foundation",
    url                 =   "https://github.com/tristanlatr/sre_parse36",
    version             =   "1.0.0",
    py_modules          =   ['sre_parse36',],
    classifiers         =   ["Programming Language :: Python :: 3"],
    license             =   "GNU General Public License v3.0",
    long_description    =   pathlib.Path(__file__).parent.joinpath("README.md").read_text(),
    long_description_content_type   =   "text/markdown",
)
