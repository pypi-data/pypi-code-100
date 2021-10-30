from os import path

from setuptools import find_packages, setup

wdir = path.abspath(path.dirname(__file__))

with open(path.join(wdir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='elice-backend-components',

    description='Components for building elice-backend projects.',
    long_description=long_description,
    url='https://git.elicer.io/elice/elice-backend-components',

    author='elice.io',
    author_email='contact@elice.io',

    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X'
    ],

    python_requires='>=3.8, <3.11',

    packages=find_packages(),

    package_data={
        'ebc': ['py.typed']
    },

    zip_safe=False,

    use_scm_version={
        'write_to': 'ebc/_version.py'
    },
    setup_requires=['setuptools_scm'],

    install_requires=[
        'sentry-sdk>=1.4,<1.5',
        'setuptools-scm',
    ],

    extras_require={
        'dev': [
            'bandit',
            'flake8-bugbear',
            'flake8-datetimez',
            'flake8-isort',
            'flake8',
            'mypy',
            'pip-tools',
            'safety',
        ]
    }
)
