from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.1.0'
DESCRIPTION = 'A package manager to install general purpose script by Google Developer Student Club'

base_dir = os.environ['VIRTUAL_ENV'] 
path = os.path.join(base_dir,'bin')

f = open(f"{path}/gpscript","w")
f.write('python -c "from script.script import *; $1()" $2')
f.close()
os.system(f'chmod +x {path}/gpscript')

# Setting up
setup(
    name="gpscript",
    version=VERSION,
    author="Ujjwal Kar",
    author_email="ujjwalkar21@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
