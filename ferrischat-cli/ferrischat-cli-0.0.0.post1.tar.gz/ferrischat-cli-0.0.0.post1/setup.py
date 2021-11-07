import pathlib
import re

from setuptools import setup


setup(
    name="ferrischat-cli",
    author='Cryptex',
    url="https://github.com/FerrisChat/terris",
    version='0.0.0.post1',
    packages=[],
    license="EUPL v1.2",
    description="This is a mirror package of terris, please install that instead.",
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=['terris'],
)
