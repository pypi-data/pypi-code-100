import os
from setuptools import setup

def get_long_description():
    with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf8") as fp:
        return fp.read()

setup(
    name="fp_functions",
    version="0.1.1",
    description="A small Python library that adds some functional programming features",
    author="Thomas Gregory",
    license="Apache License, Version 2.0",
    py_modules=["fp_functions"],
    requires=["more_itertools"],
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
)