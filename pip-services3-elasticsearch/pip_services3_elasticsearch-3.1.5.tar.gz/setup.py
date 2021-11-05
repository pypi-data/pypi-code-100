"""
Pip.Services Elasticsearch
------------------

Pip.Services is an open-source library of basic microservices.
pip_services3_elasticsearch  contains logging components with data storage on the Elasticsearch server.

Links
`````

* `website <http://github.com/pip-services/pip-services>`_
* `development version <http://github.com/pip-services3-python/pip-services3-elasticsearch-python>`

"""

from setuptools import find_packages
from setuptools import setup

readme = ''

try:
    readme = open('readme.md').read()
except:
    readme = __doc__

setup(
    name='pip_services3_elasticsearch',
    version='3.1.5',
    url='http://github.com/pip-services3-python/pip-services3-elasticsearch-python',
    license='MIT',
    author='Conceptual Vision Consulting LLC',
    author_email='seroukhov@gmail.com',
    description='ElasticSearch components for Pip.Services in Python',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['config', 'data', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'moment',
        'elasticsearch',

        'pip-services3-commons >= 3.3.9, < 4.0',
        'pip-services3-components >= 3.5.0, < 4.0',
        'pip-services3-rpc >= 3.2.12, < 4.0'

    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
