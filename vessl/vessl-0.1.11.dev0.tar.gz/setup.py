import os
from importlib.machinery import SourceFileLoader

import setuptools

version = (
    SourceFileLoader(
        "vessl._version",
        os.path.join(
            "vessl",
            "_version.py",
        ),
    )
    .load_module()
    .__VERSION__
)

with open("README.md") as fh:
    long_description = fh.read()

requirements = [
    "boto3",
    "click==8.0.1",
    "inquirer>=2.7.0",
    "numpy",
    "paramiko==2.7.2",
    "Pillow>=8.0.0",
    "python-dateutil>=2.8.1",
    "requests>=2.0.0",
    "requests-futures>=1.0.0",
    "sentry-sdk>=1.1.0",
    "schema>=0.7.4",
    "shortuuid",
    "sshpubkeys==3.3.1",
    "terminaltables>=3.1.0",
    "timeago==1.0.15",
    "toml==0.10.1",
    "tqdm",
]

setuptools.setup(
    name="vessl",
    version=version,
    author="Vessl AI Dev Team",
    author_email="contact@vessl.ai",
    description="A library and CLI for Vessl",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "vessl=vessl.cli._main:cli",
            "vsl=vessl.cli._main:cli",
        ],
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
