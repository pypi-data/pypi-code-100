"""Setup file for package."""

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("../../protos/python_requirements.txt") as f:
    proto_reqs = f.read().splitlines()

setup(
    name="rime_sdk",
    version="0.12.0",
    packages=find_packages(include=["rime_sdk*"]),
    description="Package to programmatically access a RIME deployment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["simplejson",] + proto_reqs,
    python_requires=">=3.6",
    license="OSI Approved :: Apache Software License",
)
