import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-datalake-constructs",
    "version": "0.0.39",
    "description": "AWS CDK Constructs that can be used to create datalakes/meshes and more",
    "license": "MIT",
    "url": "https://github.com/randyridgley/cdk-datalake-constructs.git",
    "long_description_content_type": "text/markdown",
    "author": "Randy Ridgley<randy.ridgley@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/randyridgley/cdk-datalake-constructs.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_datalake_constructs",
        "cdk_datalake_constructs._jsii"
    ],
    "package_data": {
        "cdk_datalake_constructs._jsii": [
            "cdk-datalake-constructs@0.0.39.jsii.tgz"
        ],
        "cdk_datalake_constructs": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.assets>=1.85.0, <2.0.0",
        "aws-cdk.aws-athena>=1.85.0, <2.0.0",
        "aws-cdk.aws-cloudwatch>=1.85.0, <2.0.0",
        "aws-cdk.aws-ec2>=1.85.0, <2.0.0",
        "aws-cdk.aws-events-targets>=1.85.0, <2.0.0",
        "aws-cdk.aws-events>=1.85.0, <2.0.0",
        "aws-cdk.aws-glue>=1.85.0, <2.0.0",
        "aws-cdk.aws-iam>=1.85.0, <2.0.0",
        "aws-cdk.aws-kinesis>=1.85.0, <2.0.0",
        "aws-cdk.aws-kinesisanalytics>=1.85.0, <2.0.0",
        "aws-cdk.aws-kinesisfirehose>=1.85.0, <2.0.0",
        "aws-cdk.aws-kms>=1.85.0, <2.0.0",
        "aws-cdk.aws-lakeformation>=1.85.0, <2.0.0",
        "aws-cdk.aws-lambda-nodejs>=1.85.0, <2.0.0",
        "aws-cdk.aws-lambda-python>=1.85.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.85.0, <2.0.0",
        "aws-cdk.aws-logs>=1.85.0, <2.0.0",
        "aws-cdk.aws-s3-assets>=1.85.0, <2.0.0",
        "aws-cdk.aws-s3-deployment>=1.85.0, <2.0.0",
        "aws-cdk.aws-s3-notifications>=1.85.0, <2.0.0",
        "aws-cdk.aws-s3>=1.85.0, <2.0.0",
        "aws-cdk.aws-sns>=1.85.0, <2.0.0",
        "aws-cdk.aws-stepfunctions-tasks>=1.85.0, <2.0.0",
        "aws-cdk.aws-stepfunctions>=1.85.0, <2.0.0",
        "aws-cdk.core>=1.85.0, <2.0.0",
        "aws-cdk.custom-resources>=1.85.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.41.0, <2.0.0",
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
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
