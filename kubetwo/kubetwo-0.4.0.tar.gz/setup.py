import json
import os
import re
import sys
from codecs import open
from pathlib import Path
import subprocess
from typing import List

from setuptools import setup
from setuptools.command.install import install


class VersionValidation(install):

    def run(self):
        with open("setup_info.json", "r") as f:
            version = json.load(f)["version"]

        result = subprocess.check_output("git tag -l", shell=True).decode('utf-8')
        registered_versions = [tag.strip("v") for tag in result.split("\n") if tag]

        if not re.match(r"^\d+\.\d+\.\d+$", version):
            print(f"Specified version {version} is invalid format.")
            sys.exit(1)

        if version in registered_versions:
            print(f"Specified version {version} is already registered.")
            sys.exit(1)

        print("Specified version is valid.")


def package_files(directory: str, excelude_suffix_list: List=[]) -> List[str]:
    directory_path = Path("kubetwo") / directory
    paths = []
    excelude_suffix_list = ["." + excelude_suffix for excelude_suffix in excelude_suffix_list]
    for path in directory_path.glob("**/*"):
        if path.suffix in excelude_suffix_list:
            continue
        paths.append(str(path.relative_to("kubetwo")))
    return paths


all_package_files = \
    package_files("ansible_template") + \
    package_files("data") + \
    package_files("terraform_template")

here = Path(os.path.dirname(__file__))

with open(here / "README.md", encoding="utf-8") as f:
    long_description = f.read()

with open(here / "requirements.txt") as f:
    install_requires = f.read().splitlines()

with open("setup_info.json", "r") as f:
    version = json.load(f)["version"]

setup(
    name="kubetwo",
    version=version,
    description="Simple CLI tool to create Kubernetes cluster on AWS EC2.",
    long_description=long_description,
    author="opeco17",
    url="https://github.com/opeco17/kubetwo",
    long_description_content_type="text/markdown",
    packages=["kubetwo"],
    package_data={"kubetwo": all_package_files},
    install_requires=install_requires,
    license="Apache License 2.0",
    python_requires=">= 3.6",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology"
    ],
    keywords="kubetwo kube-two kube2 kube-2",
    entry_points={
        "console_scripts": [
            "kubetwo = kubetwo.main:main"
        ]
    },
    cmdclass={
        'verify': VersionValidation
    }
)
