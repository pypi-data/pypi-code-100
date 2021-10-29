from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'A package that can calculate distance between two points on Earth'
LONG_DESCRIPTION = 'A package that can calculate distance between two points on Earth with given longitude and latitude'

# Setting up
setup(
    name="dist_calculating",
    version=VERSION,
    url="https://github.com/reisgoldmanX/dist_calculations",
    author="reisgoldmanX (U D)",
    author_email="<reisgoldman@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'geography', 'meridian', 'distance calculations', 'earth', 'parallel'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)