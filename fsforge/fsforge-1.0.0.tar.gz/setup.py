#!/usr/bin/env python3


from setuptools import setup


with open("README.md", "rt", encoding="utf-8") as ff:
    long_description = ff.read()

setup(
    name="fsforge",
    version="1.0.0",
    description="Helper to create fake filesystem and quick capture its state (or state of a real one).",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: System :: Monitoring",
        "Topic :: Software Development :: Testing",
        "Framework :: Pytest",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
    ],
    keywords="fsforge pyfakefs fs forged literal dict hard disk HDD snapshot in-memory test",
    author="Michał Kaczmarczyk",
    author_email="michal.s.kaczmarczyk@gmail.com",
    url="https://gitlab.com/kamichal/fsforge",
    license="Apache License v.2",
    packages=[
        'fsforge',
    ],
    include_package_data=False,
    install_requires=[
        "pyfakefs==4.5.1",
    ],
)
