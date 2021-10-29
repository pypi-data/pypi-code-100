from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Access your webcam and track your face'
# Setting up
setup(
    name="FaceC",
    version=VERSION,
    author="Goldenninja",
    author_email="",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python', 'mediapipe'],
    keywords=['python', 'face detector', 'face'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)
