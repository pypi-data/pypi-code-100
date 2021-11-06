from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Converts frames into video'
LONG_DESCRIPTION = 'A package that allows you to convert a directory of frames into a video.'

# Setting up
setup(
    name="frametovideo",
    version=VERSION,
    author="Jonas Barth",
    author_email="jonas.barth.95@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=['frametovideo.writer'],
    install_requires=['glob2', 'dataclasses'],
    keywords=['python', 'video', 'converter', 'images', 'frames'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)