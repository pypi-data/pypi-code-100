"""
Pip.Services Redis
----------------------

Pip.Services is an open-source library of basic microservices.
pip_services3_redis module for working with a Redis database of type key-value contains components for working with cache and locks.

Links
`````

* `website <http://github.com/pip-services-python/>`_
* `development version <http://github.com/pip-services3-python/pip-services3-redis-python>`

"""

from setuptools import find_packages
from setuptools import setup

try:
    readme = open('readme.md').read()
except:
    readme = __doc__

setup(
    name='pip_services3_redis',
    version='3.0.1',
    url='http://github.com/pip-services3-python/pip-services3-redis-python',
    license='MIT',
    author='Conceptual Vision Consulting LLC',
    author_email='seroukhov@gmail.com',
    description='Communication components for Pip.Services in Python',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['config', 'data', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'redis',
        'pip-services3-commons >= 3.3.9, < 4.0',
        'pip-services3-components >= 3.5.0, < 4.0'
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
