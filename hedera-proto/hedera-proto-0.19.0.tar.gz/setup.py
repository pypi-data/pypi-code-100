import os
import setuptools
import xml.etree.ElementTree as ET

pom = ET.parse("./src/hedera_proto/pom.xml")
version = [a.text for a in pom.getroot().getchildren() if a.tag == '{http://maven.apache.org/POM/4.0.0}version'][0]
version = version.split("-")[0]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hedera-proto",
    version=version,
    author="Wensheng Wang",
    author_email="wenshengwang@gmail.com",
    description="Hedera Protobufs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carady/hedera-proto-python",
    project_urls={
        "Bug Tracker": "https://github.com/carady/hedera-proto-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=['grpcio>=1.34.1'],
    python_requires=">=3.7",
    include_package_data=True,
    package_data={ "hedera_proto": ["*.xml"]},
)
