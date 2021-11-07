import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('src/scaffold/base')

setuptools.setup(
    name="flask_scaffolding",
    version="0.0.12",
    author="Muhammad Yunus",
    author_email="yunusmuhammad007@gmail.com",
    description="Flask Scaffolding with buiiltin Authentication & Authorization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Muhammad-Yunus/Flask-Scaffolding-Base",
    project_urls={
        "Bug Tracker": "https://github.com/Muhammad-Yunus/Flask-Scaffolding-Base/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={'': extra_files},
    python_requires=">=3.6"

)