from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name = 'autoauthnumber',
    version = '1.0.1',
    url='http://belfast.web3v.com/power/myself.html',
    keywords = ['auto', 'author number'],
    description = 'This is a library about automatic number-taking of "General Chinese Author Number Table". At present, there is only one way to take the number, that is, directly looking up the table.In the future, we will adapt to a variety of author numbering methods, please wait.',
    license = 'GPL-3.0 License',
    py_modules=['auto_AUTHNumber','author_number'],
    author = 'Matt Brown',
    author_email = 'thedayofthedo@gmail.compile',
    packages = find_packages(),
    platforms = 'any',
)
