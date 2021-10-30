from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'A Conversion package of Weights and Area'
LONG_DESCRIPTION = 'A package which helps in conversion of Weights,Area'

# Setting up
setup(
    name="anything-conversion",
    version=VERSION,
    author="sairamdgr8",
    author_email="<sairamdgr8@gmail.com>",
    description=DESCRIPTION,
    #long_description_content_type="text/markdown",
    #long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'convertor', 'weight', 'Area', 'Area conversion', 'Weights conversion'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)