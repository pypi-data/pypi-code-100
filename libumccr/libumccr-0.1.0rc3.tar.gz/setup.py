# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

from libumccr import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="libumccr",
    version=__version__,
    author="UMCCR and Contributors",
    author_email="services@umccr.org",
    description="UMCCR Reusable Python modules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/umccr/libumccr",
    license="MIT",
    packages=find_packages(exclude=("tests**", "docs")),
    extras_require={
        "dev": [
            "pipdeptree",
            "sphinx",
            "twine",
            "setuptools",
            "wheel",
            "pdoc3",
        ],
        "test": [
            "pytest",
            "pytest-cov",
            "flake8",
            "mockito",
            "tox",
            "nose2",
        ],
        "all": [
            "Django",
        ],
    },
    install_requires=[
        "boto3",
        "botocore",
        "cachetools",
        "requests",
        "pandas",
        "gspread",
        "gspread-pandas",
        "google-auth",
    ],
    python_requires=">=3.6",
)
