import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "compliantdynamodb",
    "version": "0.0.20",
    "description": "compliantdynamodb",
    "license": "Apache-2.0",
    "url": "https://github.com/jhornung/compliantDynamodb.git",
    "long_description_content_type": "text/markdown",
    "author": "Janek<jhornung@oev.de>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/jhornung/compliantDynamodb.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "compliant_dynamodb",
        "compliant_dynamodb._jsii"
    ],
    "package_data": {
        "compliant_dynamodb._jsii": [
            "compliantdynamodb@0.0.20.jsii.tgz"
        ],
        "compliant_dynamodb": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-backup>=1.129.0, <2.0.0",
        "aws-cdk.aws-dynamodb>=1.129.0, <2.0.0",
        "aws-cdk.aws-events>=1.129.0, <2.0.0",
        "aws-cdk.aws-iam>=1.129.0, <2.0.0",
        "aws-cdk.aws-kinesis>=1.129.0, <2.0.0",
        "aws-cdk.aws-kms>=1.129.0, <2.0.0",
        "aws-cdk.core>=1.129.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.40.0, <2.0.0",
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
