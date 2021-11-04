from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='classical',

    version='2.1.2',

    description='Class Tools for Python',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/altvod/classical',

    # Author details
    author='Grigory Statsenko',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],

    keywords=[
        'class',
        'utilities',
        'descriptors',
        'properties',
        'factories',
        'dataclasses',
        'attrs',
        'fields',
        'schematics',
        'sqlalchemy',
    ],

    packages=find_packages(exclude=['tests']),

    extras_require=dict(
        fielded=[
            'attr',
            'schematics',
            'sqlalchemy',
        ],
        testing=[
            'pylama',
            'pytest',
            'pytest-cov',
            'pytest-html',
        ],
        docs=[
            'sphinx',
            'sphinx_rtd_theme',
        ],
        build=[
            'build',
            'twine',
        ],
    )
)