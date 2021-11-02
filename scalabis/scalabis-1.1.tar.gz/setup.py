from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = '1.1' 
DESCRIPTION = """A Python3 module for fast & easy sequence comparison."""

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="scalabis", 
        version=VERSION,
        author="Afonso M Bravo",
        author_email="<afonsombravo@hotmail.com>",
        url='https://github.com/afombravo/scalabis',
        description=DESCRIPTION,
        long_description=long_description,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=[],
        
        keywords=['sequence', 'mismatch', 'comparison'],
        classifiers= [
            "Development Status :: 6 - Mature",
            "Intended Audience :: Science/Research",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ]
)