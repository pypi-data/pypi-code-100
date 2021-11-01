#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""OSDU CLI package that can be installed using setuptools"""

# For reasons behind /src/ file structure see https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure

import os
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
from setuptools import setup, find_packages


def read(fname):
    """Local read helper function for long documentation"""
    osducli_path = dirname(os.path.realpath(__file__))
    return open(join(osducli_path, fname)).read()


version_file = read(os.path.join("src", "osducli", "__init__.py"))
__VERSION__ = re.search(
    r'^__VERSION__\s*=\s*[\'"]([^\'"]*)[\'"]', version_file, re.MULTILINE
).group(1)

setup(
    name="osducli",
    version=__VERSION__,
    description="OSDU command line",
    long_description=read("README.rst"),
    url="https://community.opengroup.org/osdu/platform/data-flow/data-loading/osdu-cli",
    author="Equinor ASA",
    author_email="mhew@equinor.com",
    license="Apache",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="osdu",
    python_requires=">=3.8",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    install_requires=["click", "jmespath", "osdu-sdk==0.0.8", "requests", "tabulate", "msal"],
    project_urls={
        "Issue Tracker": "https://community.opengroup.org/osdu/platform/data-flow/data-loading/osdu-cli/-/issues",
    },
    entry_points={"console_scripts": ["osdu=osducli.__main__:main"]},
)
