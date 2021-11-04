#!/usr/bin/env python
import io

from setuptools import setup, find_packages

with io.open("README.md", encoding="utf-8") as f:
    readme = f.read()

requirements = [
    'Click>=7.0',
]

test_requirements = [
    'pytest>=3',
]

setup(
    author="Deshraj Yadav",
    author_email='deshraj.yadav@mltrics.ai',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Monitor ML models in production",
    entry_points={
        'console_scripts': [
            'mltrics=mltrics.cli:main',
        ],
    },
    install_requires=requirements,
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='mltrics',
    name='mltrics',
    packages=find_packages(include=['mltrics', 'mltrics.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mltrics-ai/mltrics',
    version='0.1.0',
    zip_safe=False,
)
