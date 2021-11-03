import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="mediapipe-rpi3",
    version="0.8.8",
    description="MediaPipe for Raspberry Pi OS on Raspberry Pi 3",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/superuser789/MediaPipe-on-RaspberryPi",
    author="Nitin Singh",
    author_email="acc4nitin@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["mediapipe"],
    include_package_data=True,
    
    install_requires=["numpy", "absl-py", "attrs>=19.1.0", "protobuf>=3.11.4", "six", "wheel", "matplotlib"],

)