import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

# The execution of the Setup.py will install your package using, pip install

setuptools.setup(
    name="CL_Dynamic_Test_Case_Library", # A custom Library to create dynamic test cases
    version="1.0.7.9",
    author="sieqqc",
    author_email="sieqqc@gmail.com",
    description="A custom Library",
    long_description="A custom Library",
    long_description_content_type="text/markdown",
    url="http://10.21.37.110/corp_sieq/Partner%20Automation%20Testing%20Trial/_git/CL_Dynamic_Test_Case_Library",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)