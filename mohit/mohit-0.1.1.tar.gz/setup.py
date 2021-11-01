from setuptools import setup

setup(
   name='mohit',
   version='0.1.1',
   author='jpts',
   author_email='jpts@pypi.org',
   packages=['mohit'],
   url='http://pypi.python.org/pypi/mohit/',
   description='Imports the mohit',
   install_requires=[
       "kubernetes >= 19.13.0",
       "awscli >= 1.21.5",
       "google-api-python-client >= 2.24.0",
       "docker",
       "alive_progress",
    ],
)
