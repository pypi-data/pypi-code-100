from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["requests>=2.20", 'python-dateutil>=2']

import os.path

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name="skolo",
    version=get_version("skolo/__init__.py"),
    author="Skolo, LLC",
    author_email="admin@skolocfd.com",
    license = 'MIT License',
    description="A command line tool and python package for SkoloCFD",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/skoloCFD/skolo/",
    py_modules = ['skoloCliParser'],
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    entry_points = '''
        [console_scripts]
        skolo=skoloCliParser:main
    '''
)