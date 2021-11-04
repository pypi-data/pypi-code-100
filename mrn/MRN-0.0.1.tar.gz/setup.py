from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Library used to Normalize numerical time-series data'
LONG_DESCRIPTION = 'A package that allows to efficiently normalize numerical timeseries data without lossing long term memory dependency and to retain information from the data as possible.'

# Setting up
setup(
    name="MRN",
    version=VERSION,
    author="Philip Pankaj",
    author_email="<philip.pankaj@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy'],
    keywords=['python', 'normalization', 'standardization', 'long term memory', 'LTM', 'LTM Normalization'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)