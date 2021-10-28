# from https://packaging.python.org/tutorials/packaging-projects/

import os
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-alda_pipeline",
    version="0.0.1",
    author="AlDa",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/alda_pipeline",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/alda_pipeline/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
)

# --- to build 
# python3 -m pip install --upgrade build
# --- and 
# python3 -m build
# package saved in dist directory