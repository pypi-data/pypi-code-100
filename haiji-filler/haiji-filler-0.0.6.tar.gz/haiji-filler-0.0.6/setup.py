#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

def main():
    description = 'Just for test'
    setup(
        # package name(editable)
        # Note : name might end such as 'filler'
        name='haiji-filler',
        #name='pokemon-filler',
        # version(editable)
        version='0.0.6',
        # entry point(editable)
        entry_points = {
            'console_scripts':
            ['haiji_filler=haiji_filler:main'],
                        },
        #--- in this case, no need to edit below ---#
        classifiers=['Programming Language :: Python :: 3.9', ],
        author='example',
        author_email='example@example.jp',
        url='https://www.google.co.jp',
        description=description,
        long_description=description,
        zip_safe=False,
        include_package_data=True,
        packages=find_packages(),
        install_requires=[],
        tests_require=[],
        setup_requires=[],
        )

if __name__ == '__main__':
    main()
