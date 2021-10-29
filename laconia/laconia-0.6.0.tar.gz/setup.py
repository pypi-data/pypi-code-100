#!/usr/bin/env python
from setuptools import setup

setup(
    name="laconia",
    use_scm_version={
        "local_scheme": "dirty-tag",
        "write_to": "laconia/_version.py",
        "fallback_version": "0.0.0",
    },
    packages=["laconia"],
    author="Ross Fenning",
    author_email="ross.fenning@gmail.com",
    url="http://github.com/avengerpenguin/laconia",
    description="Simple API for RDF",
    long_description="""Laconia is a Python API for RDF that is designed
to help easily learn and navigate the Semantic Web programmatically.
Unlike other RDF interfaces, which are generally triple-based, Laconia
binds RDF nodes to Python objects and RDF arcs to attributes of those
Python objects.""",
    license="GPLv3+",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=["rdflib"],
    setup_requires=[
        "setuptools_scm>=3.3.1",
        "pre-commit",
    ],
    extras_require={
        "test": [
            "pytest",
            "pytest-pikachu",
            "pytest-mypy",
        ],
    },
)
