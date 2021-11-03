# -*- coding:utf-8 -*-
from setuptools import setup, find_packages
from os.path import join, dirname

"""

python setup.py sdist bdist_wheel
twine upload dist/* 

"""


with open(join(dirname(__file__), 'pybirds/version.py'), 'r') as f:
    exec(f.read())

with open(join(dirname(__file__), 'requirements.txt'), 'r') as f:
    install_requires = f.read().split("\n")


setup(
    name='pybirds',
    version=__version__ ,
    description='Business Intelligence Risk Data Science',
    author='Ouyang Ruofei',
    author_email='rfouyang@gmail.com',
    packages=find_packages(),
    package_data={'pybirds': ['pybirds/*.pyi', 'pybirds/data/*']},
    zip_safe=False,
    include_package_data=True,
    url='',
    platforms='any',
    keywords=["pybirds", "birds"],
    install_requires=install_requires,
    tests_require=[
        'nose',
        'packaging'
    ],
    test_suite='nose.collector',
    classifiers=[
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.6'
)