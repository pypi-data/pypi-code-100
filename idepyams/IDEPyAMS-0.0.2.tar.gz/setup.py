from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='IDEPyAMS',
    version='0.0.2',
    description='PyAMS: Python for Analog and Mixed Signals',
    author= 'd.fathi',
    url = 'https://pyams.org',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['','symbols','symbols.basic','symbols.source','demo'],
    keywords=['Creating new symbols ', 'CAD System', 'Simulation circuit'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
    py_modules=['IDEPyAMS','SymbolEditor'],
    package_dir={'':'src','symbols':'src/symbols','symbols.basic':'src/symbols/basic','symbols.source':'src/symbols/source','demo':'src/demo'},
    install_requires = [
        'PyQt5',
        'PyQtWebEngine'
    ],
    package_data={'symbols.basic': ['*'],'symbols.source': ['*'],'demo': ['*']},
    include_package_data=True
)

