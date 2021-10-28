import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='drone-api-client',
    version='0.2.3',
    use_scm_version=False,
    description='Drone Api Python Client',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Biriukov Maksym',
    author_email='maximbirukov77@gmail.com',
    url="https://github.com/Slamnlc/drone-api-client",
    download_url='https://github.com/Slamnlc/drone-api-client/archive/refs/tags/v0.2.3.tar.gz',
    packages=setuptools.find_packages(exclude=("tests", "dev_tools")),
    install_requires=[
        'requests'
    ],
    entry_points={
        "drone_api": [
            "drone-api-client = drone_api_client.drone_api_client",
        ]
    },
)
