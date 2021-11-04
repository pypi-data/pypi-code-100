import sys
from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

if sys.argv[1] not in ('sdist'):
    raise RuntimeError("Install aborted - please install python-dnf from distributiong system.")

setup(
    name='dnf',
    version='0.0.2.1',
    url='https://github.com/JaneSoo/rpm-dnf/',
    license='GPLv2+',
    author='DNF developers',
    author_email='ncoghlan@gmail.com',
    maintainer='Nick Coghlan',
    maintainer_email='ncoghlan@gmail.com',
    description='Dummy DNF package. Please use python-dnf provided by your OS.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    platforms='any',
)
