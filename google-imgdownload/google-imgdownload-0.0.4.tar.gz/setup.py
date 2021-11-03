import os
import setuptools
with open("README.md","r") as fh:
    long_description=fh.read()

setuptools.setup(
    name = "google-imgdownload",
    version = "0.0.4",
    author = "Srinivasan",
    author_email = "srini.pit21@gmail.com",
    description = ("Download Google image as Bulk."),
    license = "MIT",
    keywords = "google image",
    url = "https://github.com/srivas91/google-imgdownload.git",
    download_url='',
    packages=setuptools.find_packages(),
    long_description="this project about downloading google image",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
)