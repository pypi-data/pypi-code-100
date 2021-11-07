import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-datadog-resources",
    "version": "0.2.42",
    "description": "@nomadblacky/cdk-datadog-resources",
    "license": "Apache-2.0",
    "url": "https://github.com/NomadBlacky/cdk-datadog-resources.git",
    "long_description_content_type": "text/markdown",
    "author": "NomadBlacky<nomadblacky@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/NomadBlacky/cdk-datadog-resources.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_datadog_resources",
        "cdk_datadog_resources._jsii"
    ],
    "package_data": {
        "cdk_datadog_resources._jsii": [
            "cdk-datadog-resources@0.2.42.jsii.tgz"
        ],
        "cdk_datadog_resources": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.core>=1.101.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.42.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
