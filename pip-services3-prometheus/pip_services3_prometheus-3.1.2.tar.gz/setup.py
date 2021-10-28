"""
Pip.Services Prometheus
--------------------

Pip.Services is an open-source library of basic microservices.
pip_services3_prometheus contains components for working with meters in the Prometheus service.

Links
`````

* `website <http://github.com/pip-services/pip-services>`
* `development version <http://github.com/pip-services-python/pip-services-prometheus-python>`

"""

from setuptools import find_packages
from setuptools import setup

try:
    readme = open('readme.md').read()
except:
    readme = __doc__

setup(
    name='pip_services3_prometheus',
    version='3.1.2',
    url='http://github.com/pip-services3-python/pip-services3-prometheus-python',
    license='MIT',
    description='Prometheus components for Pip.Services in Python',
    author='Conceptual Vision Consulting LLC',
    author_email='seroukhov@gmail.com',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['config', 'data', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'pytest',

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
