import io
import os
import re
from setuptools import setup

# Use the README.md content for the long description:
with io.open("README.md", encoding="utf-8") as fileObj:
    long_description = fileObj.read()

with open("jetorm/__init__.py") as file:
    regex_version = r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]'
    version = re.search(regex_version, file.read(), re.MULTILINE).group(1) 

setup(
    name='jetorm',
    version=version,
    url='https://github.com/immadev2k21/JetORM',
    packages=['jetorm'],
    author='kapitanov',
    author_email='<leonidmilk2007@gmail.com>',
    description=('JetORM is the simplest ORM of its kind.'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['prettytable==2.2.1', 'PyMySQL==1.0.2'],
    license='MIT license',
    keywords="db database orm ORM jet JetORM jetorm easy simple"
)

