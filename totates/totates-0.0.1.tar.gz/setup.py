#!/usr/bin/env python3

import setuptools

# with open("README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="totates",
    version="0.0.1",
    author="Johnny Accot",
    description="Manage ecmascript components",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    py_modules=["totates"],
    install_requires=[],
    entry_points={"console_scripts": ["totates = totates.cli:main"]},
    test_suite="tests.build_test_suite",
)
