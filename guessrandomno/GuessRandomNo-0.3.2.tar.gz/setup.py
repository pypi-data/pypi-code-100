from setuptools import setup, find_packages

VERSION = "0.3.2"
DESCRIPTION = "Random Number Package"

setup(
    name="GuessRandomNo",
    version=VERSION,
    author="Dhiraj Tembulkar",
    author_email="tembulkardhiraj@gmail.com",
    description=DESCRIPTION,
    packages = find_packages(),
    install_requires = [],
    keywords = ['python'],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
