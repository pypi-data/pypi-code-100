import os

import setuptools

install_requires = [
    "httpx[http2]>=0.18",
    "simplejson",
]

test_requires = [
    "pytest",
    "pytest-xdist"
]

package_version = os.environ.get("PACKAGE_VERSION", "0.0.0")
package_name = os.environ.get("PACKAGE_NAME")
server_version = os.environ.get("JELASTIC_VERSION", "0.0.0")

setuptools.setup(
    name=package_name,
    version=package_version,
    author="Laurent Michel",
    author_email="softozor@gmail.com",
    description=f"A client library for Jelastic v{server_version}",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.hidora.com/softozor/packages",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    extras_require={
        "test": test_requires,
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
