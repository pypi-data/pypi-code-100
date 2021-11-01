#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "pandas==1.2.4",
    "requests==2.25.1",
    "requests-toolbelt==0.9.1",
]

test_requirements = ['pytest>=3', ]

setup(
    author="modep-ai",
    author_email='contact@modep.ai',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python client for the modep API",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='modep_client',
    name='modep_client',
    packages=find_packages(include=['modep_client', 'modep_client.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/modep-ai/modep-client',
    version='0.0.1',
    zip_safe=False,
)
