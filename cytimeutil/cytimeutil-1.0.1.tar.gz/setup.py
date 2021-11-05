#-*-coding:utf-8-*-
import setuptools

with open("README.md","r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
        name = "cytimeutil",
        version = "1.0.1",
        author = "lybule52",
        author_email = "ly352hz@163.com",
        description = "This is a Time calculation module",
        long_description = long_description,
        long_description_content_type = "text/markdown",
        url = "https://upload.pypi.org/legacy",
        packages = setuptools.find_packages(),
        classifiers=[
        "Programming Language :: Python :: 3",
            ],
        )
