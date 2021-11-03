#
# MIT License
#
# Copyright 2021 NXP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os
from setuptools import setup, find_packages

version = '0.3.4'

install_requires = [
    'pyserial<4.0,>=3.5',
    'mbed-ls>=1.8.9',
    "pexpect<5.0,>=4.8",
    "packaging>=20.4",
    'future',
    "click>=7.0",
    "pyelftools",
    "pyyaml",
    'globster',
    'enum34'
]

extras_require = {
    'pyocd': ['pyocd>=0.28.3']
}

version_file = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'mcutk/_version.py')

try:
    with open(version_file, 'w') as f:
        f.write("VERSION='%s'" % version)
except Exception as e:
    print(e)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pymcutk",
    version=version,
    url='https://github.com/Hoohaha/pymcutk',
    description="A lite tool kit for MCU.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Haley Guo, Fly Yu",
    license="MIT License",
    install_requires=install_requires,
    extras_require=extras_require,
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mtk = mcutk.__main__:main',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
