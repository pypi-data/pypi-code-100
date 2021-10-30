#!/usr/bin/env python

from setuptools import setup

with open("README.md") as readme:
    setup(
        name="snvis",
        version="0.1.0",
        description="Social network visualising tool",
        long_description=readme.read(),
        long_description_content_type="text/markdown",
        url="https://github.com/Callum-Irving/snvis",
        author="Callum Irving",
        author_email="callum.irving04@gmail.com",
        license="MIT",
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.9",
        ],
        packages=["snvis"],
        install_requires=["thefuzz >= 0.19.0", "python-igraph >= 0.9.8"],
        entry_points={"console_scripts": ["snvis = snvis.__main__:main"]}
    )
