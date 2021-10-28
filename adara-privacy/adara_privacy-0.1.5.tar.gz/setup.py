from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="adara_privacy",
    version='0.1.5',
    author="Adara, Inc.",
    author_email="privacy-sdk@adara.com",
    description="The Adara Privacy SDK is an open source library which allows you to safely manage sensitive Personally Identifiable Information (PII).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/adarainc/adara-privacy-sdk-python",
    packages=['adara_privacy'],
    include_package_data=True,
    scripts=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "requests"
    ]
)
