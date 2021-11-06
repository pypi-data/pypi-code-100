from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.2'
DESCRIPTION = 'Automatically conducting a PVM Analysis'

with open("README.md","r") as fh:
	long_description = fh.read()

# Setting up
setup(
    name="autoPVM",
    version=VERSION,
    author="Akash Sonthalia",
    author_email="<axsonthalia@gmail.com>",
    description=DESCRIPTION,
    long_description= long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'plotly'],
    keywords=['python', 'data', 'analysis', 'data analysis', 'business analysis', 'PVM Analysis'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)