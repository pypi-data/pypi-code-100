from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'Potits trucs utils on ne sait jamais'
LONG_DESCRIPTION = 'Plein de trucs sympa, voir le repo github pour plus de datails'

# Setting up
setup(
    name="utis_matisse",
    version=VERSION,
    author="momoladebrouill",
    author_email="<momoladebrouill@github.io>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'maths', 'OOP'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
