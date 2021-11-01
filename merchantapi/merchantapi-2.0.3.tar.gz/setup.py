"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

import sys
from setuptools import setup, find_packages
from merchantapi.version import Version

setup(
    name='merchantapi',
    version=Version.STRING,
    license='Miva SDK License Agreement',
    author='Miva, Inc.',
    author_email='support@miva.com',
    url='https://www.miva.com',
    description='Miva Merchant JSON API SDK',
    long_description=open('README.md', encoding='utf-8').read().strip(),
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['examples', 'tests']),
    py_modules=['merchantapi'],
    install_requires=['requests', 'pycryptodome'],
    zip_safe=False,
    keywords='miva merchant json api sdk',
    python_requires='>=3.6'
)
