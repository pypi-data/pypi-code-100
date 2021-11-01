# Always prefer setuptools over distutils
from setuptools import setup

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


classifiers = [
    "Intended Audience :: Developers",
    "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Operating System :: OS Independent",
]

setup(
    name="getDynamicUrl",
    version="0.0.6",
    license="MIT",
    description="Get dyanmic Url",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="Jhone Mendez",
    author_email="jhone0901@gmail.com",
    classifiers=classifiers,
    packages=["dynamic_url"],
    keywords="dynamicUrl",
    install_requires=["google-cloud-bigquery", "pyarrow"],
)
