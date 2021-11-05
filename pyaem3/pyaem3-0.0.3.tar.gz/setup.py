import setuptools
from setuptools import setup

setup(name='pyaem3',
      version='0.0.3',
      description='Python API for AEM',
      packages=setuptools.find_packages(),
      packages_src={'': 'PyAEM'},
      classifiers=[
              "Development Status :: 1 - Planning",
              "Intended Audience :: Developers",
              "Programming Language :: Python :: 3.8",
              "Operating System :: Unix",
              "Operating System :: MacOS :: MacOS X",
              "Operating System :: Microsoft :: Windows",
          ]
      )
