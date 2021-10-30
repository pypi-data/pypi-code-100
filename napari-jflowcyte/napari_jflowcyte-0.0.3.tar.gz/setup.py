#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import setup, find_packages

def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()

setup(
    name='napari_jflowcyte',
    version='0.0.3',
    author='Jay Unruh',
    description='A plugin to read, write, gate, and compensate flow cytometry (fcs) files.',
    url='https://github.com/jayunruh/napari_jflowcyte',
    license='GNU GPLv2',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=["napari_plugin_engine>=0.1.4","numpy","numba","pandas"],
    py_modules=['importflowcyte','exportflowcyte','gateflowcyte','compensateflowcyte'],
    #entry_points={
    #    'napari.plugin': [
    #        'napari_jroireader = napari_jroireader',
    #    ],
    #},
)
