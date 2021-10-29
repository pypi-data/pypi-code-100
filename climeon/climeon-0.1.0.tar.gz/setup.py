# pylint: disable=missing-module-docstring

from setuptools import setup, find_packages

PYPI_DESCRIPTION = "Climeon utility functions."

setup(
    name="climeon",
    packages=find_packages(),
    version="0.1.0",
    license="MIT",
    description=PYPI_DESCRIPTION,
    long_description=PYPI_DESCRIPTION,
    author="Emil Hjelm",
    author_email="emil.hjelm@climeon.com",
    keywords=["climeon", "REST", "API"],
    python_requires="!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=[
        "fastparquet",
        "matplotlib",
        "msal",
        "pandas",
        "requests"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ]
)
