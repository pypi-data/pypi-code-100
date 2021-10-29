from setuptools import setup, find_packages
from _init_ import mp3
VERSION = '3.2.4' 
DESCRIPTION = 'python mp3 converter'
LONG_DESCRIPTION = 'A simple mp3 converter made in python'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="ytmp3 converter 2.0", 
        version=VERSION,
        author="Gavin Pritchard ",
        author_email="312983629@mcsdgas.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['ffmpeg', 'youtube-dl'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'youtube'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ]
)