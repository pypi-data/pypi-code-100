from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'A simple colouring package for making console programmes great again.'

setup(
    name='colorain',
    version=VERSION,
    author='Susmit Islam',
    author_email='susmitislam31@gmail.com',
    description = DESCRIPTION,
    packages = find_packages(),
    install_requires = [],
    keywords=['terminal','color','colour','console'],
    classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)