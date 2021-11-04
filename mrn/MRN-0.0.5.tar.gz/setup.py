from setuptools import setup, find_packages, Extension

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.0.5'
DESCRIPTION = 'Library used to Normalize numerical time-series data'
LONG_DESCRIPTION = 'A package that allows to efficiently normalize numerical timeseries data without lossing long term memory dependency and to retain information from the data as possible.'

# Setting up
setup(
    name="MRN",
    version=VERSION,
    author="Philip Pankaj",
    author_email="<philip.pankaj@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=long_description,
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
