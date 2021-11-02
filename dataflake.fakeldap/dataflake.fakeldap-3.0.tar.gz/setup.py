##############################################################################
#
# Copyright (c) 2012-2021 Jens Vagelpohl and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import os

from setuptools import find_packages
from setuptools import setup


NAME = 'dataflake.fakeldap'


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


setup(name=NAME,
      version=read('version.txt').strip(),
      description='Mocked-up LDAP connection library',
      long_description=read('README.rst'),
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Systems Administration ::"
        " Authentication/Directory :: LDAP",
        ],
      keywords='ldap ldapv3',
      author="Jens Vagelpohl",
      author_email="jens@dataflake.org",
      url="https://github.com/dataflake/%s" % NAME,
      project_urls={
        'Source code': 'https://github.com/dataflake/%s' % NAME,
        'Issue Tracker': 'https://github.com/dataflake/%s/issues' % NAME,
      },
      license="ZPL 2.1",
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['dataflake'],
      python_requires='>=3.5',
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'python-ldap >= 3.3',
        ],
      tests_require=['python-ldap', 'volatildap'],
      test_suite='%s.tests' % NAME,
      extras_require={
        'docs': ['Sphinx',
                 'repoze.sphinx.autointerface',
                 'sphinx_rtd_theme',
                 ],
        },
      )
