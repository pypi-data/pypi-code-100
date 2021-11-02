from setuptools import setup
import sys

setup_requires = ['setuptools >= 30.3.0']
if {'pytest', 'test', 'ptr'}.intersection(sys.argv):
    setup_requires.append('pytest-runner')


setup(description="ccspectools",
      long_description=open('README.md').read(),
      version = '2.0.0', 
      setup_requires=setup_requires)
