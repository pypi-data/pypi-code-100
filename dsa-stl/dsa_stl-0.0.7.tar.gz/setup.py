from setuptools import setup, find_packages
import codecs
import os
from dsa_stl import __version__ as version

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.7' #version
DESCRIPTION = 'DSA Algorithm'
LONG_DESCRIPTION = open('README.md').read()

# Setting up
setup(
    name="dsa_stl",
    version=VERSION,
    author="Aman Jaiswal (aman2000jaiswal)",
    author_email="<aman2000jaiswal14@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'dsa_stl','data structure','algorithms'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)