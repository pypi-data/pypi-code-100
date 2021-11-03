import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='krules-cli',
    version='0.2.2',
    author="Alberto Degli Esposti",
    author_email="alberto@arispot.tech",
    description="KRules command line utility",
    license="Apache Licence 2.0",
    keywords="krules knative kubernetes eventing microservices serverless",
    url="https://github.com/airspot-dev/krules",
    long_description=read('README.md'),
    packages=find_packages(),
    py_modules=['krules_cli'],
    install_requires=[
        'click',
        'gitpython',
        'mdv',
        'krules-dev-support'
    ],
    entry_points={
        'console_scripts': [
            'krules = krules_cli.main:cli'
        ]
    }
)