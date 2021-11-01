from setuptools import setup

setup(
   name='mohit',
   version='0.1.0',
   author='jpts',
   author_email='jpts@pypi.org',
   packages=['mohit'],
   url='http://pypi.python.org/pypi/mohit/',
   description='Imports the mohit',
   install_requires=[
       "kubernetes >= 19.13.0",
       "awscli >= 1.21.5",
    ],
)
