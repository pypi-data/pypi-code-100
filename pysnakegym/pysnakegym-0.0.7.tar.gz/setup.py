from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.7'
DESCRIPTION = 'Gym for the Snake Game'
LONG_DESCRIPTION = 'A package that allows you to write training algorithms for the classic game of snake.'

# Setting up
setup(
    name="pysnakegym",
    version=VERSION,
    author="Jonas Barth",
    author_email="jonas.barth.95@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=['pysnakegym.game', 'pysnakegym.game.core', 'pysnakegym.mdp', 'pysnakegym.model'],
    install_requires=['torch==1.7.1', 'numpy', 'scipy', 'pygame==1.9.4', 'pytest'],
    keywords=['python', 'snake', 'game', 'video game'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)