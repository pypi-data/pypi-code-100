#!/usr/bin/env python

import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as f:
    readme = f.read()

setup(name='atooms-models',
      version='1.0.6',
      description='',
      long_description=readme,
      long_description_content_type="text/markdown",
      author='Daniele Coslovich',
      author_email='daniele.coslovich@umontpellier.fr',
      url='https://framagit.org/atooms/models',
      packages=['atooms', 'atooms/models', 'atooms/models/numba', 'atooms/models/f90'],
      license='GPLv3',
      install_requires=['atooms~=3.3', 'f2py_jit'],
      scripts=[],
      package_data={'atooms': ['models/f90/*.f90', 'models/*.json', 'models/samples/*/*']},
      include_package_data=True,
      zip_safe=False,
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
      ]
     )
