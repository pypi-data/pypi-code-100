#!/usr/bin/env python

from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name="pyparsec",
      version="0.7.4",
      description="Parsec From Haskell Python 3 Portable",
      long_description=long_description,
      long_description_content_type='text/markdown',
      author="marsliu",
      author_email="mars.liu@outlook.com",
      url="https://github.com/Dwarfartisan/pyparsec",
      license="MIT",
      packages=["parsec", "test"],
      package_dir={
          "parsec": "src/parsec",
          "test": "src/tests"
      },
      classifiers=[
          "Topic :: Utilities",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3 :: Only",
          "License :: OSI Approved :: MIT License"
      ]
      )
