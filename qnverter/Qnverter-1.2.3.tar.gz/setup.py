import os
import shutil

from os.path import join

import pathlib

from setuptools import find_packages
from setuptools import setup

here = pathlib.Path(__file__).parent.resolve()
long_description = open(join(here, 'README.md')).read()

setup(
        name='Qnverter',
        version="1.2.3",
        packages = ["qnverter"],
        url='https://github.com/Nicky5/Qnverter',
        license='MIT',
        author='nicky',
        author_email='vandini.elia@gmail.com',
        description='Python application for quick text conversions.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        install_requires=["certifi", "charset-normalizer" ,"idna" ,"PyQt5" ,"requests" ,"urllib3"],
        entry_points='''
            [console_scripts]
            qnverter=qnverter.qnverter:main
        '''
)

APPDIR = join(os.path.expanduser('~'), ".qnverter")
SCRIPTDIR = join(APPDIR, "scripts")
RESDIR = join(APPDIR, "resources")

try:
    os.mkdir(APPDIR)
    os.mkdir(SCRIPTDIR)
    os.mkdir(RESDIR)

    for i in os.listdir(join(here, "resources")):
        if i[-4:] == ".png":
            shutil.copy(join(join(here, "resources"), i), RESDIR)

    for i in os.listdir(join(here, "scripts")):
        if i[-3:] == ".py":
            shutil.copy(join(join(here, "scripts"), i), SCRIPTDIR)
except Exception as e:
    print(e)