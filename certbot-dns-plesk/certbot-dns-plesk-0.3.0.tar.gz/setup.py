#! /usr/bin/env python
from os import path
from setuptools import setup
from setuptools import find_packages

version = "0.3.0"

with open('README.md') as f:
    long_description = f.read()

install_requires = [
    'acme>=0.31.0',
    'certbot>=1.18.0',
    'dns-lexicon>=3.2.4',
    'setuptools',
    'requests'
]

here = path.abspath(path.dirname(__file__))

setup(
    name='certbot-dns-plesk',
    version=version,

    description="plesk DNS Authenticator plugin for Certbot",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/spike77453/certbot-dns-plesk',
    author="Christian Schürmann",
    author_email='spike@fedoraproject.org',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],

    packages=find_packages(where='.', exclude=('tests', 'hooks')),
    install_requires=install_requires,

    # extras_require={
    #     'docs': docs_extras,
    # },

    entry_points={
        'certbot.plugins': [
            'dns-plesk = certbot_dns_plesk.dns_plesk:Authenticator',
        ],
    },
    test_suite='tests',
)
