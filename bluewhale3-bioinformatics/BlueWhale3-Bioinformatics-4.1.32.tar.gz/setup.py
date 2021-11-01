#!/usr/bin/env python
import setuptools

if __name__ == '__main__':
    setuptools.setup(
        use_scm_version=False,
        version='4.1.32',
        setup_requires=['setuptools-scm', 'setuptools>=40.0'],
        install_requires=[
            'BlueWhale3>=3.28.0',
            'bluewhale-widget-base>=4.14.1',
            'scipy>=1.5.0',
            'pyclipper>=1.2.0',
            'point-annotator~=2.0',
            'requests',
            'requests-cache',
            'serverfiles',
            'resdk>=13.3.0',
            'genesis-pyapi',
            # Versions are determined by Orange
            'numpy',
        ],
        extras_require={
            # docutils changed html in 0.17; fixing to 0.16 until parser fixed
            # todo: remove docutils when parser fixed in widget-base and released
            'doc': ['sphinx', 'recommonmark', 'sphinx_rtd_theme', 'docutils<0.17'],
            'test': [
                'flake8',
                'flake8-comprehensions',
                'flake8-black',
                'pep8-naming',
                'isort',
                'pre-commit',
                'pytest',
                'coverage',
                'codecov',
            ],
        },
    )