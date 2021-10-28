"""Setup script for ehttp-executor"""

# Standard library imports
import pathlib

# Third party imports
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).resolve().parent

# The text of the README file is used as a description
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ehttp-executor",
    version="1.0.0",
    description="Execute API method by HTTP",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://www.pepsi.com/",
    keywords='example project',
    author="Eugenia Morales",
    author_email="eugeniamorales251@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=["requests"],
)
